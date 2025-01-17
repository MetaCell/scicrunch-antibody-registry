from functools import cache

from django.contrib import admin
from django.contrib.admin.widgets import ManyToManyRawIdWidget, FilteredSelectMultiple
from django.forms import CheckboxSelectMultiple
from django.db.models import Q
from django.contrib.auth.models import User
from django.forms import TextInput, Textarea, URLInput
from django.db import models
from django.db.models.functions import Length
from django.urls import reverse
from django.utils.encoding import smart_str
from django.utils.html import escape, format_html, format_html_join, mark_safe
from django.utils.text import format_lazy
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from keycloak.exceptions import KeycloakGetError
from cloudharness_django.models import Member

from api.forms.AntibodyImportForm import AntibodyImportForm
from api.models import (
    STATUS,
    Antibody,
    Application,
    Vendor,
    Specie,
    VendorDomain,
    VendorSynonym, AntibodyFiles, CommercialType,
    Partner,
)
from api.import_export import AntibodyResource
from api.services.keycloak_service import KeycloakService
from cloudharness import log
from portal.settings import FOR_NEW_KEY, FOR_EXTANT_KEY, METHOD_KEY


@admin.display(description="ab_id")
def id_with_ab(obj: Antibody):
    return f"AB_{obj.ab_id}"


@cache
def get_user_by_kc_id(kc_id) -> User:
    try:
        return Member.objects.get(kc_id=kc_id).user
    except Member.DoesNotExist:
        return None


class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):
    """
    A Widget for displaying ManyToMany ids in the "raw_id" interface rather
    than in a <select multiple> box. Display user-friendly value like the ForeignKeyRawId widget
    """

    def label_and_url_for_value(self, value):
        values = value
        str_values = []
        field = self.rel.get_related_field()
        key = field.name
        fk_model = self.rel.model
        app_label = fk_model._meta.app_label
        class_name = fk_model._meta.object_name.lower()
        for the_value in values:
            try:
                obj = fk_model._default_manager.using(
                    self.db).get(**{key: the_value})
                url = reverse(
                    "admin:{0}_{1}_change".format(app_label, class_name), args=[obj.id]
                )
                label = escape(smart_str(obj))
                elt = '<a href="{0}" {1}>{2}</a>'.format(
                    url,
                    'onclick="return showAddAnotherPopup(this);" target="_blank"',
                    label,
                )
                str_values.append(elt)
            except fk_model.DoesNotExist:
                str_values.append("???")
        return mark_safe(", ".join(str_values)), ""

    def format_value(self, value):
        return ",".join(str(v) for v in value) if value else ""


class ApplicationsInlineAdmin(admin.TabularInline):
    model = Antibody.applications.through
    extra = 1


class TargetSpeciesInlineAdmin(admin.TabularInline):
    model = Antibody.species.through
    extra = 1
    autocomplete_fields = ("specie",)
    classes = ("collapse",)
    verbose_name = "Target Specie"


class AntibodyFilesAdmin(admin.TabularInline):
    model = AntibodyFiles
    fields = ("file", "type", "antibody")
    exclude = ("uploader_uid", 'filehash', 'timestamp', 'display_name')
    extra = 1


# not in fields - catalog_num_search
antibody_fields_shown = (
    "ab_name", "ab_id", "accession", "commercial_type", "catalog_num", "cat_alt", "citation", "vendor",
    "url", "ab_target", "entrez_id", "uniprot_id", "target_species_raw", "subregion",
    "modifications", "epitope", "source_organism", "clonality", "clone_id", "product_isotype",
    "product_conjugate", "defining_citation", "product_form", "comments",
    "kit_contents", "feedback", "curator_comment", "disc_date", "status", "show_link",
    # also in the read-only fields
    "uid", "uid_legacy", "insert_time", "lastedit_time", "curate_time",
)


