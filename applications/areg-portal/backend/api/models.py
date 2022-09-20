from django.db import models
from django.db.models import Q

from areg_portal.settings import ANTIBODY_NAME_MAX_LEN, ANTIBODY_TARGET_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIBODY_CATALOG_NUMBER_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_CLONE_ID_MAX_LEN, ANTIGEN_ENTREZ_ID_MAX_LEN, ANTIGEN_UNIPROT_ID_MAX_LEN, STATUS_MAX_LEN, \
    ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, \
    ANTIBODY_TARGET_MODIFICATION_MAX_LEN, ANTIBODY_TARGET_SUBREGION_MAX_LEN, ANTIBODY_DEFINING_CITATION_MAX_LEN, \
    ANTIBODY_ID_MAX_LEN, ANTIBODY_CAT_ALT_MAX_LEN, VENDOR_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_TARGET_EPITOPE_MAX_LEN, \
    VENDOR_NIF_MAX_LEN, ANTIBODY_TARGET_SPECIES_MAX_LEN, ANTIBODY_DISC_DATE_MAX_LEN, \
    URL_MAX_LEN


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
    name = models.CharField(max_length=VENDOR_MAX_LEN, db_column='vendor')
    nif_id = models.CharField(max_length=VENDOR_NIF_MAX_LEN, db_column='nif_id', null=True)

    def __str__(self):
        return self.name


class VendorSynonym(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)


class Specie(models.Model):
    name = models.CharField(max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, unique=True)


class VendorDomain(models.Model):
    base_url = models.URLField(unique=True, max_length=URL_MAX_LEN, null=True, db_column='domain_name')
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True, db_column='vendor_id')
    is_domain_visible = models.BooleanField(default=True, db_column='link')
    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS.choices,
        default=STATUS.QUEUE
    )

    def __str__(self):
        return self.base_url


class Antigen(models.Model):
    symbol = models.CharField(max_length=ANTIBODY_TARGET_MAX_LEN, db_column='ab_target', null=True)
    entrez_id = models.CharField(unique=True, max_length=ANTIGEN_ENTREZ_ID_MAX_LEN, db_column='ab_target_entrez_gid',
                                 null=True)
    uniprot_id = models.CharField(unique=True, max_length=ANTIGEN_UNIPROT_ID_MAX_LEN, null=True)

    def __str__(self):
        return self.entrez_id


class Antibody(models.Model):
    # todo: make sure autoincrement is functional with incremental ingestion
    ix = models.AutoField(primary_key=True, unique=True, null=False)
    ab_name = models.CharField(max_length=ANTIBODY_NAME_MAX_LEN)
    ab_id = models.IntegerField()
    accession = models.CharField(max_length=ANTIBODY_ID_MAX_LEN)
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
        null=True
    )
    # todo: change to foreignKey to user model @afonsobspinto
    uid = models.CharField(max_length=ANTIBODY_ID_MAX_LEN)
    catalog_num = models.CharField(max_length=ANTIBODY_CATALOG_NUMBER_MAX_LEN)
    cat_alt = models.CharField(max_length=ANTIBODY_CAT_ALT_MAX_LEN)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True)
    url = models.URLField(max_length=URL_MAX_LEN)
    antigen = models.ForeignKey(Antigen, on_delete=models.RESTRICT, db_column='antigen_id')
    species = models.ManyToManyField(Specie, db_column='target_species', related_name="targets",
                                     through='AntibodySpecies')
    subregion = models.CharField(max_length=ANTIBODY_TARGET_SUBREGION_MAX_LEN, db_column='target_subregion')
    modifications = models.CharField(max_length=ANTIBODY_TARGET_MODIFICATION_MAX_LEN, db_column='target_modification')
    epitope = models.CharField(max_length=ANTIBODY_TARGET_EPITOPE_MAX_LEN)
    source_organism = models.ForeignKey(Specie, on_delete=models.RESTRICT, related_name="source")
    clonality = models.CharField(
        max_length=ANTIBODY_CLONALITY_MAX_LEN,
        choices=AntibodyClonality.choices,
        default=AntibodyClonality.UNKNOWN,
    )
    clone_id = models.CharField(max_length=ANTIBODY_CLONE_ID_MAX_LEN)
    product_isotype = models.CharField(max_length=ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN)
    product_conjugate = models.CharField(max_length=ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN)
    defining_citation = models.CharField(max_length=ANTIBODY_DEFINING_CITATION_MAX_LEN)
    product_form = models.CharField(max_length=ANTIBODY_PRODUCT_FORM_MAX_LEN)
    comments = models.TextField()
    feedback = models.TextField()
    curator_comment = models.TextField()
    disc_date = models.CharField(max_length=ANTIBODY_DISC_DATE_MAX_LEN)
    status = models.CharField(
        max_length=STATUS_MAX_LEN,
        choices=STATUS.choices,
        default=STATUS.QUEUE
    )
    insert_time = models.DateTimeField(auto_now_add=True)
    curate_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.uid

    class Meta:
        constraints = [
            models.CheckConstraint(check=~Q(status='curated') | (Q(status='curated') &
                                                                 Q(catalog_num__isnull=False) &
                                                                 Q(ab_name__isnull=False) &
                                                                 Q(ab_name__exact='') &
                                                                 Q(vendor__isnull=False)),
                                   name='curated_constraints'),
        ]


class AntibodySpecies(models.Model):
    antibody = models.ForeignKey(Antibody, on_delete=models.CASCADE)
    specie = models.ForeignKey(Specie, on_delete=models.CASCADE)
