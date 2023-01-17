from typing import Optional

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Transform, CharField, Index, Q, Value
from django.db.models.functions import Length, Coalesce
from django.utils import timezone

from api.utilities.exceptions import DuplicatedAntibody
from api.utilities.functions import generate_id_aux
from cloudharness import log
from portal.settings import ANTIBODY_NAME_MAX_LEN, ANTIBODY_TARGET_MAX_LEN, APPLICATION_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIBODY_CATALOG_NUMBER_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_CLONE_ID_MAX_LEN, ANTIGEN_ENTREZ_ID_MAX_LEN, ANTIGEN_UNIPROT_ID_MAX_LEN, STATUS_MAX_LEN, \
    ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, \
    ANTIBODY_TARGET_MODIFICATION_MAX_LEN, ANTIBODY_TARGET_SUBREGION_MAX_LEN, ANTIBODY_DEFINING_CITATION_MAX_LEN, \
    ANTIBODY_ID_MAX_LEN, ANTIBODY_CAT_ALT_MAX_LEN, VENDOR_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_TARGET_EPITOPE_MAX_LEN, \
    VENDOR_NIF_MAX_LEN, ANTIBODY_TARGET_SPECIES_MAX_LEN, ANTIBODY_DISC_DATE_MAX_LEN, \
    URL_MAX_LEN, VENDOR_EU_ID_MAX_LEN, ANTIBODY_UID_MAX_LEN


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
                            db_column='vendor', db_index=True)
    nif_id = models.CharField(
        max_length=VENDOR_NIF_MAX_LEN, db_column='nif_id', null=True, blank=True)
    eu_id = models.CharField(
        max_length=VENDOR_EU_ID_MAX_LEN, db_column='euid', null=True, blank=True)
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
        null=True
    )

    class Meta:
        indexes = [
            GinIndex(SearchVector('name', config='english'),
                     name='vendor_name_fts_idx'),
        ]

    def __str__(self):
        return self.name


