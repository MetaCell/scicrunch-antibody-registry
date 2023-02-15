from typing import Callable

from import_export.fields import Field
from import_export.instance_loaders import ModelInstanceLoader
from import_export.resources import ModelResource

from api.models import Antibody, Vendor, Antigen, Specie, STATUS
from api.services.gene_service import get_or_create_gene
from api.services.import_antbody_service import filter_dataset_c1, filter_dataset_c2, get_antibody_q1, get_antibody_q2
from api.services.keycloak_service import KeycloakService
from api.services.specie_service import get_or_create_specie
from api.services.vendor_service import get_or_create_vendor
from api.widgets.foreign_key_widget import ForeignKeyWidgetWithCreation
from api.widgets.many_to_many_widget import ManyToManyWidgetWithCreation
from portal.settings import FOR_NEW_KEY, IGNORE_KEY, FOR_EXTANT_KEY, METHOD_KEY, FILL_KEY, UPDATE_KEY, \
    DUPLICATE_KEY, KC_USER_ID_KEY, USER_KEY


class AntibodyIdentifier:
    def __init__(self, fields, condition: Callable, q: Callable, filter_dataset: Callable):
        self.fields = fields
        self.condition = condition
        self.q = q
        self.filter_dataset = filter_dataset


class AntibodyInstanceLoaderClass(ModelInstanceLoader):
    def get_instance(self, q):
        instances = self.get_queryset().filter(q).order_by('insert_time')
        return instances[0] if len(instances) > 0 else None


