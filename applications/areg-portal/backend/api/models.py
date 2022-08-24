from django.db import models

from areg_portal.settings import ANTIBODY_ID_MAX_LEN, CATALOG_NUMBER_MAX_LEN, VENDOR_MAX_LEN, \
    ANTIGEN_SPECIES_MAX_LEN, ANTIGEN_ID_MAX_LEN, ANTIGEN_DESCRIPTION_MAX_LEN, ANTIGEN_SUBREGION_MAX_LEN, \
    ANTIGEN_MODIFICATION_MAX_LEN, ANTIGEN_EPITOPE_MAX_LEN, ANTIBODY_SOURCE_ORGANISM_MAX_LEN, ANTIBODY_CLONALITY_MAX_LEN, \
    ANTIBODY_COMMERCIAL_TYPE_MAX_LEN, ANTIBODY_CLONE_ID_MAX_LEN, ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN, \
    ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, ANTIBODY_PRODUCT_FORM_MAX_LEN, ANTIBODY_CITATION_MAX_LEN, \
    ANTIBODY_STATUS_MAX_LEN


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


class CatalogAlternative(models.Model):
    number = models.CharField(max_length=CATALOG_NUMBER_MAX_LEN)

    def __str__(self):
        return self.number


class Catalog(models.Model):
    number = models.CharField(max_length=CATALOG_NUMBER_MAX_LEN, unique=True)
    alternatives = models.ManyToManyField(CatalogAlternative, blank=True)

    def __str__(self):
        return self.number


class Vendor(models.Model):
    name = models.CharField(max_length=VENDOR_MAX_LEN)
    url = models.URLField()

    def __str__(self):
        return self.name


class AntigenSpecie(models.Model):
    name = models.CharField(max_length=ANTIGEN_SPECIES_MAX_LEN)

    def __str__(self):
        return self.name


class AntigenModification(models.Model):
    name = models.CharField(max_length=ANTIGEN_MODIFICATION_MAX_LEN)

    def __str__(self):
        return self.name


class Antigen(models.Model):
    entrez_id = models.CharField(max_length=ANTIGEN_ID_MAX_LEN, unique=True)
    uniprot_id = models.CharField(max_length=ANTIGEN_ID_MAX_LEN, unique=True)
    description = models.CharField(max_length=ANTIGEN_DESCRIPTION_MAX_LEN)
    species = models.ManyToManyField(AntigenSpecie, blank=True)
    subregion = models.CharField(max_length=ANTIGEN_SUBREGION_MAX_LEN, blank=True)
    modifications = models.ManyToManyField(AntigenModification, blank=True)
    epitope = models.CharField(max_length=ANTIGEN_EPITOPE_MAX_LEN, blank=True)

    def __str__(self):
        return self.entrez_id


class Antibody(models.Model):
    uid = models.CharField(max_length=ANTIBODY_ID_MAX_LEN, unique=True, null=False)
    name = models.TextField()
    accession = models.CharField(max_length=ANTIBODY_ID_MAX_LEN)
    commercial_type = models.CharField(
        max_length=ANTIBODY_COMMERCIAL_TYPE_MAX_LEN,
        choices=AntibodyCommercialType.choices,
        default=AntibodyCommercialType.OTHER,
    )
    catalog_id = models.ForeignKey(Catalog, on_delete=models.RESTRICT, null=False)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.RESTRICT, null=False)
    antigen_id = models.ForeignKey(Antigen, on_delete=models.RESTRICT, null=False)
    source_organism = models.CharField(max_length=ANTIBODY_SOURCE_ORGANISM_MAX_LEN)
    clonality = models.CharField(
        max_length=ANTIBODY_CLONALITY_MAX_LEN,
        choices=AntibodyClonality.choices,
        default=AntibodyClonality.UNKNOWN,
    )
    clone_id = models.CharField(max_length=ANTIBODY_CLONE_ID_MAX_LEN, blank=True)
    isotype = models.CharField(
        max_length=ANTIBODY_PRODUCT_ISOTYPE_MAX_LEN,
        choices=ProductIsotype.choices,
        blank=True
    )
    conjugate = models.CharField(max_length=ANTIBODY_PRODUCT_CONJUGATE_MAX_LEN, blank=True)
    form = models.CharField(
        max_length=ANTIBODY_PRODUCT_FORM_MAX_LEN,
        choices=ProductForm.choices,
        blank=True
    )
    citation = models.CharField(max_length=ANTIBODY_CITATION_MAX_LEN, null=False)
    disc_date = models.DateTimeField(null=True, blank=True)

    comments = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    curator_comment = models.TextField(blank=True)

    status = models.CharField(
        max_length=ANTIBODY_STATUS_MAX_LEN,
        choices=STATUS.choices,
        default=STATUS.QUEUE
    )

    date_modified = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid
