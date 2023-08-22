from typing import Callable
from api.repositories.maintainance import refresh_search_view

from import_export.fields import Field
from import_export.instance_loaders import ModelInstanceLoader
from import_export.resources import ModelResource

from api.models import Antibody, AntibodyClonality, CommercialType, Vendor, Specie, STATUS
from api.services.gene_service import get_or_create_gene
from api.import_export.import_antibody_helpers import filter_dataset_by_accession, filter_dataset_by_catnum_vendor, filter_dataset_by_ix, get_antibody_q1, get_antibody_q2
from api.services.keycloak_service import KeycloakService
from api.services.specie_service import get_or_create_specie
from api.services.vendor_service import get_or_create_vendor
from .widgets.foreign_key_widget import ForeignKeyWidgetWithCreation
from .widgets.many_to_many_widget import ManyToManyWidgetWithCreation
from portal.settings import FOR_NEW_KEY, IGNORE_KEY, FOR_EXTANT_KEY, METHOD_KEY, FILL_KEY, UPDATE_KEY, \
    DUPLICATE_KEY, KC_USER_ID_KEY, USER_KEY, REMOVE_KEYWORD

from cloudharness import log

CLONALITIES = {c[0] for c in AntibodyClonality.choices}
COMMERCIAL_TYPES = {c[0] for c in CommercialType.choices}

class AntibodyIdentifier:
    def __init__(self, fields, condition: Callable, q: Callable, filter_dataset: Callable):
        """
        :param fields: list of fields that are used to identify the antibody
        :param condition: function that returns true if the identifier is activated
        :param q: how to filter objects in the existing database: returns a Q object
        :param filter_dataset: function that filters the dataset to be ingested (the data from the csv file). The mask to the pandas dataframe is returned
        """
        self.fields = fields
        self.condition = condition
        self.q = q
        self.filter_dataset = filter_dataset


class AntibodyInstanceLoaderClass(ModelInstanceLoader):
    def get_instance(self, q):
        instances = self.get_queryset().filter(q).order_by('insert_time')
        return instances[0] if len(instances) > 0 else None


