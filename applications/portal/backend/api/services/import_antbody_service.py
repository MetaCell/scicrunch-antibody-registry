from collections import OrderedDict

from django.db.models import Q

from api.utilities.functions import remove_empty_string


def get_antibody_q1(dataset, mandatory_id_field, alternative_id_fields) -> Q:
    q = Q(
        **{"%s__in" % mandatory_id_field.attribute: remove_empty_string(dataset[mandatory_id_field.column_name])})

    alternative_q = Q()
    for field in alternative_id_fields:
        if _exists_column(field.column_name, dataset):
            alternative_q.add(Q(**{"%s__in" % field.attribute: remove_empty_string(dataset[field.column_name])}),
                              Q.OR)
    q.add(alternative_q, Q.AND)
    return q


def _exists_column(name: str, dataset):
    if type(dataset) is OrderedDict:
        return name in dataset.keys()
    return name in dataset.headers


def get_antibody_q2(dataset, catalog_number_field, vendor_field) -> Q:
    return Q(**{"%s__in" % catalog_number_field.attribute: remove_empty_string(
        dataset[catalog_number_field.column_name])}) & Q(
        **{"%s__%s__in" % (vendor_field.attribute, vendor_field.widget.field): remove_empty_string(
            dataset[vendor_field.column_name])})


def filter_dataset_c1(dataset, negate, antibodies, ab_id_field, ix_field, accession_field):
    antibody_ids = []
    antibody_ixs = []
    antibody_accessions = []
    for antibody in antibodies:
        antibody_ids.append(antibody.ab_id)
        antibody_ixs.append(str(antibody.ix))
        antibody_accessions.append(str(antibody.accession))
    base_condition = dataset.df[ab_id_field.column_name].isin(antibody_ids)
    if ix_field.column_name in dataset.df:
        condition = base_condition & dataset.df[ix_field.column_name].isin(antibody_ixs)
    else:
        condition = base_condition & dataset.df[accession_field.column_name].isin(antibody_accessions)
    return ~condition if negate else condition


def filter_dataset_c2(dataset, negate, antibodies, catalog_number_field, vendor_field):
    antibody_catalog_numbers = []
    antibody_vendor_names = []
    for antibody in antibodies:
        antibody_catalog_numbers.append(antibody.catalog_number)
        antibody_vendor_names.append(antibody.vendor.name)
    condition = dataset.df[catalog_number_field.column_name].isin(antibody_catalog_numbers) & \
                dataset.df[vendor_field.column_name].isin(antibody_vendor_names)
    return ~condition if negate else condition
