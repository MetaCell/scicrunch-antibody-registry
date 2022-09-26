from django.test import TestCase

from api.services.antibody_service import *
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
        ab = create_antibody(AddUpdateAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.clonality, Clonality.cocktail)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "string")
        self.assertEquals(ab.url, example_ab["url"])
        self.assertEquals(ab.status, Status.QUEUE)
        self.assertIsNotNone(ab.curateTime)
        self.assertIsNotNone(ab.insertTime)

        new_ant = AddUpdateAntibodyDTO(**example_ab)
        try:
            ab2 = create_antibody(new_ant, "bbb")
            self.fail("Should detect duplicate antibody")
        except DuplicatedAntibody:
            pass
        new_ant.catalogNum="new cat num"
        ab2 = create_antibody(new_ant, "bbb")
        self.assertNotEqual(ab.abId, ab2.abId)
        self.assertEquals(ab.vendorName, ab2.vendorName)

        abs = get_antibodies()
        assert abs.page == 1
        assert len(abs.items) == 0
        assert count() == 0
        user_abs = get_user_antibodies("aaaa")
        assert user_abs.page == 1
        assert len(user_abs.items) == 1

        ab3 = get_antibody(ab.abId)
        assert ab.url == ab3.url

        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.save()


        abs = get_antibodies()
        assert len(abs.items) == 1

        assert count() == 1
        print(last_update())