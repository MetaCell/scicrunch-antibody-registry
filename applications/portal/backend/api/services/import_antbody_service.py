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
            dataset[catalog_number_field.column_name])})


def filter_dataset_c1(dataset, negate, antibodies, mandatory_field, alternative_id_fields):
    assert len(alternative_id_fields) == 2
    condition = dataset.df[mandatory_field.column_name].isin(antibodies) & \
                (dataset.df[alternative_id_fields[0].column_name].isin(antibodies) |
                 dataset.df[alternative_id_fields[1].column_name].isin(antibodies))
    return ~condition if negate else condition


def filter_dataset_c2(dataset, negate, antibodies, mandatory_fields):
    assert len(mandatory_fields) == 2
    condition = dataset.df[mandatory_fields[0].column_name].isin(antibodies) & \
                dataset.df[mandatory_fields[1].column_name].isin(antibodies)
    return ~condition if negate else condition
