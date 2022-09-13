from django.db import models

from areg_portal.settings import ANTIBODY_NAME_MAX_LEN, ANTIBODY_TARGET_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIBODY_CATALOG_NUMBER_MAX_LEN, ANTIBODY_SOURCE_ORGANISM_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_CLONE_ID_MAX_LEN, ANTIGEN_ENTREZ_ID_MAX_LEN, ANTIGEN_UNIPROT_ID_MAX_LEN, STATUS_MAX_LEN, \
    ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, \
    ANTIBODY_TARGET_MODIFICATION_MAX_LEN, ANTIBODY_TARGET_SUBREGION_MAX_LEN, ANTIBODY_DEFINING_CITATION_MAX_LEN, \
    ANTIBODY_ID_MAX_LEN, ANTIBODY_CAT_ALT_MAX_LEN, VENDOR_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_TARGET_EPITOPE_MAX_LEN, \
    VENDOR_NIF_MAX_LEN, VENDOR_SYNONYMS_TYPE_MAX_LEN, ANTIBODY_TARGET_SPECIES_MAX_LEN, ANTIBODY_DISC_DATE_MAX_LEN, \
    ANTIBODY_URL_MAX_LEN


class CommercialType(models.TextChoices):
    COMMERCIAL = 'CM', 'commercial'
    PERSONAL = 'PS', 'personal'
    NON_PROFIT = 'NP', 'non-profit'
    OTHER = 'OT', 'other'


class AntibodyClonality(models.TextChoices):
    UNKNOWN = 'UNK', 'Unknown'
    COCKTAIL = 'CKT', 'Cocktail'
    CONTROL = 'CTR', 'Control'
    ISOTYPE_CONTROL = 'I_CTR', 'Isotype Control'
    MONOCLONAL = 'MNC', 'Monoclonal'
    MONOCLONAL_SECONDARY = 'MNC_S', 'Monoclonal Secondary'
    POLYCLONAL = 'PLC', 'Polyclonal'
    POLYCLONAL_SECONDARY = 'PLC_S', 'Polyclonal Secondary'
    OLIGOCLONAL = 'OLC', 'Oligoclonal'
    RECOMBINANT = 'RCB', 'Recombinant'
    RECOMBINANT_MONOCLONAL = 'RCB_M', 'Recombinant Monoclonal'
    RECOMBINANT_MONOCLONAL_SECONDARY = 'RCB_M_S', 'Recombinant Monoclonal Secondary'
    RECOMBINANT_POLYCLONAL = 'RCB_P', 'Recombinant Polyclonal'
    RECOMBINANT_POLYCLONAL_SECONDARY = 'RCB_P_S', 'Recombinant Polyclonal Secondary'


class STATUS(models.TextChoices):
    CURATED = 'C', 'CURATED'
    REJECTED = 'R', 'REJECTED'
    QUEUE = 'Q', 'QUEUE'


class Vendor(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN, db_column='vendor')
    nif_id = models.CharField(max_length=VENDOR_NIF_MAX_LEN, db_column='nif_id')
    commercial_type = models.CharField(
        max_length=VENDOR_COMMERCIAL_TYPE_MAX_LEN,
        choices=CommercialType.choices,
        default=CommercialType.OTHER,
    )
    synonyms = models.CharField(max_length=VENDOR_SYNONYMS_TYPE_MAX_LEN)

    def __str__(self):
        return self.name


class VendorDomain(models.Model):
    base_url = models.URLField(unique=True, null=True, db_column='domain_name')
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
    symbol = models.CharField(unique=True, max_length=ANTIBODY_TARGET_MAX_LEN, db_column='ab_target')
    entrez_id = models.CharField(max_length=ANTIGEN_ENTREZ_ID_MAX_LEN, db_column='ab_target_entrez_gid', null=True)
    uniprot_id = models.CharField(max_length=ANTIGEN_UNIPROT_ID_MAX_LEN, null=True)

    def __str__(self):
        return self.entrez_id

# todo: add model constraints according to https://github.com/MetaCell/scicrunch-antibody-registry/issues/29#issuecomment-1245134405
class Antibody(models.Model):
    ix = models.AutoField(unique=True, null=False, primary_key=True)
    ab_name = models.CharField(max_length=ANTIBODY_NAME_MAX_LEN)
    # todo: ab_id doesn't need to be unique
    ab_id = models.CharField(unique=True, max_length=ANTIBODY_ID_MAX_LEN)
    accession = models.CharField(max_length=ANTIBODY_ID_MAX_LEN)
    # todo: change to foreignKey to user model @afonsobspinto
    uid = models.CharField(max_length=ANTIBODY_ID_MAX_LEN)
    catalog_num = models.CharField(max_length=ANTIBODY_CATALOG_NUMBER_MAX_LEN, null=False)
    cat_alt = models.CharField(max_length=ANTIBODY_CAT_ALT_MAX_LEN)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True)
    url = models.URLField(null=False, max_length=ANTIBODY_URL_MAX_LEN)
    antigen = models.ForeignKey(Antigen, on_delete=models.RESTRICT, db_column='antigen_id')
    species = models.CharField(max_length=ANTIBODY_TARGET_SPECIES_MAX_LEN, db_column='target_species')
    subregion = models.CharField(max_length=ANTIBODY_TARGET_SUBREGION_MAX_LEN, db_column='target_subregion')
    modifications = models.CharField(max_length=ANTIBODY_TARGET_MODIFICATION_MAX_LEN, db_column='target_modification')
    epitope = models.CharField(max_length=ANTIBODY_TARGET_EPITOPE_MAX_LEN)
    source_organism = models.CharField(max_length=ANTIBODY_SOURCE_ORGANISM_MAX_LEN)
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

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['vendor', 'catalog_num'], name='unique_catalog_num_per_vendor')
    #     ]