@admin.register(Antibody)
class AntibodyAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):

    change_form_template = "admin/antibody_change_form.html"

    # Import/Export module settings
    import_template_name = "admin/import_export/custom_import_form.html"
    import_form_class = AntibodyImportForm
    resource_classes = [AntibodyResource]

    # list display settings
    list_filter = ("status",)
    list_display = (id_with_ab, "accession", "ab_name", "submitter_name", "citation", "status", "vendor", "catalog_num", "insert_time")
    search_fields = ("ab_id", "ab_name", "catalog_num")

    # the following - maintains the order of the fields
    fields = antibody_fields_shown

    inlines = [TargetSpeciesInlineAdmin, AntibodyFilesAdmin, ApplicationsInlineAdmin]

    readonly_fields = (
        "submitter_name",
        "submitter_email",
        "accession",
        "insert_time",
        "lastedit_time",
        "curate_time",
        "uid",
        "uid_legacy"
    )
    autocomplete_fields = ("vendor", "source_organism")
    save_on_top = True
    show_save = False

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '120'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 120})}
    }

    @property
    def keycloak_admin(self):
        from cloudharness.auth import AuthClient
        return AuthClient().get_admin_client()

    @cache
    def get_user(self, user_id):
        return self.keycloak_admin.get_user(user_id=user_id)

    @admin.display(description="Submitter name")
    def submitter_name(self, obj: Antibody):
        if not obj.uid:
            return "Unknown"

        dj_user: User = get_user_by_kc_id(obj.uid)
        if dj_user:
            return f"{dj_user.get_full_name()} ({dj_user.username})"
        try:
            submitter = self.get_user(user_id=obj.uid)
            return f"{submitter.get('firstName', '')} {submitter.get('lastName', '')} ({submitter['email']})"
        except KeycloakGetError:
            log.error(f"User {obj.uid} lookup error", exc_info=True)
            return f"{obj.uid} (not found)"
        except Exception:
            log.error(f"User {obj.uid} definition error", exc_info=True)
            return f"{obj.uid} (error)"

    @admin.display(description="Submitter email")
    def submitter_email(self, obj: Antibody):
        if not obj.uid:
            return "Unknown"

        dj_user: User = get_user_by_kc_id(obj.uid)
        if dj_user:
            return dj_user.email

        try:
            submitter = self.get_user(user_id=obj.uid)
            return f"{submitter['email']}"
        except:
            log.error(f"User {obj.uid} lookup error", exc_info=True)
            return "Error"

    def get_resource_kwargs(self, request, *args, **kwargs):
        rk = super().get_resource_kwargs(request, *args, **kwargs)
        rk["request"] = request
        return rk

    def get_import_data_kwargs(self, request, *args, **kwargs):
        kwargs[FOR_NEW_KEY] = request.POST.get(FOR_NEW_KEY, None)
        kwargs[FOR_EXTANT_KEY] = request.POST.get(FOR_EXTANT_KEY, None)
        kwargs[METHOD_KEY] = request.POST.get(METHOD_KEY, None)
        return super().get_import_data_kwargs(request, *args, **kwargs)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        search_term = search_term.strip()
        if search_term.lower().startswith("ab_"):
            queryset |= self.model.objects.filter(ab_id=search_term[3:])
        return queryset, may_have_duplicates

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name not in ("species", "applications"):
            return super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == "applications":
            kwargs["widget"] = CheckboxSelectMultiple(

            )
            if "queryset" not in kwargs:
                queryset = db_field.related_model.objects.all()
                if queryset is not None:
                    kwargs["queryset"] = queryset
            form_field = db_field.formfield(**kwargs)
            # msg = "Hold down “Control”, or “Command” on a Mac, to select more than one."
            # help_text = form_field.help_text
            # form_field.help_text = (
            #     format_lazy("{} {}", help_text, msg) if help_text else msg
            # )
            return form_field
        if db_field.name == "species":
            kwargs["widget"] = VerboseManyToManyRawIdWidget(
                db_field.remote_field, self.admin_site
            )
            return ""

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if formset.fk.model == AntibodyFiles:
                keycloak_service = KeycloakService()
                uid = keycloak_service.get_user_id_from_django_user(request.user)
                if not uid:
                    raise Exception("User not found")
                instance.uploader_uid = uid
            instance.save()
        formset.save_m2m()


# @admin.register(Antigen)
# class GeneAdmin(admin.ModelAdmin):
#     search_fields = ("symbol",)
#     list_display = ("symbol",)
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size':'150'})},
#     }

@admin.register(Specie)
class SpecieAdmin(admin.ModelAdmin):
    search_fields = ("name",)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request,
            queryset,
            search_term,
        )
        search_term = search_term.strip()
        if search_term:
            queryset = queryset.filter(name__icontains=search_term).order_by(
                Length("name").asc()
            )
        return queryset, may_have_duplicates


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class NonCuratedDomains(admin.SimpleListFilter):
    title = "Vendor Domain Status"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "curated_domain"

    def lookups(self, request, model_admin):
        return (
            ("Non-curated", ("Vendors with non-curated domains")),
            ("Curated", ("Vendors with curated domains")),
            ("No-domain", ("Vendors with no domains")),
        )

    def queryset(self, request, queryset):
        if self.value() == "Non-curated":
            return queryset.exclude(vendordomain__status=STATUS.CURATED).exclude(vendordomain__base_url__isnull=True)
        if self.value() == "Curated":
            return queryset.filter(vendordomain__status=STATUS.CURATED)
        if self.value() == "No-domain":
            return queryset.filter(vendordomain__base_url__isnull=True)


class VendorSynonymInline(admin.TabularInline):
    model = VendorSynonym
    show_change_link = True
    extra = 0


class VendorDomainInline(admin.TabularInline):
    model = VendorDomain
    fields = ("base_url", "status")
    # readonly_fields = ("base_url", "status")
    show_change_link = True
    extra = 0


class CommercialTypeFilter(admin.SimpleListFilter):
    title = "Commercial Type"
    parameter_name = "commercial_type"

    def lookups(self, request, model_admin):
        return [
            (CommercialType.COMMERCIAL, ("Commercial vendors")),
            (CommercialType.PERSONAL, ("Personal vendors")),
            (CommercialType.NON_PROFIT, ("Non-profit vendors")),
            (CommercialType.OTHER, ("Other vendors")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(vendor__commercial_type=self.value())
        return queryset


@admin.register(VendorDomain)
class VendorDomainAdmin(SimpleHistoryAdmin):
    list_display = (
        "base_url",
        "vendor",
        "status",
        "is_domain_visible",
    )
    list_editable = ("is_domain_visible",)
    list_filter = [CommercialTypeFilter]


@admin.register(Vendor)
class VendorAdmin(SimpleHistoryAdmin):
    delete_confirmation_template = "admin/vendor/delete_confirmation.html"
    search_fields = ("name",)
    list_display = ("id", "name", "commercial_type", "nif_id", "eu_id")
    ordering = ("-id",)
    list_filter = (NonCuratedDomains, "commercial_type",)
    fields = (
        "nb_antibodies",
        "recent_antibodies",
        "name",
        "nif_id",
        "eu_id",
        "commercial_type",
        "show_link"
    )
    readonly_fields = ("nb_antibodies", "recent_antibodies")
    inlines = [
        VendorSynonymInline,
        VendorDomainInline,
    ]

    @admin.display(description="Number of antibodies")
    def nb_antibodies(self, obj):
        return Antibody.objects.filter(vendor=obj).count()

    @admin.display(description=format_html("Recent antibodies<br/>(in queue)"))
    def recent_antibodies(self, obj, limit=10):
        antibodies = Antibody.objects.filter(vendor=obj, status=STATUS.QUEUE)
        # size = len(antibodies)
        if not antibodies.exists():
            return "None"
        return format_html_join(
            "\n", "<li>{}</li>", ((id_with_ab(a),) for a in antibodies)
        )

    def delete_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context["vendors"] = list(
            self.model.objects.filter(~Q(id=object_id)))
        extra_context["nb_antibodies"] = list(
            Antibody.objects.filter(vendor=object_id))
        return super().delete_view(
            request,
            object_id,
            extra_context,
        )

    def _force_delete(self, src_vendor: Vendor):
        # We make copies of the iterables, just in case
        to_delete = [a for a in src_vendor.antibody_set.all()]
        to_delete.extend(d for d in src_vendor.vendordomain_set.all())
        for entity in to_delete:
            entity.delete()

    def _swap_ownership(self, src_vendor, target_vendor):
        # We transfer the antibodies to the new vendor
        for ab in src_vendor.antibody_set.all():
            target_vendor.antibody_set.add(ab)
        for domain in src_vendor.vendordomain_set.all():
            target_vendor.vendordomain_set.add(domain)
        for synonym in src_vendor.vendorsynonym_set.all():
            target_vendor.vendorsynonym_set.add(synonym)
        VendorSynonym.objects.create(name=src_vendor.name, vendor=target_vendor)
        src_vendor.antibody_set.remove()
        src_vendor.vendordomain_set.remove()

        # We save the updated model
        src_vendor.save()
        target_vendor.save()

    def get_deleted_objects(self, objs, request):
        if request.method == "POST":
            if not objs:
                return super().get_deleted_objects(objs, request)
            src_vendor = objs[0]
            # This case is only for deleting single vendor
            if "_swap_ownership" in request.POST:
                target_vendor = self.model.objects.filter(
                    id=request._post["vendors"]
                ).first()
                self._swap_ownership(src_vendor, target_vendor)
                return super().get_deleted_objects(objs, request)
            # This case if for deleting a vendor, forcing antibody deletion also
            if "_force_delete" in request.POST:
                self._force_delete(src_vendor)
                return super().get_deleted_objects(objs, request)
        return super().get_deleted_objects(objs, request)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    pass