class VendorSynonym(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN, db_index=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "%s->%s" % (self.name, self.vendor.name)


class Specie(models.Model):
    name = models.CharField(
        max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, unique=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(
        max_length=APPLICATION_MAX_LEN, unique=True)

    def __str__(self):
        return self.name


class VendorDomain(models.Model):
    base_url = models.URLField(unique=True, max_length=URL_MAX_LEN,
                               null=True, db_column='domain_name', db_index=True)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.RESTRICT, null=True, db_column='vendor_id', db_index=True)
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
    entrez_id = models.CharField(unique=False, max_length=ANTIGEN_ENTREZ_ID_MAX_LEN, db_column='ab_target_entrez_gid',
                                 null=True, db_index=True, blank=True)
    uniprot_id = models.CharField(
        unique=False, max_length=ANTIGEN_UNIPROT_ID_MAX_LEN, null=True, db_index=True, blank=True)

    class Meta:
        indexes = [
            GinIndex(SearchVector('symbol', config='english'),
                     name='gene_symbol_fts_idx'),
        ]

    def __str__(self):
        return f"{self.symbol or '?' + self.id}"


class Antibody(models.Model):
    ix = models.AutoField(primary_key=True, unique=True, null=False)
    ab_name = models.CharField(
        max_length=ANTIBODY_NAME_MAX_LEN, null=True, db_index=True)
    ab_id = models.CharField(
        max_length=ANTIBODY_ID_MAX_LEN, null=True, db_index=True)
    accession = models.CharField(max_length=ANTIBODY_ID_MAX_LEN, null=True, blank=True)
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
        null=True
    )
    # This user id maps the users in keycloak
    uid = models.CharField(
        max_length=ANTIBODY_UID_MAX_LEN, null=True, db_index=True, blank=True)
    # Maps to old users -- used only for migration purpose
    uid_legacy = models.IntegerField(null=True, blank=True)
    catalog_num = models.CharField(
        max_length=ANTIBODY_CATALOG_NUMBER_MAX_LEN, null=True, db_index=True)
    cat_alt = models.CharField(
        max_length=ANTIBODY_CAT_ALT_MAX_LEN, null=True, db_index=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True)
    url = models.URLField(max_length=URL_MAX_LEN, null=True, db_index=True, blank=True)
    antigen = models.ForeignKey(
        Antigen, on_delete=models.RESTRICT, db_column='antigen_id', null=True)
    target_species_raw = models.CharField(
        max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, null=True, blank=True)

    species = models.ManyToManyField(Specie, db_column='target_species', related_name="targets",
                                     through='AntibodySpecies', blank=True)
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
        max_length=ANTIBODY_DEFINING_CITATION_MAX_LEN, null=True, blank=True)
    product_form = models.CharField(
        max_length=ANTIBODY_PRODUCT_FORM_MAX_LEN, null=True, db_index=True, blank=True)
    comments = models.TextField(null=True, blank=True)
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
    lastedit_time = models.DateTimeField(
        auto_now=True, db_index=True, null=True)
    curate_time = models.DateTimeField(db_index=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self._handle_status_changes()
        self._generate_automatic_attributes(*args, **kwargs)
        has_duplicate = self._handle_duplicates()
        super(Antibody, self).save(*args, **kwargs)
        if has_duplicate:
            raise DuplicatedAntibody()

    def _generate_automatic_attributes(self, *args, **kwargs):
        """
        Generates ab_id, accession and status for newly created instances
        """
        if not self.ix:  # Newly instantiated instances have ix = None
            super(Antibody, self).save(*args, **kwargs)
            self.ab_id = self._generate_ab_id()
            self.accession = self.ab_id
            self.status = STATUS.QUEUE

    def _handle_status_changes(self):
        """
        Updates curate_time on status changes to CURATED
        """
        if self.status == STATUS.CURATED:
            old_version = Antibody.objects.get(ix=self.ix)
            if old_version.status != STATUS.CURATED:
                self.curate_time = timezone.now()

    def _handle_duplicates(self) -> bool:
        """
        Verifies if instance meets the duplicate criteria and acts accordingly
        """
        duplicate = self._get_duplicate()
        if duplicate:
            self.ab_id = duplicate.ab_id
        return duplicate is not None

    def _generate_ab_id(self) -> int:
        return generate_id_aux(self.ix)

    def _get_duplicate(self) -> Optional['Antibody']:
        """
        Returns a non-personal antibody with the same vendor_id and same catalog_number if exists
        """
        duplicate_antibodies = Antibody.objects.filter(vendor__id=self.vendor.id, catalog_num=self.catalog_num) \
            .exclude(commercial_type=CommercialType.PERSONAL)
        duplicates_length = len(duplicate_antibodies)
        if duplicates_length == 1:  # Because the save happened before there will always be one antibody in the database
            return None
        if duplicates_length > 2:
            log.error("Unexpectedly found multiple antibodies with catalog number %s and vendor %s", self.vendor.name,
                      self.catalog_num)
        return duplicate_antibodies[0]

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
            GinIndex(SearchVector('catalog_num__normalize',
                                  'cat_alt__normalize_relaxed', config='english'), name='antibody_catalog_num_fts_idx'),

            Index((Length(Coalesce('defining_citation', Value(''))) - Length(Coalesce(
                'defining_citation__remove_coma', Value('')))).desc(), name='antibody_nb_citations_idx'),

            Index((Length(Coalesce('defining_citation', Value(''))) - Length(Coalesce('defining_citation__remove_coma',
                                                                                      Value(''))) - (
                           100 + Length(Coalesce('disc_date', Value(''))))).desc(),
                  name='antibody_nb_citations_idx2'),

            Index(fields=['-disc_date'], name='antibody_discontinued_idx'),

            GinIndex(SearchVector('ab_name',
                                  'clone_id__normalize_relaxed', config='english', weight='A'),
                     name='antibody_name_fts_idx'),
            GinIndex(
                SearchVector('ab_name',
                             'clone_id__normalize_relaxed', config='english', weight='A') +
                SearchVector(
                    'accession',
                    'commercial_type',
                    'uid',
                    'uid_legacy',
                    'url',
                    'subregion',
                    'modifications',
                    'epitope',
                    'clonality',
                    'product_isotype',
                    'product_conjugate',
                    'defining_citation',
                    'product_form',
                    'comments',
                    'kit_contents',
                    'feedback',
                    'curator_comment',
                    'disc_date',
                    'status',
                    config='english',
                    weight='C',
                ), name='antibody_all_fts_idx'),

            GinIndex(
                SearchVector(
                    'accession',
                    'commercial_type',
                    'uid',
                    'uid_legacy',
                    'url',
                    'subregion',
                    'modifications',
                    'epitope',
                    'clonality',
                    'product_isotype',
                    'product_conjugate',
                    'defining_citation',
                    'product_form',
                    'comments',
                    'kit_contents',
                    'feedback',
                    'curator_comment',
                    'disc_date',
                    'status',
                    config='english',
                    weight='C',
                ), name='antibody_all_fts_idx2'),
        ]


class AntibodySpecies(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE, db_index=True)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "AB_%s->%s" % (self.antibody.ab_id, self.specie.name)


class AntibodyApplications(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE, db_index=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return "AB_%s->%s" % (self.antibody.ab_id, self.application.name)
