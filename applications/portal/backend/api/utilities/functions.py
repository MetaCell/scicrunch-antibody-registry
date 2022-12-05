from typing import List

magic = 64544


def generate_id_aux(base: int) -> int:
    return base + magic


def remove_empty_string(str_list: List[str]) -> List[str]:
    return list(filter(None, str_list))
