import os
import re
from random import randint
from typing import Optional, Tuple
from api.repositories.maintainance import refresh_search_view

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector, SearchVectorField
from django.db import models, transaction
from django.db.models import Transform, CharField, Index, Q, Value
from django.db.models.functions import Length, Coalesce
from django.utils import timezone

from api.services.user_service import UnrecognizedUser, get_current_user_id
from api.utilities.exceptions import RequiredParameterMissing
from api.utilities.functions import catalog_number_chunked, generate_id_aux, extract_base_url, \
    get_antibody_persistence_directory
from cloudharness import log
from portal.settings import ANTIBODY_NAME_MAX_LEN, ANTIBODY_TARGET_MAX_LEN, APPLICATION_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIBODY_CATALOG_NUMBER_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_CLONE_ID_MAX_LEN, ANTIGEN_ENTREZ_ID_MAX_LEN, ANTIGEN_UNIPROT_ID_MAX_LEN, STATUS_MAX_LEN, \
    ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, \
    ANTIBODY_TARGET_MODIFICATION_MAX_LEN, ANTIBODY_TARGET_SUBREGION_MAX_LEN, ANTIBODY_DEFINING_CITATION_MAX_LEN, \
    ANTIBODY_ID_MAX_LEN, ANTIBODY_CAT_ALT_MAX_LEN, VENDOR_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_TARGET_EPITOPE_MAX_LEN, \
    VENDOR_NIF_MAX_LEN, ANTIBODY_TARGET_SPECIES_MAX_LEN, ANTIBODY_DISC_DATE_MAX_LEN, \
    URL_MAX_LEN, VENDOR_EU_ID_MAX_LEN, ANTIBODY_UID_MAX_LEN, ANTIBODY_FILE_DISPLAY_NAME_MAX_LEN, \
    ANTIBODY_FILES_HASH_MAX_LEN, ANTIBODY_FILE_TYPE_MAX_LEN


@CharField.register_lookup
class Normalize(Transform):
    lookup_name = 'normalize'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return (f"regexp_replace({lhs}, '[^a-zA-Z0-9]', '', 'g')", params)


@CharField.register_lookup
class NormalizeRelaxed(Transform):
    lookup_name = 'normalize_relaxed'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return (f"regexp_replace({lhs}, '[^a-zA-Z0-9, ]', '', 'g')", params)


@CharField.register_lookup
class RemoveComa(Transform):
    lookup_name = 'remove_coma'

    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return (f"replace({lhs}, ',', '')", params)


class CommercialType(models.TextChoices):
    COMMERCIAL = 'commercial', 'commercial'
    PERSONAL = 'personal', 'personal'
    NON_PROFIT = 'non-profit', 'non-profit'
    OTHER = 'other', 'other'


class AntibodyClonality(models.TextChoices):
    UNKNOWN = 'unknown', 'Unknown'
    COCKTAIL = 'cocktail', 'Cocktail'
    CONTROL = 'control', 'Control'
    ISOTYPE_CONTROL = 'isotype control', 'Isotype Control'
    MONOCLONAL = 'monoclonal', 'Monoclonal'
    MONOCLONAL_SECONDARY = 'monoclonal secondary', 'Monoclonal Secondary'
    POLYCLONAL = 'polyclonal', 'Polyclonal'
    POLYCLONAL_SECONDARY = 'polyclonal secondary', 'Polyclonal Secondary'
    OLIGOCLONAL = 'oligoclonal', 'Oligoclonal'
    RECOMBINANT = 'recombinant', 'Recombinant'
    RECOMBINANT_MONOCLONAL = 'recombinant monoclonal', 'Recombinant Monoclonal'
    RECOMBINANT_MONOCLONAL_SECONDARY = 'recombinant monoclonal secondary', 'Recombinant Monoclonal Secondary'
    RECOMBINANT_POLYCLONAL = 'recombinant polyclonal', 'Recombinant Polyclonal'
    RECOMBINANT_POLYCLONAL_SECONDARY = 'recombinant polyclonal secondary', 'Recombinant Polyclonal Secondary'


