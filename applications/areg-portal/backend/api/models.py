from django.core.validators import MinLengthValidator
from django.db import models

from areg_portal.settings import ANTIBODY_ID_MAX_LEN, CATALOG_NUMBER_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIGEN_ID_MAX_LEN, ANTIGEN_DESCRIPTION_MAX_LEN, ANTIGEN_SUBREGION_MAX_LEN, \
    ANTIGEN_EPITOPE_MAX_LEN, ANTIBODY_SOURCE_ORGANISM_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_CLONE_ID_MAX_LEN, ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, \
    ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, ANTIBODY_CITATION_MAX_LEN, \
    ANTIBODY_STATUS_MAX_LEN, ANTIBODY_UID_MAX_LEN


class AntibodyCommercialType(models.TextChoices):
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


class ProductIsotype(models.TextChoices):
    IGG = 'IGG', 'IgG'
    IGG1 = 'IGG1', 'IgG1'
    IGG2 = 'IGG2', 'IgG2'
    IGG3 = 'IGG3', 'IgG3'
    IGG4 = 'IGG4', 'IgG4'
    IGY = 'IGY', 'IgY'
    IGA = 'IGA', 'IgA'
    IGM = 'IGM', 'IgM'


class ProductForm(models.TextChoices):
    LYOPHILIZED = 'LP', 'Lyophilized'
    AFFINITY_PURIFIED = 'AP', 'Affinity Purified'
    LIQUID = 'LQ', 'LIQUID'


class STATUS(models.TextChoices):
    CURATED = 'C', 'Curated'
    REJECTED = 'R', 'Rejected'
    QUEUE = 'Q', 'QUEUE'


class Vendor(models.Model):
    id = models.AutoField(db_column='vendor_id', null=False, primary_key=True)
    name = models.CharField(max_length=VENDOR_MAX_LEN, db_column='vendor')

    def __str__(self):
        return self.name


class Antigen(models.Model):
    symbol = models.CharField(unique=True, max_length=ANTIGEN_DESCRIPTION_MAX_LEN, db_column='ab_target')
    species = models.TextField(db_column='target_species')
    entrez_id = models.CharField(unique=True, max_length=ANTIGEN_ID_MAX_LEN, db_column='ab_target_entrez_gid')
    subregion = models.CharField(max_length=ANTIGEN_SUBREGION_MAX_LEN, db_column='target_subregion')
    modifications = models.TextField(db_column='target_modification')
    epitope = models.CharField(max_length=ANTIGEN_EPITOPE_MAX_LEN)
    uniprot_id = models.CharField(unique=True, max_length=ANTIGEN_ID_MAX_LEN)

    def __str__(self):
        return self.entrez_id


class Antibody(models.Model):
    ab_name = models.TextField()
    ab_id = models.CharField(unique=True, max_length=ANTIBODY_ID_MAX_LEN, validators=[MinLengthValidator(1)])
    accession = models.CharField(max_length=ANTIBODY_ID_MAX_LEN, validators=[MinLengthValidator(1)])
    ix = models.AutoField(unique=True, null=False, primary_key=True)
    uid = models.CharField(unique=True, max_length=ANTIBODY_UID_MAX_LEN, validators=[MinLengthValidator(1)])
    commercial_type = models.CharField(
        max_length=ANTIBODY_COMMERCIAL_TYPE_MAX_LEN,
        choices=AntibodyCommercialType.choices,
        default=AntibodyCommercialType.OTHER,
    )
    catalog_num = models.CharField(max_length=CATALOG_NUMBER_MAX_LEN, null=False)
    cat_alt = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=True)
    url = models.URLField(null=False)
    antigen = models.ForeignKey(Antigen, on_delete=models.RESTRICT)
    source_organism = models.CharField(max_length=ANTIBODY_SOURCE_ORGANISM_MAX_LEN)
    clonality = models.CharField(
        max_length=ANTIBODY_CLONALITY_MAX_LEN,
        choices=AntibodyClonality.choices,
        default=AntibodyClonality.UNKNOWN,
    )
    clone_id = models.CharField(max_length=ANTIBODY_CLONE_ID_MAX_LEN)
    # todo: can be multiple choices
    product_isotype = models.CharField(
        max_length=ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN,
        choices=ProductIsotype.choices,
    )
    product_conjugate = models.CharField(max_length=ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN)
    defining_citation = models.CharField(max_length=ANTIBODY_CITATION_MAX_LEN)
    product_form = models.CharField(
        max_length=ANTIBODY_PRODUCT_FORM_MAX_LEN,
        choices=ProductForm.choices,
    )
    comments = models.TextField()
    feedback = models.TextField()
    curator_comment = models.TextField()
    disc_date = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=ANTIBODY_STATUS_MAX_LEN,
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
