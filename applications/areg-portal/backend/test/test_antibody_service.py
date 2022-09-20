from django.test import TestCase

from api.services.antibody_service import create_antibody, get_antibodies
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO, Status, CommercialType, Clonality

example_ab = {
  "clonality": "unknown",
  "epitope": "string",
  "comments": "string",
  "url": "https://vendorurl/ab",
  "abName": "string",
  "abTarget": "string",
  "catalogNum": "string",
  "cloneId": "string",
  "commercialType": "commercial",
  "definingCitation": "string",
  "productConjugate": "string",
  "productForm": "string",
  "productIsotype": "string",
  "sourceOrganism": "string",
  "targetSpecies": [
    "string"
  ],
  "uniprotId": "string",
  "vendorName": "vendor name",
  "vendorId": "vid"
}

class AnimalTestCase(TestCase):
    def setUp(self):
        pass
        

    def test_create(self):
        ab = create_antibody(AddUpdateAntibodyDTO(**example_ab))
        self.assertEquals(ab.clonality, Clonality.unknown)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "vendor name")
        self.assertEquals(ab.url, "https://vendorurl/ab")
        self.assertEquals(ab.status, Status.QUEUE)
        self.assertIsNotNone(ab.curateTime)
        self.assertIsNotNone(ab.insertTime)

        ab2 = create_antibody(AddUpdateAntibodyDTO(**example_ab))
        self.assertNotEqual(ab.abId, ab2.abId)
        self.assertEquals(ab.vendorName, ab2.vendorName)

        abs = get_antibodies()
        assert abs.page == 0
        assert len(abs.items) == 2
