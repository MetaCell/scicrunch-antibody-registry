from typing import List

magic = 64544


def generate_id_aux(base: int) -> int:
    return int(base) + magic


def remove_empty_string(str_list) -> List[str]:
    if str_list is None:
        return []
    if type(str_list) is str:
        return [str_list]
    return list(filter(None, set(str_list)))