class STATUS(models.TextChoices):
    CURATED = 'CURATED', 'Curated'
    REJECTED = 'REJECTED', 'Rejected'
    QUEUE = 'QUEUE', 'Queued'


class Vendor(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN,
                            db_column='vendor', db_index=True, unique=False)
    nif_id = models.CharField(
        max_length=VENDOR_NIF_MAX_LEN, db_column='nif_id', null=True, blank=True)
    eu_id = models.CharField(
        max_length=VENDOR_EU_ID_MAX_LEN, db_column='euid', null=True, blank=True)
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
        null=True,
        db_index=True,
    )
    show_link = models.BooleanField(default=False, null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            GinIndex(SearchVector('name', config='english'),
                     name='vendor_name_fts_idx'),
        ]
        ordering = ('name',)

    def __str__(self):
        return self.name


class VendorSynonym(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN, db_index=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "%s->%s" % (self.name, self.vendor.name)


class Specie(models.Model):
    name = models.CharField(
        max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, unique=True, db_index=True)

    class Meta:
        indexes = [
            GinIndex(SearchVector('name', config='english'),
                     name='specie_name_fts_idx'),
        ]

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(
        max_length=APPLICATION_MAX_LEN, unique=True, db_index=True)

    class Meta:
        indexes = [
            GinIndex(SearchVector('name', config='english'),
                     name='application_name_fts_idx'),
        ]

    def __str__(self):
        return self.name


class VendorDomain(models.Model):
    base_url = models.CharField(max_length=URL_MAX_LEN,
                                null=True, db_column='domain_name', db_index=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, null=True, db_column='vendor_id', db_index=True)
    is_domain_visible = models.BooleanField(default=True, db_column='link')
    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS.choices,
        default=STATUS.QUEUE, db_index=True
    )

    def __str__(self):
        return self.base_url


class Antigen(models.Model):
    symbol = models.CharField(max_length=ANTIBODY_TARGET_MAX_LEN,
                              db_column='ab_target', null=True, db_index=True)

    class Meta:
        indexes = [
            GinIndex(SearchVector('symbol', config='english'),
                     name='gene_symbol_fts_idx'),
        ]

    def __str__(self):
        return self.symbol


