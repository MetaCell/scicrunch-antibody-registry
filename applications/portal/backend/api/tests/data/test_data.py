from openapi.models import FilterRequest, KeyValuePair, KeyValueArrayPair, Operation


CONTAINS_FILTER: KeyValuePair = KeyValuePair(key="ab_name", value="sars")
IS_ANY_OF_FILTER: KeyValueArrayPair = KeyValueArrayPair(key="ab_name", value=["sars"])

INCOMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY: FilterRequest = FilterRequest(
    search="",
    contains=[CONTAINS_FILTER],
    equals=[],
    startsWith=[],
    endsWith=[],
    isNotEmpty=[],
    isAnyOf=[IS_ANY_OF_FILTER],
    size=10,
    page=1,
    sortOn=[],
)

COMPLETE_TEST_FILTER_AND_SEARCH_REQUEST_BODY: FilterRequest = FilterRequest(
    search="",
    contains=[],
    equals=[],
    startsWith=[],
    endsWith=[],
    isEmpty=[],
    isNotEmpty=[],
    isAnyOf=[],
    size=10,
    page=1,
    sortOn=[],
    operation=Operation.and_,
    isUserScope=False,
)

example_ab = {
    "clonality": "cocktail",
    "epitope": "OTTHUMP00000018992",
    "comments": "comment is free text",
    "url": "https://www.bdbiosciences.com/en-it/products/reagents/flow-cytometry-reagents/clinical-discovery-research/single-color-antibodies-ruo-gmp/pe-mouse-anti-human-il-8.340510",
    "abName": "BD FastImmune™ PE Mouse Anti-Human IL-8",
    "abTarget": "LRKK2",
    "catalogNum": "N176A/35",
    "cloneId": "N176A/35",
    "commercialType": "commercial",
    "definingCitation": "1000",
    "productConjugate": "string",
    "productForm": "string",
    "productIsotype": "string",
    "sourceOrganism": "mouse",
    "targetSpecies": ["mouse", "human"],
    "uniprotId": "uuiid",
    "vendorName": "My vendorname",
    "applications": "ELISA, IHC, WB".split(", "),
    "kitContents": "Sheep polyclonal anti-FSH antibody labeled with acridinium ester. Mouse monoclonal anti-FSH antibody covalently coupled to paramagnetic particles.",
}

example_ab2 = {
    "clonality": "polyclonal",
    "epitope": "OTTHUMP00000018992",
    "comments": "ENCODE PROJECT External validation DATA SET is released testing lot unknown for any cell type or tissues; status is awaiting lab characterization",
    "url": "https://www.encodeproject.org/antibodies/ENCAB558DXQ/",
    "abName": "Antibody against Drosophila melanogaster Snr1",
    "abTarget": "Snr1",
    "catalogNum": "ENCAB558DXQ",
    "cloneId": "ENCAB558DXQsasa",
    "commercialType": "commercial",
    "definingCitation": "",
    "productConjugate": "string",
    "productForm": "string",
    "productIsotype": "string",
    "sourceOrganism": "rabbit",
    "targetSpecies": ["Drosophila melanogaster"],
    "uniprotId": "uuiid",
    "vendorName": "Andrew Dingwall",
    "applications": ["ELISA"],
}
