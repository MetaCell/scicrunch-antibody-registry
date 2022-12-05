from django.db.models import Q
from import_export.fields import Field
from import_export.instance_loaders import ModelInstanceLoader
from import_export.resources import ModelResource

from api.models import Antibody
from areg_portal.settings import FOR_NEW_KEY, IGNORE_KEY, FOR_EXTANT_KEY, METHOD_KEY


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
        if kwargs[FOR_NEW_KEY] is None:
            kwargs[FOR_NEW_KEY] = self.request.session[FOR_NEW_KEY]
            kwargs[FOR_EXTANT_KEY] = self.request.session[FOR_EXTANT_KEY]
            kwargs[METHOD_KEY] = self.request.session[METHOD_KEY]
            self.request.session[FOR_NEW_KEY] = None
            self.request.session[FOR_EXTANT_KEY] = None
            self.request.session[METHOD_KEY] = None
        else:  # if we are in the import form request we set the values in session using the request values
            self.request.session[FOR_NEW_KEY] = kwargs[FOR_NEW_KEY]
            self.request.session[FOR_EXTANT_KEY] = kwargs[FOR_EXTANT_KEY]
            self.request.session[METHOD_KEY] = kwargs[METHOD_KEY]

        ignore_new = kwargs.get(FOR_NEW_KEY, IGNORE_KEY) == IGNORE_KEY
        ignore_update = kwargs.get(FOR_EXTANT_KEY, IGNORE_KEY) == IGNORE_KEY
        mandatory_id_field = self.get_import_mandatory_id_field()

        if ignore_new:
            # If there's no mandatory id field it means all the entries are new
            # If ignore_update is also selected there's no entry to be considered
            if mandatory_id_field.column_name not in dataset.headers or ignore_update:
                dataset.df = dataset.df[0:0]
                return
            # if new entries are not meant to be considered but update ones are not
            # we need keep the existing entries only
            existent_antibodies = self._get_existent_antibodies(dataset)
            dataset.df = dataset.df.where(dataset.df[mandatory_id_field.column_name].isin(existent_antibodies))
        else:
            # if new entries are meant to be considered but update ones are not
            # we need to remove existing entries
            if ignore_update:
                existent_antibodies = self._get_existent_antibodies(dataset)
                dataset.df = dataset.df.where(~dataset.df[mandatory_id_field.column_name].isin(existent_antibodies))
            # if both options are active we ignore entries with ab_id + other that do not exist in the db
            else:
                # we need to check if the dataset has the id columns (required for update)
                if mandatory_id_field.column_name not in dataset.headers:
                    return
                new_antibodies_with_ids = self._get_new_antibodies_with_id_references(dataset)
                dataset.df = dataset.df.where(~dataset.df[mandatory_id_field.column_name].isin(new_antibodies_with_ids))
        # removes empty nan line when the full dataset is removed
        dataset.df = dataset.df.dropna(axis=0, how='all')

    def _get_existent_antibodies(self, dataset):
        mandatory_id_field = self.get_import_mandatory_id_field()
        q = Q(**{"%s__in" % mandatory_id_field.attribute: dataset[mandatory_id_field.column_name]})
        alternative_q = Q()
        for field in self.get_import_alternative_id_fields():
            if field.column_name in dataset.headers:
                alternative_q.add(Q(**{"%s__in" % field.attribute: dataset[field.column_name]}), Q.OR)
        q.add(alternative_q, Q.OR)
        return [antibody.ab_id for antibody in Antibody.objects.filter(q)]

    def _get_new_antibodies_with_id_references(self, dataset):
        mandatory_id_field = self.get_import_mandatory_id_field()
        existent_antibodies = self._get_existent_antibodies(dataset)
        # trick to remove empty string from the results
        existent_antibodies.append('')
        return set(dataset[mandatory_id_field.column_name]) - set(existent_antibodies)

    def before_import_row(self, row, row_number=None, **kwargs):
        mandatory_id_field = self.get_import_mandatory_id_field()
        if mandatory_id_field.column_name in row:
            if row[mandatory_id_field.column_name] == '':
                row[mandatory_id_field.column_name] = None
        for field in self.get_import_alternative_id_fields():
            if field.column_name in row:
                if row[field.column_name] == '':
                    row[field.column_name] = None