class Antibody(models.Model):
    ix = models.AutoField(primary_key=True, unique=True, null=False)
    ab_name = models.CharField(
        max_length=ANTIBODY_NAME_MAX_LEN, null=True, db_index=True, blank=True)
    ab_id = models.CharField(
        max_length=ANTIBODY_ID_MAX_LEN, null=True, db_index=True)
    accession = models.CharField(
        max_length=ANTIBODY_ID_MAX_LEN, null=True, blank=True, db_index=True)
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
        null=True,
        blank=True,
        db_index=True,
    )
    # This user id maps the users in keycloak
    uid = models.CharField(
        max_length=ANTIBODY_UID_MAX_LEN, null=True, db_index=True, blank=True)
    # Maps to old users -- used only for migration purpose
    uid_legacy = models.IntegerField(null=True, blank=True)
    catalog_num = models.CharField(
        max_length=ANTIBODY_CATALOG_NUMBER_MAX_LEN, null=True, db_index=True, blank=True)
    catalog_num_search = models.CharField(
        max_length=ANTIBODY_CATALOG_NUMBER_MAX_LEN, null=True, db_index=True, blank=True)

    cat_alt = models.CharField(
        max_length=ANTIBODY_CAT_ALT_MAX_LEN, null=True, db_index=True, blank=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.SET_NULL, null=True, blank=True)

    url = models.URLField(max_length=URL_MAX_LEN,
                          null=True, db_index=True, blank=True)
    # antigen = models.ForeignKey(
    #     Antigen, on_delete=models.SET_NULL, db_column='antigen_id', null=True, blank=True)
    ab_target = models.CharField(max_length=ANTIBODY_TARGET_MAX_LEN,
                                 db_column='ab_target', null=True, db_index=True, blank=True,
                                 verbose_name="Target antigen")
    entrez_id = models.CharField(unique=False, max_length=ANTIGEN_ENTREZ_ID_MAX_LEN, db_column='ab_target_entrez_gid',
                                 null=True, db_index=True, blank=True)
    uniprot_id = models.CharField(
        unique=False, max_length=ANTIGEN_UNIPROT_ID_MAX_LEN, null=True, db_index=True, blank=True)
    target_species_raw = models.CharField(
        max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, null=True, blank=True, verbose_name="Target species (csv)", db_index=True,
        help_text="Comma separated value for target species. Values filled here will be parsed and assigned to the 'Target species' field.")

    species = models.ManyToManyField(Specie, db_column='target_species', related_name="targets",
                                     through='AntibodySpecies', blank=True, verbose_name="Target species")
    subregion = models.CharField(max_length=ANTIBODY_TARGET_SUBREGION_MAX_LEN, db_column='target_subregion', null=True,
                                 db_index=True, blank=True)
    modifications = models.CharField(max_length=ANTIBODY_TARGET_MODIFICATION_MAX_LEN, db_column='target_modification',
                                     null=True, db_index=True, blank=True)
    epitope = models.CharField(
        max_length=ANTIBODY_TARGET_EPITOPE_MAX_LEN, null=True, db_index=True, blank=True)
    source_organism = models.ForeignKey(
        Specie, on_delete=models.RESTRICT, related_name="source", null=True, blank=True)
    clonality = models.CharField(
        max_length=ANTIBODY_CLONALITY_MAX_LEN,
        choices=AntibodyClonality.choices,
        default=AntibodyClonality.UNKNOWN,
        db_index=True,
        null=True,
        blank=True
    )
    clone_id = models.CharField(
        max_length=ANTIBODY_CLONE_ID_MAX_LEN, null=True, db_index=True, blank=True)
    product_isotype = models.CharField(
        max_length=ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, null=True, db_index=True, blank=True)
    product_conjugate = models.CharField(
        max_length=ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, null=True, db_index=True, blank=True)
    defining_citation = models.CharField(
        max_length=ANTIBODY_DEFINING_CITATION_MAX_LEN, null=True, blank=True, db_index=False)
    product_form = models.CharField(
        max_length=ANTIBODY_PRODUCT_FORM_MAX_LEN, null=True, db_index=True, blank=True)
    comments = models.TextField(null=True, blank=True, db_index=False)
    applications = models.ManyToManyField(
        Application, through='AntibodyApplications', blank=True)
    kit_contents = models.TextField(null=True, db_index=True, blank=True)
    feedback = models.TextField(null=True, db_index=True, blank=True)
    curator_comment = models.TextField(null=True, db_index=True, blank=True)
    disc_date = models.CharField(
        max_length=ANTIBODY_DISC_DATE_MAX_LEN, null=True, db_index=True, blank=True)
    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS.choices,
        default=STATUS.QUEUE,
        db_index=True
    )
    insert_time = models.DateTimeField(
        auto_now_add=True, db_index=True, null=True, blank=True)
    lastedit_time = models.DateTimeField(auto_now=True, db_index=True, null=True, blank=True)
    curate_time = models.DateTimeField(db_index=True, null=True, blank=True)
    # whether the full link to the antibody is shown. If None, the vendor's default is used
    show_link = models.BooleanField(null=True, blank=True, db_index=True)

    def import_save(self):
        first_save = self.ix is None
        if first_save:
            super().save()
            self._handle_duplicates()
        
        if self.catalog_num:
            self.catalog_num_search = catalog_number_chunked(self.catalog_num, self.cat_alt)

        if not self.accession or not self.ab_id:
            self._generate_automatic_attributes()
        super().save()

    @transaction.atomic
    def save(self, *args, update_search=True, **kwargs):
        first_save = self.ix is None
        self._handle_status_changes(first_save)

        # It's not an import that activated the save
        # We need to merge the data in a smart way
        old_instance = Antibody.objects.filter(pk=self.pk).first()
        old_species = self.species_from_raw(old_instance.target_species_raw) if old_instance else set()

        super(Antibody, self).save(*args, **kwargs)

        if self.catalog_num:
            self.catalog_num_search = catalog_number_chunked(self.catalog_num, self.cat_alt)
        self._handle_duplicates(*args, **kwargs)
        self._generate_related_fields(*args, **kwargs)
        self._synchronize_target_species(old_species)

        if first_save:  # Newly instantiated instances have ix = None
            self._generate_automatic_attributes(*args, **kwargs)

        super(Antibody, self).save()
        if int(self.ab_id) == 0:
            raise Exception(f"Error during antibody id assignment: {self.ix}")
        if update_search and self.status == STATUS.CURATED:
            refresh_search_view()


    def _has_target_species_raw_changed(self, old_instance):
        if old_instance:
            return self.target_species_raw != old_instance.target_species_raw
        return self.target_species_raw is not None


    def delete(self, *args, **kwargs):
        super(Antibody, self).delete(*args, **kwargs)
        if self.status == STATUS.CURATED:
            refresh_search_view()

    def _generate_automatic_attributes(self, *args, **kwargs):
        """
        Generates ab_id, accession and status for newly created instances
        """
        if not self.ab_id:
            self.ab_id = self._generate_ab_id()
        elif type(self.ab_id) is str:
            self.ab_id = int(self.ab_id.replace('AB_', ''))
        if not self.accession:
            self.accession = self.ab_id
        elif type(self.accession) is str:
            self.accession = int(float(self.accession.replace('AB_', '')))
        if self.status is None:
            self.status = STATUS.QUEUE
        if not self.uid:
            try:
                self.uid = get_current_user_id()
            except:
                log.exception("Could not set user")

    def _handle_status_changes(self, first_save=False):
        """
        Updates curate_time on status changes to CURATED
        """

        if self.status == STATUS.CURATED:
            if first_save:
                self.curate_time = timezone.now()
            else:
                try:
                    old_version = Antibody.objects.get(ix=self.ix)
                    if old_version.status != STATUS.CURATED:
                        self.curate_time = timezone.now()
                except Antibody.DoesNotExist:
                    self.curate_time = timezone.now()

    def _handle_duplicates(self, *args, **kwargs):
        """
        Verifies if instance meets the duplicate criteria and acts accordingly
        """
        duplicate = self.get_duplicate()
        if duplicate:
            self.ab_id = duplicate.ab_id
            self.accession = self.accession or self._generate_ab_id()

    def _generate_ab_id(self) -> int:
        return generate_id_aux(self.ix)

    @staticmethod
    def species_from_raw(raw):
        if raw:
            return {specie_name.strip().lower() for specie_name in re.split(r'[,;]', raw)}
        return set()

    def _synchronize_target_species(self, old_species):
        new_species = self.species_from_raw(self.target_species_raw)

        if new_species != old_species or len(new_species) != self.species.count():
            to_remove =  old_species - new_species
            if to_remove:
                for specie_name in to_remove:
                    specie_name = specie_name.strip().lower()
                    try:
                        specie = Specie.objects.get(name=specie_name)
                    except Specie.DoesNotExist:
                        continue
                    self.species.remove(specie)
            to_add = new_species - old_species
            if to_add:
                for specie_name in to_add:
                    specie_name = specie_name.strip().lower()
                    specie, _ = Specie.objects.get_or_create(name=specie_name)
                    self.species.add(specie)

        self._fill_target_species_raw_from_species()





    def _target_species_from_raw(self):
        species = []
        if self.target_species_raw:
            for specie_name in re.split(r'[,;]', self.target_species_raw):
                specie_name = specie_name.strip().lower()
                specie, _ = Specie.objects.get_or_create(name=specie_name)
                species.append(specie)

        return species

    def _fill_target_species_raw_from_species(self):
        self.refresh_from_db(fields=['species'])
        species_names = self.species.values_list('name', flat=True)
        self.target_species_raw = ';'.join(species_names)

    def get_duplicate(self) -> Optional['Antibody']:
        """
        Returns a non-personal antibody with the same vendor_id and same catalog_number if exists
        """
        if self.vendor and self.catalog_num:
            duplicate_antibodies = Antibody.objects.filter(
                vendor__id=self.vendor.id,
                catalog_num__iexact=self.catalog_num, 
            ).exclude(commercial_type=CommercialType.PERSONAL).exclude(ix=self.ix).exclude(status=STATUS.REJECTED)
            duplicates_length = len(duplicate_antibodies)
            if duplicates_length == 0:  # Because the save happened before there will always be one antibody in the database
                return None
            # Work around to handle the temporary
            if duplicates_length > 2 and len(set(ab.ab_id for ab in duplicate_antibodies if ab.ab_id is not None)) > 1:
                # creation of entities on the confirmation step of django-import-export
                log.error("Unexpectedly found multiple antibodies with catalog number %s and vendor %s",
                          self.catalog_num, self.vendor.name)
            return duplicate_antibodies[0]
        return None

    def set_vendor_from_name_url(self, url, name=None):
        """
        Sets vendor from name and url.

        if the name exists:
            if the url exists:
                return existing vendor
            else:
                create new vendor domain and associate to existing vendor
        else:
            if the url exists:
                try to guess a vendor just by the url and add a vendor synonym
            else if the url doesn't exist:
                create a new vendor with the name from url
            else:
                do nothing
        """

        base_url = url and extract_base_url(url)
        try:
            # First, try to match by exact name
            vendor = Vendor.objects.get(name__iexact=name or base_url)
            self.vendor = vendor
            if base_url:
                self.add_vendor_domain(base_url, vendor)
        except Vendor.MultipleObjectsReturned:
            log.exception("Multiple vendors with name %s", name)
            vendor = self.vendor = Vendor.objects.filter(name__iexact=name or base_url)[0]
            if base_url:
                self.add_vendor_domain(base_url, vendor)
        except Vendor.DoesNotExist:
            # Then, try to match by domain

            vds = VendorDomain.objects.filter(base_url__iexact=base_url, status=STATUS.CURATED)
            if len(vds) == 0:
                # If the domain is not matched, try to match by domain with and without www

                if "www." in base_url:
                    alt_base_url = base_url.replace("www.", "")
                else:
                    alt_base_url = "www." + base_url
                vds = VendorDomain.objects.filter(base_url__iexact=alt_base_url, status=STATUS.CURATED)

                if len(vds) == 0:
                    # As it doesn't match, create a new vendor
                    vendor_name = name or base_url
                    log.info("Creating new Vendor `%s` on domain  to `%s`",
                             vendor_name, base_url)
                    vendor = Vendor(name=vendor_name,
                                    commercial_type=self.commercial_type)
                    vendor.save()
                    self.vendor = vendor
                    if base_url:
                        self.add_vendor_domain(base_url, vendor)
                    return


            # Vendor domain matched one way or the other, so associate to existing vendor
            if len(vds) > 1:
                log.error("Unexpectedly found multiple vendor domains for %s", base_url)

            self.vendor = vds[0].vendor
            if name:
                VendorSynonym.objects.create(vendor=self.vendor, name=name)

    def add_vendor_domain(self, base_url, vendor):
        try:
            VendorDomain.objects.get(base_url__iexact=base_url)
        except VendorDomain.DoesNotExist:
            vd = VendorDomain(vendor=vendor,
                              base_url=base_url, status=STATUS.QUEUE)
            vd.save()

    def _generate_related_fields(self, *args, **kwargs):
        """
        Creates VendorDomain entity from current vendor content if non-existent
        """
        if self.url:
            if not self.vendor:
                self.set_vendor_from_name_url(url=self.url)
            else:
                self.add_vendor_domain(extract_base_url(self.url), self.vendor)

    def __str__(self):
        return 'AB_' + str(self.ab_id)

    class Meta:
        verbose_name_plural = "antibodies"
        constraints = [
            models.CheckConstraint(check=~Q(status='curated') | (Q(status='curated') &
                                                                 Q(catalog_num__isnull=False) &
                                                                 Q(ab_name__isnull=False) &
                                                                 Q(ab_name__exact='') &
                                                                 Q(vendor__isnull=False)),
                                   name='curated_constraints'),
        ]
        indexes = [
            GinIndex(SearchVector('catalog_num_search', config='simple'),
                     # TODO the english configurations has stop words we don't want here
                     name='antibody_catalog_num_fts_idx'),

            Index(fields=['-disc_date'], name='antibody_discontinued_idx'),

        ]


def get_antibody_filename(instance, original_filename):
    name, extension = os.path.splitext(original_filename)
    rand_str = str(randint(0, 9999)).zfill(4)[:4]
    return f"AB{instance.antibody.ab_id}_{str.upper(instance.type)}{rand_str}{extension}"


def antibody_persistence_directory(instance, filename):
    return get_antibody_persistence_directory(instance.antibody.ab_id, get_antibody_filename(instance, filename))


class AntibodyFiles(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False)
    antibody = models.ForeignKey(
        Antibody, on_delete=models.CASCADE, db_column='ab_ix')
    type = models.CharField(
        max_length=ANTIBODY_FILE_TYPE_MAX_LEN, null=True, default="mds")
    file = models.FileField(upload_to=antibody_persistence_directory)
    display_name = models.CharField(
        max_length=ANTIBODY_FILE_DISPLAY_NAME_MAX_LEN)
    timestamp = models.DateTimeField(auto_now_add=True)
    uploader_uid = models.CharField(max_length=ANTIBODY_UID_MAX_LEN)
    filehash = models.CharField(max_length=ANTIBODY_FILES_HASH_MAX_LEN)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.id is None:
            self.display_name = get_antibody_filename(self, self.file.name)
        super(AntibodyFiles, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Antibody files"


class AntibodySpecies(models.Model):
    antibody = models.ForeignKey(
        Antibody, on_delete=models.CASCADE, db_index=True)
    specie = models.ForeignKey(
        Specie, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "AB_%s->%s" % (self.antibody.ab_id, self.specie.name)


def get_or_create_specie(**kwargs) -> Tuple[Specie, bool]:
    name = kwargs.get('name', None)
    if name is None:
        raise RequiredParameterMissing('name')

    new = False
    try:
        specie = Specie.objects.get(name=name)
    except Specie.DoesNotExist:
        specie = Specie(**kwargs)
        specie.save()
        new = True
    return specie, new


class AntibodyApplications(models.Model):
    antibody = models.ForeignKey(
        Antibody, on_delete=models.CASCADE, db_index=True)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "AB_%s->%s" % (self.antibody.ab_id, self.application.name)


class AntibodySearch(models.Model):
    ix = models.OneToOneField(Antibody, on_delete=models.DO_NOTHING, db_column='ix', primary_key=True)
    search_vector = SearchVectorField(null=True)
    citations = models.FloatField(null=True)
    data = models.IntegerField(null=True)
    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        db_index=True,
        null=True,
    )

    class Meta:
        # managed = False
        db_table = 'antibody_search'
        indexes = [
            GinIndex(
                fields=["search_vector"],
                name='antibody_search_fts_idx'),

        ]
