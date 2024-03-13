from django.test import TestCase
from api.services.antibody_service import *
from api.services.search_service import fts_antibodies
from api.models import Vendor, VendorDomain
from api.repositories.maintainance import refresh_search_view
from openapi.models import (
    AddAntibody as AddAntibodyDTO,
    Status,
    CommercialType,
    Clonality,
    UpdateAntibody,
    AddAntibody,
)

from ..models import Vendor, Antibody, VendorDomain, Specie
from .data.test_data import example_ab2, example_ab
from cloudharness.middleware import set_authentication_token, get_authentication_token
from api.services.user_service import get_current_user_id

token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJUHJQcnZBanBrZ19HQlVUSVN5YVBoaXRMeUtVNDlQUGJRUTlPaWNBWEtzIn0.eyJleHAiOjE3MTAyMzg2MDAsImlhdCI6MTcxMDIyNzgwMCwiYXV0aF90aW1lIjoxNzEwMjI3ODAwLCJqdGkiOiIxZTFkMjRmMy0zMTU3LTRhNzEtOGI4Ny0yNzZhZjBkMGFjMTUiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmFyZWcuZGV2Lm1ldGFjZWxsLnVzL2F1dGgvcmVhbG1zL2FyZWciLCJhdWQiOlsid2ViLWNsaWVudCIsImFjY291bnQiXSwic3ViIjoiNjZhOWRkNTQtMjIxNC00ZWQ3LWI0ZjgtZGFhNWJmM2M5YTc5IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoid2ViLWNsaWVudCIsInNlc3Npb25fc3RhdGUiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFkbWluaXN0cmF0b3IiLCJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiI1MzMyNDQ5MS0zNmY4LTRlODctOGE5YS0yZTIyODc3YmQxMDciLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJGaWxpcHBvIExlZGRhIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYSIsImdpdmVuX25hbWUiOiJGaWxpcHBvIiwiZmFtaWx5X25hbWUiOiJMZWRkYSIsImVtYWlsIjoiYUBhYS5pdCJ9.RShiiCZPEwz2IxEQqU2TBB1F6NQIOMfcrVU99eMSlXEahb38VegqUyIqUfoQUrQAHqnyysR67HeBuCq2SNh9ctxpAiEpFq7LAkqpEIQfByvdyDsBArT0jeWd6DuQ91_7PAdSPWqFEr-uFo9476NQZecrIuXCaNC3rrHbPb6GZKwT6gUMu_sCYAawT8jA_V9rpfgedM5PuqJHTp40of-ZDchD7Cc2NTIE2RopgkKifxtRRjQ9wwudz0hxKjVb9E9GCtkaA-MjDdEeVxnSgTu2p8Y9EaPOoZKt-zt0XTjRT8otwx7yOzz1euhDVh1-1zBb7V3Lt-w4BW19draYkGWMzg"


