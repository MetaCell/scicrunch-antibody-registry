from django.test import TestCase

from api.services.antibody_service import create_antibody, get_antibodies
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO, Status, CommercialType, Clonality

example_ab = {
  "clonality": "cocktail",
  "epitope": "OTTHUMP00000018992",
  "comments": "comment is free text",
  "url": "https://www.bdbiosciences.com/en-it/products/reagents/flow-cytometry-reagents/clinical-discovery-research/single-color-antibodies-ruo-gmp/pe-mouse-anti-human-il-8.340510",
  "abName": "string",
  "abTarget": "LRKK2",
  "catalogNum": "N176A/35",
  "cloneId": "N176A/35",
  "commercialType": "commercial",
  "definingCitation": "string",
  "productConjugate": "string",
  "productForm": "string",
  "productIsotype": "string",
  "sourceOrganism": "mouse",
  "targetSpecies": [
    "mouse",
    "human"
  ],
  "uniprotId": "string",
  "vendorName": "string",
  "applications": "ELISA, IHC, WB",
  "kitContents": "Sheep polyclonal anti-FSH antibody labeled with acridinium ester. Mouse monoclonal anti-FSH antibody covalently coupled to paramagnetic particles."
}

class AnimalTestCase(TestCase):
    def setUp(self):
        pass
        

    def test_create(self):
        ab = create_antibody(AddUpdateAntibodyDTO(**example_ab))
        self.assertEquals(ab.clonality, Clonality.cocktail)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "string")
        self.assertEquals(ab.url, example_ab["url"])
        self.assertEquals(ab.status, Status.QUEUE)
        self.assertIsNotNone(ab.curateTime)
        self.assertIsNotNone(ab.insertTime)

        ab2 = create_antibody(AddUpdateAntibodyDTO(**example_ab))
        self.assertNotEqual(ab.abId, ab2.abId)
        self.assertEquals(ab.vendorName, ab2.vendorName)

        abs = get_antibodies()
        assert abs.page == 0
        assert len(abs.items) == 2
