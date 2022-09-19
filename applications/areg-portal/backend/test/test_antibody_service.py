from django.test import TestCase

from api.services.antibody_service import create_antibody, Antibody, AntibodyDTO
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO

example_ab = AddUpdateAntibodyDTO(**{
  "clonality": "unknown",
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
  "productForm": "string",
  "productIsotype": "string",
  "sourceOrganism": "string",
  "targetSpecies": [
    "string"
  ],
  "uniprotId": "string",
  "vendorName": "string",
  "vendorId": "string"
})


class AnimalTestCase(TestCase):
    def setUp(self):
        pass
        

    def test_create(self):
        ab = create_antibody(example_ab)