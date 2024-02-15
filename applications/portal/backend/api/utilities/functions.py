from typing import List, Union
import re
from urllib.parse import urlsplit

from django.db.models import AutoField
from django.forms import URLField

from portal.settings import ANTIBODY_PERSISTENCE

magic = 64544
prefix = "AB_"


def generate_id_aux(base: Union[int, AutoField]) -> int:
    return int(base) + magic


def remove_empty_string(str_list) -> List[str]:
    if str_list is None:
        return []
    if type(str_list) is str:
        return [str_list]
    return list(filter(None, set(str_list)))


def strip_ab_from_id(ab_id: str) -> str:
    return ab_id if not ab_id.startswith(prefix) else ab_id.strip(prefix)


def extract_base_url(url: Union[str, URLField]) -> str:
    return urlsplit(url).hostname


def get_antibody_persistence_directory(ab_id: str, filename: str) -> str:
    return f'{ANTIBODY_PERSISTENCE}/{ab_id}/{filename}'

def get_catalog_number_digits(catalog_number: str) -> List[str]:
    return [c for c in re.split(r'(\d+)',re.sub(r'[^\w]', '', catalog_number)) if c]


def get_catalog_non_alphanumeric(catalog_number: str) -> List[str]:
    split_by_non_alphanumeric_array = [c for c in re.split(r'\W+', catalog_number) if c]
    alphanumeric_catalogs = []
    for c in split_by_non_alphanumeric_array:
        alphanumeric_catalogs.extend(get_catalog_number_digits(c))
    return alphanumeric_catalogs

def catalog_number_chunked(catalog_number: str, catalog_alt_number: str=None, fill=' ') -> List[str]:
    if not catalog_number and not catalog_alt_number:
        return ""
    try:
        cat_split_by_digits = get_catalog_number_digits(catalog_number)
        cat_split_by_non_alphanumeric = get_catalog_non_alphanumeric(catalog_number)

        cat_alt_split_by_digits = get_catalog_number_digits(catalog_alt_number) if catalog_alt_number else []
        cat_alt_split_by_non_alphanumeric = get_catalog_non_alphanumeric(catalog_alt_number) if catalog_alt_number else []


        joined_catalog_chunk = fill.join(set(cat_split_by_digits + cat_split_by_non_alphanumeric + cat_alt_split_by_digits + cat_alt_split_by_non_alphanumeric))
        
        return joined_catalog_chunk.strip().lower()
    except Exception as e:
        return ""
