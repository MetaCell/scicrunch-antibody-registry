import re
from api.services.user_service import get_current_user_id


def to_snake(camel_str: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()


def to_camel(snake_str):
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def dict_to_snake(d):
    return {to_snake(k): v for k, v in d.items()}


def dict_to_camel(d):
    return {to_camel(k): v for k, v in d.items()}


if __name__ == '__main__':
    from pprint import pprint

    pprint(dict_to_snake({
        "clonality": "Unknown",
        "epitope": "string",
        "comments": "string",
        "url": "string",
        "abName": "string",
        "abTarget": "string",
        "catalogNum": "string",
        "cloneId": "string",
        "commercialType": "commercial",
        "definingCitation": "string",
        "productConjugate": "string",
        "productForm": "Lyophilized",
        "productIsotype": "string",
        "sourceOrganism": "string",
        "targetSpecies": "string",
        "uniprotId": "string",
        "vendorName": "string"
    }))

    pprint(dict_to_camel(dict_to_snake({
        "clonality": "Unknown",
        "epitope": "string",
        "comments": "string",
        "url": "string",
        "abName": "string",
        "abTarget": "string",
        "catalogNum": "string",
        "cloneId": "string",
        "commercialType": "commercial",
        "definingCitation": "string",
        "productConjugate": "string",
        "productForm": "Lyophilized",
        "productIsotype": "string",
        "sourceOrganism": "string",
        "targetSpecies": "string",
        "uniprotId": "string",
        "vendorName": "string"
    })))


def get_url_if_permitted(dao):
    """
        Get antibody URL only if permitted. RULES:
        1. If user is creator of the antibody, return the URL.
        2. Else return only if show_link is True.
    """
    try:
        user_id = get_current_user_id()
    except Exception as e:
        return dao.url if dao.show_link else None

    if user_id == dao.uid:
        return dao.url if dao.url else None
    else:
        return dao.url if dao.show_link else None
