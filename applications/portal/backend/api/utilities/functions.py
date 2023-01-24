from typing import List

magic = 64544
prefix = "AB_"


def generate_id_aux(base: int) -> int:
    return int(base) + magic


def remove_empty_string(str_list) -> List[str]:
    if str_list is None:
        return []
    if type(str_list) is str:
        return [str_list]
    return list(filter(None, set(str_list)))


def strip_ab_from_id(ab_id: str) -> str:
    return ab_id if not ab_id.startswith(prefix) else ab_id.strip(prefix)[1]