class AntibodyResource(ModelResource):
    name = Field(attribute='ab_name', column_name='NAME')
    vendor = Field(
        column_name='VENDOR',
        attribute='vendor',
        widget=ForeignKeyWidgetWithCreation(model=Vendor, field='name',
                                            get_or_create=lambda **kwargs: get_or_create_vendor(**kwargs)[0])
    )
    catalog_num = Field(attribute='catalog_num', column_name='base cat')
    url = Field(attribute='url', column_name='URL')
    target = Field(
        column_name='TARGET',
        attribute='antigen',
        widget=ForeignKeyWidgetWithCreation(model=Antigen, field='symbol',
                                            get_or_create=lambda **kwargs: get_or_create_gene(**kwargs)[
                                                0],
                                            other_cols_map={'GID': 'entrez_id', 'UNIPROT': 'uniprot_id'})
    )
    species = Field(
        column_name='SPECIES',
        attribute='species',
        widget=ManyToManyWidgetWithCreation(model=Specie, separator=';', field='name',
                                            get_or_create=lambda **kwargs: get_or_create_specie(**kwargs)[0])
    )
    clonality = Field(attribute='clonality', column_name='CLONALITY')
    host = Field(
        column_name='HOST',
        attribute='source_organism',
        widget=ForeignKeyWidgetWithCreation(model=Specie, field='name',
                                            get_or_create=lambda **kwargs: get_or_create_specie(**kwargs)[0])
    )
    clone_id = Field(attribute='clone_id', column_name='clone')
    product_isotype = Field(attribute='product_isotype', column_name='ISOTYPE')
    product_conjugate = Field(
        attribute='product_conjugate', column_name='CONJUGATE')
    product_form = Field(attribute='product_form', column_name='FORM')
    comments = Field(attribute='comments', column_name='COMMENTS')
    defining_citation = Field(
        attribute='defining_citation', column_name='CITATION')
    subregion = Field(attribute='subregion', column_name='SUBREGION')
    modifications = Field(attribute='modifications',
                          column_name='MODIFICATION')
    disc_date = Field(attribute='disc_date', column_name='DISC')
    commercial_type = Field(attribute='commercial_type', column_name='TYPE')
    epitope = Field(attribute='epitope', column_name='EPITOPE')
    cat_alt = Field(attribute='cat_alt', column_name='CAT ALT')
    ab_id = Field(attribute='ab_id', column_name='id')
    accession = Field(attribute='accession', column_name='ab_id_old')
    ix = Field(attribute='ix', column_name='ix')

    def __init__(self, request=None):
        super()
        super().__init__()
        self.antibody_identifiers = [
            AntibodyIdentifier(
                [self.fields['ab_id'], self.fields['ix'], self.fields['accession']],
                lambda row: self.fields['ab_id'].column_name in row and (
                        self.fields['ix'].column_name in row or self.fields['accession'].column_name in row),
                lambda dataset: get_antibody_q1(dataset, self.fields['ab_id'],
                                                [self.fields['ix'], self.fields['accession']]),
                lambda dataset, negate, antibodies: filter_dataset_c1(dataset, negate, antibodies, self.fields['ab_id'],
                                                                      self.fields['ix'], self.fields['accession'])
            ),
            AntibodyIdentifier(
                [self.fields['vendor'], self.fields['catalog_num']],
                lambda row: self.fields['vendor'].column_name in row and self.fields['catalog_num'].column_name in row,
                lambda dataset: get_antibody_q2(
                    dataset, self.fields['catalog_num'], self.fields['vendor']),
                lambda dataset, negate, antibodies: filter_dataset_c2(dataset, negate, antibodies,
                                                                      self.fields['catalog_num'],
                                                                      self.fields['vendor'])
            )
        ]
        self.keycloak_service = KeycloakService()
        self.request = request

    class Meta:
        model = Antibody
        fields = (
            'name', 'vendor', 'catalog_num', 'url', 'target', 'species', 'clonality', 'host', 'clone_id',
            'product_isotype', 'product_conjugate', 'product_form', 'comments', 'defining_citation', 'subregion',
            'modifications', 'gid', 'disc_date', 'commercial_type', 'uniprot', 'epitope', 'cat_alt', 'ab_id',
            'accession', 'ix')
        instance_loader_class = AntibodyInstanceLoaderClass

    def get_antibody_identifier(self, row):
        for antibody_identifier in self.antibody_identifiers:
            if antibody_identifier.condition(row):
                return antibody_identifier
        return None

    def get_or_init_instance(self, instance_loader, row):
        """
        Either fetches an already existing instance or initializes a new one.
        """
        create_duplicate = self.request.session.get(
            FOR_EXTANT_KEY, UPDATE_KEY) == DUPLICATE_KEY

        if not self._meta.force_init_instance:
            instance = self.get_instance(instance_loader, row)
            if instance:
                if not create_duplicate:
                    return (instance, False)
                row[self.fields['accession'].column_name] = instance.ab_id
                # if self.fields['ab_id'].column_name in row:
                #     del row[self.fields['ab_id'].column_name]
                if self.fields['ix'].column_name in row:
                    del row[self.fields['ix'].column_name]
        instance = self.init_instance(row)
        instance.status = STATUS.CURATED
        if 'uid' in row:
            instance.uid = row['uid']
        return instance, True

    def get_instance(self, instance_loader, row):
        antibody_identifier = self.get_antibody_identifier(row)
        return instance_loader.get_instance(antibody_identifier.q(row)) if antibody_identifier else None

    def import_data_inner(self, dataset, dry_run, raise_errors, using_transactions,
                          collect_failed_rows, rollback_on_validation_errors=False, **kwargs):
        # The following is a hacky way to have the kwargs from the Import Form to carry on to
        # the Confirm Import Form using django sessions based on:
        # https://stackoverflow.com/questions/52335510/extend-django-import-exports-import-form-to-specify-fixed-value-for-each-import

        # if we are in the confirmation import request we read the values from session
        # and get the keycloak user id from the keycloak_service
        if kwargs[FOR_NEW_KEY] is None:
            kwargs[FOR_NEW_KEY] = self.request.session[FOR_NEW_KEY]
            kwargs[FOR_EXTANT_KEY] = self.request.session[FOR_EXTANT_KEY]
            kwargs[METHOD_KEY] = self.request.session[METHOD_KEY]

            kwargs[KC_USER_ID_KEY] = self.keycloak_service.get_user_id_from_django_user(kwargs[USER_KEY])

        else:  # if we are in the import form request we set the values in session using the request values
            self.request.session[FOR_NEW_KEY] = kwargs[FOR_NEW_KEY]
            self.request.session[FOR_EXTANT_KEY] = kwargs[FOR_EXTANT_KEY]
            self.request.session[METHOD_KEY] = kwargs[METHOD_KEY]

        return super().import_data_inner(dataset, dry_run, raise_errors, using_transactions, collect_failed_rows,
                                         rollback_on_validation_errors, **kwargs)

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        ignore_new = kwargs.get(FOR_NEW_KEY, IGNORE_KEY) == IGNORE_KEY
        ignore_update = kwargs.get(FOR_EXTANT_KEY, IGNORE_KEY) == IGNORE_KEY
        if ignore_new:
            # if new entries are not meant to be considered
            # we need keep the existing entries only
            self._filter_dataset(dataset, False)
        if ignore_update:
            # we need to remove existing entries
            self._filter_dataset(dataset, True)
            # BOTH
            # if both new entries and current entries are to be considered then all the dataset is relevant
        # removes empty nan line when the full dataset is removed
        dataset.df = dataset.df.dropna(axis=0, how='all')

    def _filter_dataset(self, dataset, negate_filter_condition=False):
        ic = self.get_antibody_identifier(dataset.headers)
        if ic is None:
            return
        existent_antibodies = Antibody.objects.filter(ic.q(dataset))
        dataset.df = dataset.df.where(ic.filter_dataset(
            dataset, negate_filter_condition, existent_antibodies))

    def before_import_row(self, row, row_number=None, **kwargs):
        antibody_identifier = self.get_antibody_identifier(row)
        # modify empty strings to none on identifier columns
        create_duplicate = self.request.session.get(FOR_EXTANT_KEY, UPDATE_KEY) == DUPLICATE_KEY
        for field in antibody_identifier.fields:
            # Exceptionally on the create_duplicate option we retain the ab_id
            if field.attribute == 'ab_id' and create_duplicate:
                continue
            if field.column_name in row:
                if row[field.column_name] == '':
                    row[field.column_name] = None
        if KC_USER_ID_KEY in kwargs:
            row['uid'] = kwargs[KC_USER_ID_KEY]

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        is_fill = kwargs.get(METHOD_KEY, FILL_KEY) == FILL_KEY
        if field.attribute and (field.column_name in data):
            # If we are only updating the filled columns and the column is empty we do nothing
            if is_fill and data[field.column_name] == '':
                return
            # Otherwise we save the field
            field.save(obj, data, is_m2m, **kwargs)
