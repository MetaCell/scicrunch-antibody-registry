import re


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
