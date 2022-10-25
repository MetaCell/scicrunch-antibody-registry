from django.test import TestCase

from api.services.antibody_service import *
from api.services.search_service import fts_antibodies
from api.models import Vendor, VendorDomain
from openapi.models import AddUpdateAntibody as AddUpdateAntibodyDTO, Status, CommercialType, Clonality

example_ab = {
    "clonality": "cocktail",
    "epitope": "OTTHUMP00000018992",
    "comments": "comment is free text",
    "url": "https://www.bdbiosciences.com/en-it/products/reagents/flow-cytometry-reagents/clinical-discovery-research/single-color-antibodies-ruo-gmp/pe-mouse-anti-human-il-8.340510",
    "abName": "My antibody",
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
    "vendorName": "My vendor",
    "applications": "ELISA, IHC, WB".split(", "),
    "kitContents": "Sheep polyclonal anti-FSH antibody labeled with acridinium ester. Mouse monoclonal anti-FSH antibody covalently coupled to paramagnetic particles."
}


class AntibodiesTestCase(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        ab = create_antibody(AddUpdateAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.clonality, Clonality.cocktail)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "My vendor")
        self.assertEquals(ab.url, example_ab["url"])
        self.assertEquals(ab.status, Status.QUEUE)

        self.assertIsNotNone(ab.insertTime)

        assert ab.curateTime is None
        assert ab.sourceOrganism == "mouse"
        assert len(ab.targetSpecies) == 2

        new_ant = AddUpdateAntibodyDTO(**example_ab)
        try:
            ab2 = create_antibody(new_ant, "bbb")

        except DuplicatedAntibody as e:
            self.fail("No duplicate antibody because none is curated")

        new_ant.catalogNum = "N176A/36"
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
        abget = user_abs.items[0]
        assert len(abget.targetSpecies) == 2

        ab3 = get_antibody(ab.abId, status=STATUS.QUEUE)[0]
        assert ab.url == ab3.url

        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.save()
        assert a.curate_time

        abs = get_antibodies()
        assert len(abs.items) == 1

        assert count() == 1
        print(last_update())

        search = search_antibodies_by_catalog("N176A/35").items
        assert len(search) == 1
        a: Antibody = Antibody.objects.get(ab_id=ab2.abId)
        a.status = STATUS.CURATED
        a.save()

        try:
            create_antibody(AddUpdateAntibodyDTO(**example_ab), "bbb")
            self.fail("Should detect duplicate antibody")
        except DuplicatedAntibody as e:
            da = e.antibody
            assert da.accession != da.abId
            assert da.status == Status.REJECTED
            assert da.abId == ab.abId

        assert VendorDomain.objects.all().count() == 1
        assert Vendor.objects.all().count() == 1

        # Test search

        assert len(fts_antibodies(search="N176A").items) == 2
        assert len(fts_antibodies(search="N176A 35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
