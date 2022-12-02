from django.db.models import Q
from import_export.fields import Field
from import_export.instance_loaders import ModelInstanceLoader
from import_export.resources import ModelResource

from api.models import Antibody
from areg_portal.settings import FOR_NEW, IGNORE, FOR_EXTANT, METHOD


class AntibodyInstanceLoaderClass(ModelInstanceLoader):
    def get_instance(self, row):
        try:
            params = {}
            mandatory_id_field = self.resource.get_import_mandatory_id_field()
            params[mandatory_id_field.attribute] = mandatory_id_field.clean(row)
            for field in self.resource.get_import_alternative_id_fields():
                if field.column_name in row:
                    params[field.attribute] = field.clean(row)
            if params:
                return self.get_queryset().get(**params)
            else:
                return None
        except self.resource._meta.model.DoesNotExist:
            return None


class AntibodyResource(ModelResource):
    name = Field(attribute='ab_name', column_name='NAME')
    vendor = Field(attribute='vendor__name', column_name='VENDOR', readonly=True)
    catalog_num = Field(attribute='catalog_num', column_name='base cat')
    url = Field(attribute='url', column_name='URL')
    target = Field(attribute='antigen__symbol', column_name='TARGET', readonly=True)
    species = Field(attribute='species__name', column_name='SPECIES', readonly=True)
    clonality = Field(attribute='clonality', column_name='CLONALITY')
    host = Field(attribute='source_organism__name', column_name='HOST', readonly=True)
    clone_id = Field(attribute='clone_id', column_name='clone')
    product_isotype = Field(attribute='product_isotype', column_name='ISOTYPE')
    product_conjugate = Field(attribute='product_conjugate', column_name='CONJUGATE')
    product_form = Field(attribute='product_form', column_name='FORM')
    comments = Field(attribute='comments', column_name='COMMENTS')
    defining_citation = Field(attribute='defining_citation', column_name='CITATION')
    subregion = Field(attribute='subregion', column_name='SUBREGION')
    modifications = Field(attribute='modifications', column_name='MODIFICATION')
    gid = Field(attribute='antigen__entrez_id', column_name='GID', readonly=True)
    disc_date = Field(attribute='disc_date', column_name='DISC')
    commercial_type = Field(attribute='commercial_type', column_name='TYPE')
    uniprot = Field(attribute='antigen__uniprot_id', column_name='UNIPROT', readonly=True)
    epitope = Field(attribute='epitope', column_name='EPITOPE')
    cat_alt = Field(attribute='cat_alt', column_name='CAT ALT')
    ab_id = Field(attribute='ab_id', column_name='id')
    accession = Field(attribute='accession', column_name='ab_id_old')
    ix = Field(attribute='ix', column_name='ix')

    def __init__(self, request=None):
        super()
        self.request = request

    class Meta:
        model = Antibody
        fields = (
            'name', 'vendor', 'catalog_num', 'url', 'target', 'species', 'clonality', 'host', 'clone_id',
            'product_isotype', 'product_conjugate', 'product_form', 'comments', 'defining_citation', 'subregion',
            'modifications', 'gid', 'disc_date', 'commercial_type', 'uniprot', 'epitope', 'cat_alt', 'ab_id',
            'accession', 'ix')
        import_id_fields = ('id', 'old_id', 'ix')
        instance_loader_class = AntibodyInstanceLoaderClass
        mandatory_id_field = 'ab_id'
        alternative_id_fields = ['accession', 'ix']

    def get_import_mandatory_id_field(self):
        return self.fields[self._meta.mandatory_id_field]

    def get_import_alternative_id_fields(self):
        return [self.fields[f] for f in self._meta.alternative_id_fields]

    def get_instance(self, instance_loader, row):
        # If the mandatory_id_fields is missing we return
        # If all the alternative_id_fields are missing we return
        if self.get_import_mandatory_id_field().column_name not in row or \
                all([field.column_name not in row for field in self.get_import_alternative_id_fields()]):
            return
        return instance_loader.get_instance(row)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # FIXME: The following is a hacky way to have the kwargs from the Import Form to carry on to
        # the Confirm Import Form using django sessions based on:
        # https://stackoverflow.com/questions/52335510/extend-django-import-exports-import-form-to-specify-fixed-value-for-each-import

        # if we are in the confirmation import request we read the values from session and reset the session after
        if kwargs[FOR_NEW] is None:
            kwargs[FOR_NEW] = self.request.session[FOR_NEW]
            kwargs[FOR_EXTANT] = self.request.session[FOR_EXTANT]
            kwargs[METHOD] = self.request.session[METHOD]
            self.request.session[FOR_NEW] = None
            self.request.session[FOR_EXTANT] = None
            self.request.session[METHOD] = None
        else:  # if we are in the import form request we set the values in session using the request values
            self.request.session[FOR_NEW] = kwargs[FOR_NEW]
            self.request.session[FOR_EXTANT] = kwargs[FOR_EXTANT]
            self.request.session[METHOD] = kwargs[METHOD]

        ignore_new = kwargs.get(FOR_NEW, IGNORE) == IGNORE
        if ignore_new:
            mandatory_id_field = self.get_import_mandatory_id_field()
            # If there's no mandatory id field it means all the entries are new
            if mandatory_id_field.column_name not in dataset.headers:
                dataset.df = dataset.df[0:0]
                return

            # if the mandatory id fields exists we need to query database with dataset['id']
            # and remove from dataset the ones that are new
            q = Q(**{"%s__in" % mandatory_id_field.attribute: dataset[mandatory_id_field.column_name]})
            existent_antibodies = [antibody.ab_id for antibody in Antibody.objects.filter(q)]
            # removing the new is equivalent to leaving only the existent

            dataset.df = dataset.df.where(~dataset.df[mandatory_id_field.column_name].isin(existent_antibodies))
            dataset.df = dataset.df.dropna(axis=0, how='all')