class AntibodiesTestCase(TestCase):
    def setUp(self):
        if token:
            set_authentication_token(token)
            user = get_current_user_id()

    def test_create(self):
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
        self.assertEquals(ab.clonality, Clonality.cocktail)
        self.assertEquals(ab.commercialType, CommercialType.commercial)
        self.assertIsNotNone(ab.vendorId)
        self.assertEquals(ab.vendorName, "My vendorname")
        self.assertTrue("www.bdbiosciences.com" in ab.vendorUrl)
        self.assertEquals(ab.status, Status.QUEUE)
        self.assertEquals(ab.url, example_ab["url"])

        self.assertIsNotNone(ab.insertTime)

        assert ab.curateTime is None
        assert ab.sourceOrganism == "mouse"
        assert len(ab.targetSpecies) == 2

        domains = VendorDomain.objects.filter(vendor__id=ab.vendorId)
        self.assertEquals(len(domains), 1)
        self.assertEquals(domains[0].base_url, "www.bdbiosciences.com")
        self.assertEquals(domains[0].status, STATUS.QUEUE)

        new_ant = AddAntibodyDTO(**example_ab)
        new_ant.catalogNum = "N176A/36"
        new_ant.abName = "Another antibody"
        new_ant.url = (
            "https://www.ab.com/My-antibody"  # should add this domain to the vendor
        )
        ab2 = create_antibody(new_ant, "bbb")
        self.assertNotEqual(ab.abId, ab2.abId)
        self.assertEquals(ab.vendorName, ab2.vendorName)

        domains = VendorDomain.objects.filter(vendor__id=ab2.vendorId)
        self.assertEquals(len(domains), 2)

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
        a.save(update_search=False)
        assert a.curate_time

        abs = get_antibodies()
        assert len(abs.items) == 1

        assert count() == 1
        print(last_update())

        search = search_antibodies_by_catalog("N176A/35").items
        assert len(search) == 1
        a: Antibody = Antibody.objects.get(ab_id=ab2.abId)
        a.status = STATUS.CURATED
        a.save(update_search=False)

        duplicated = AddAntibodyDTO(**example_ab)
        # duplicated.vendorName = "My vendor synonym" # should keep the same vendor and add a synonym
        da = create_antibody(duplicated, "bbb")

        assert da.accession != da.abId
        assert da.abId == ab.abId
        assert da.status == Status.QUEUE
        assert da.vendorId == ab.vendorId
        assert da.vendorName == "My vendorname"

        assert VendorDomain.objects.all().count() == 2
        assert Vendor.objects.all().count() == 1

        # Test search

        ab = create_antibody(AddAntibodyDTO(**example_ab2), "aaaa")
        a: Antibody = Antibody.objects.get(ab_id=ab.abId)
        a.status = STATUS.CURATED
        a.entrez_id = "entrez"
        a.uniprot_id = "uniprot"
        a.show_link = True
        a.save(update_search=False)

        ab = get_antibody(ab.abId)[0]
        assert ab.abTargetEntrezId == "entrez"
        assert ab.abTargetUniprotId == "uniprot"
        assert ab.ix
        assert ab.showLink is not None

        ab_by_accession = get_antibody_by_accession(ab.accession)
        assert ab_by_accession.abId == ab.abId
        assert ab_by_accession.accession == ab.accession
        assert ab_by_accession.vendorName == ab.vendorName

        # Search by catalog number
        self.assertEquals(len(fts_antibodies(search="N176A").items), 2)
        assert len(fts_antibodies(search="N176A 35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
        assert len(fts_antibodies(search="N17").items) == 0

        assert len(fts_antibodies(search="N17").items) == 0

        a = Antibody.objects.get(ab_id=ab.abId)
        a.catalog_num = "N0304-AB635P-L"
        a.cat_alt = "N0304-AB635P-S"
        a.save()

        assert len(fts_antibodies(search="N0304-AB635P-L").items) == 1
        assert len(fts_antibodies(search="N0304AB635PL").items) == 1
        assert len(fts_antibodies(search="N0304-AB635P-S").items) == 1
        assert len(fts_antibodies(search="635P-L").items) == 1
        assert len(fts_antibodies(search="N0304-AB635P-X").items) == 0

        # Search in plain fields

        # FIXME full-text search is not working in the tests as cannot account for materialized view update

        # refresh_search_view()
        # import time
        # time.sleep(60) # give time to the materialized view to be updated

        # # Search in name
        # assert len(fts_antibodies(search="FastImmune").items) == 1
        # assert len(fts_antibodies(search="fastImmune").items) == 1, "Search must be case insensitive"
        # assert len(fts_antibodies(search="FastImmune PE Mouse").items) == 1
        # assert len(fts_antibodies(search="BD FastImmune™ PE Mouse Anti-Human IL-8").items) == 1
        # assert len(fts_antibodies(search="BD FastImmune™ PE Mouse (Anti-Human) IL-8").items) == 1, "Must ignore special characters"

        # assert len(fts_antibodies(search="Sheep polyclonal anti-FSH antibody labeled with acridinium ester").items) == 2, "Search in kit contents"

        # assert len(fts_antibodies(search="defining").items) == 2, "Search in defining citation"
        # assert len(fts_antibodies(search="citation").items) == 1, "Search in defining citation specificity"

        # assert len(fts_antibodies(search="External validation DATA SET is released testing").items) == 1, "Search in comments"
        # assert len(fts_antibodies(search="vendorname").items) == 2
        # assert len(fts_antibodies(search="Andrew Dingwall").items) == 1

        # assert len(fts_antibodies(search="rabbit").items) == 1, "Search in source organism"
        # assert len(fts_antibodies(search="Rabbit").items) == 1
        # assert len(fts_antibodies(search="Andrew Dingwall").items) == 1

    def test_update(self):
        user_id = "aaaa"
        new_name = "My updated abName"
        ab = create_antibody(AddAntibodyDTO(**example_ab), user_id)
        user_antibodies = get_user_antibodies(user_id, 0, 1)
        ab_to_update = user_antibodies.items[0]
        self.assertNotEqual(ab.abName, new_name)
        assert ab.abId == ab_to_update.abId
        ab_update_example = dict(example_ab)
        ab_update_example["abName"] = new_name
        updated_ab = update_antibody(
            user_id, ab_to_update.accession, UpdateAntibody(**ab_update_example)
        )
        self.assertEquals(updated_ab.abName, new_name)
        ab_update_example["vendorName"] = "Vendor Update Test"
        with self.assertRaises(AntibodyDataException):
            update_antibody(
                user_id, ab_to_update.accession, AddAntibody(**ab_update_example)
            )

        dao = Antibody.objects.get(ab_id=ab.abId)
        dao.species.set([])
        dao.save()
        assert dao.species.count() == 0
        assert len(dao.target_species_raw) == 0

        dao.target_species_raw = "mouse"
        dao.species.add(Specie.objects.get(name="human"))
        dao.save()
        assert dao.species.count() == 2
        assert "human" in dao.target_species_raw
        assert "mouse" in dao.target_species_raw

        dao.target_species_raw = "mouse,human,rat,human,mouse"
        dao.save()
        assert dao.species.count() == 3
