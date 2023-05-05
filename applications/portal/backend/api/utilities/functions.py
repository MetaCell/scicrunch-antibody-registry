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
    return ab_id if not ab_id.startswith(prefix) else ab_id.strip(prefix)[1]


def extract_base_url(url: Union[str, URLField]) -> str:
    return urlsplit(url).hostname


def get_antibody_persistence_directory(ab_id: str, filename: str) -> str:
    return f'{ANTIBODY_PERSISTENCE}/{ab_id}/{filename}'

def catalog_number_chunked(catalog_number: str, fill=' ') -> List[str]:
    if not catalog_number:
        return ""
    try:
        return fill.join(c for c in re.split(r'(\d+)',re.sub(r'[^\w]', '', catalog_number)) if c).strip().lower()
    except Exception as e:
        return ""