class AntibodyResource(ModelResource):
    name = Field(attribute='ab_name', column_name='ab_name')
    vendor = Field(
        column_name='vendor',
        attribute='vendor',
        widget=ForeignKeyWidgetWithCreation(model=Vendor, field='name',
                                            get_or_create=lambda **kwargs: get_or_create_vendor(**kwargs)[0])
    )
    catalog_num = Field(attribute='catalog_num', column_name='catalog_num')
    url = Field(attribute='url', column_name='url')
    link = Field(column_name='link')
    target = Field(
        column_name='ab_target',
        attribute='ab_target'
    )

    species = Field(
        column_name='target_species',
        attribute='target_species_raw'
    )
    clonality = Field(attribute='clonality', column_name='clonality')
    host = Field(
        column_name='source_organism',
        attribute='source_organism',
        widget=ForeignKeyWidgetWithCreation(model=Specie, field='name',
                                            get_or_create=lambda **kwargs: get_or_create_specie(**kwargs)[0])
    )
    clone_id = Field(attribute='clone_id', column_name='clone_id')
    product_isotype = Field(attribute='product_isotype',
                            column_name='product_isotype')
    product_conjugate = Field(
        attribute='product_conjugate', column_name='product_conjugate')
    product_form = Field(attribute='product_form', column_name='product_form')
    comments = Field(attribute='comments', column_name='comments')
    defining_citation = Field(
        attribute='defining_citation', column_name='defining_citation')
    subregion = Field(attribute='subregion', column_name='target_subregion')
    modifications = Field(attribute='modifications',
                          column_name='target_modification')
    gene_id = Field(attribute='entrez_id', column_name='ab_target_entrez_gid')
    disc_date = Field(attribute='disc_date', column_name='disc_date')
    commercial_type = Field(attribute='commercial_type',
                            column_name='commercial_type')
    uniprot = Field(attribute='uniprot_id', column_name='uniprot_id')
    epitope = Field(attribute='epitope', column_name='epitope')
    cat_alt = Field(attribute='cat_alt', column_name='cat_alt')
    ab_id = Field(attribute='ab_id', column_name='ab_id')
    accession = Field(attribute='accession', column_name='ab_id_old')
    ix = Field(attribute='ix', column_name='ix')

    def __init__(self, request=None):
        super()
        super().__init__()
        self.antibody_identifiers = [
            AntibodyIdentifier(
                [self.fields['ix']],
                lambda row: self.fields['ix'].column_name in row,
                lambda dataset: get_antibody_q1(dataset, self.fields['ix']),
                lambda dataset, negate, antibodies: filter_dataset_by_ix(
                    dataset, negate, antibodies)
            ),
            AntibodyIdentifier(
                [self.fields['accession']],
                lambda row: self.fields['accession'].column_name in row,
                lambda dataset: get_antibody_q1(
                    dataset, self.fields['accession']),
                lambda dataset, negate, antibodies: filter_dataset_by_accession(
                    dataset, negate, antibodies)
            ),
            AntibodyIdentifier(
                [self.fields['vendor'], self.fields['catalog_num']],
                lambda row: self.fields['vendor'].column_name in row and self.fields['catalog_num'].column_name in row,
                lambda dataset: get_antibody_q2(
                    dataset, self.fields['catalog_num'], self.fields['vendor']),
                lambda dataset, negate, antibodies: filter_dataset_by_catnum_vendor(dataset, negate, antibodies,
                                                                                    self.fields['catalog_num'],
                                                                                    self.fields['vendor'])
            )
        ]
        self.request = request

    class Meta:
        model = Antibody
        fields = (
            'name', 'vendor', 'catalog_num', 'url', 'link', 'target', 'species', 'clonality', 'host', 'clone_id',
            'product_isotype', 'product_conjugate', 'product_form', 'comments', 'defining_citation', 'subregion',
            'modifications', 'gene_id', 'disc_date', 'commercial_type', 'epitope', 'cat_alt', 'ab_id',
            'accession', 'ix')
        instance_loader_class = AntibodyInstanceLoaderClass

    def get_antibody_identifier(self, row):
        for antibody_identifier in self.antibody_identifiers:
            if antibody_identifier.condition(row):
                return antibody_identifier
        return None

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        """
        Takes care of saving the object to the database.

        Objects can be created in bulk if ``use_bulk`` is enabled.

        :param instance: The instance of the object to be persisted.
        :param is_create: A boolean flag to indicate whether this is a new object
        to be created, or an existing object to be updated.
        :param using_transactions: A flag to indicate whether db transactions are used.
        :param dry_run: A flag to indicate dry-run mode.
        """
        self.before_save_instance(instance, using_transactions, dry_run)
        if self._meta.use_bulk:
            if is_create:
                self.create_instances.append(instance)
            else:
                self.update_instances.append(instance)
        else:
            if not using_transactions and dry_run:
                # we don't have transactions and we want to do a dry_run
                pass
            else:
                instance.save(update_search=False)
        self.after_save_instance(instance, using_transactions, dry_run)

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        super().after_import(dataset, result, using_transactions, dry_run, **kwargs)
        refresh_search_view()

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
            try:
                kwargs[KC_USER_ID_KEY] = KeycloakService(
                ).get_user_id_from_django_user(kwargs[USER_KEY])
            except Exception as e:
                log.exception("Cannot set user id for import")
                kwargs[KC_USER_ID_KEY] = None

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
        antibody_identifier = self.get_antibody_identifier(dataset.headers)
        if antibody_identifier is None:
            return
        existent_antibodies = Antibody.objects.filter(
            antibody_identifier.q(dataset))
        dataset.df = dataset.df.where(
            antibody_identifier.filter_dataset(
                dataset, negate_filter_condition, existent_antibodies)
        )

    def before_import_row(self, row, row_number=None, **kwargs):
        antibody_identifier = self.get_antibody_identifier(row)
        # modify empty strings to none on identifier columns
        create_duplicate = self.request.session.get(
            FOR_EXTANT_KEY, UPDATE_KEY) == DUPLICATE_KEY
        if antibody_identifier:
            for field in antibody_identifier.fields:
                # Exceptionally on the create_duplicate option we retain the ab_id
                if field.attribute == 'ab_id' and create_duplicate:
                    continue
                elif field.attribute == 'ab_id' or field.attribute == "ab_id_old":
                    row[field.column_name] = row[field.column_name].replace(
                        "AB_", "")

        for column_name in row:
            if row[column_name] == '':
                row[column_name] = None

        if row.get('link', None):
            row['link'] = 'y' in row['link'].lower()
        else:
            row['link'] = True
        if row.get('clonality', None):
            clonality = row['clonality'].lower()
            
            row['clonality'] = clonality if clonality in CLONALITIES else None
            
        if row.get('commercial_type', None):
            commercial_type = row['commercial_type'].lower()
            row['commercial_type'] = commercial_type if commercial_type in COMMERCIAL_TYPES else None
        if row.get('species', None):
            row['species'] = row['species'].lower().replace(",", ";")
        if row.get('host_organism', None):
            row['host_organism'] = row['host_organism'].lower()

        if KC_USER_ID_KEY in kwargs:
            row['uid'] = kwargs[KC_USER_ID_KEY]

    def import_field(self, field, obj, data, is_m2m=False, **kwargs):
        is_fill = kwargs.get(METHOD_KEY, FILL_KEY) == FILL_KEY
        if field.attribute and (field.column_name in data):
            if is_fill:
                # If we are only updating the filled columns and the column is empty we do nothing
                if data[field.column_name] == '' or data[field.column_name] is None:
                    return
                if data[field.column_name] == REMOVE_KEYWORD:
                    data[field.column_name] = None
            # Otherwise we save the field
            field.save(obj, data, is_m2m, **kwargs)
