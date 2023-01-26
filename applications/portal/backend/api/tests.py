from django.test import TestCase
from django.contrib.admin.sites import AdminSite
import jwt
from api.services.antibody_service import *
from api.services.search_service import fts_antibodies
from api.models import Vendor, VendorDomain
from openapi.models import (
    AddAntibody as AddAntibodyDTO,
    Status,
    CommercialType,
    Clonality, UpdateAntibody, AddAntibody,
)

from .admin import VendorAdmin
from .models import Vendor, Antibody, VendorDomain

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
    "targetSpecies": ["mouse", "human"],
    "uniprotId": "string",
    "vendorName": "My vendor",
    "applications": "ELISA, IHC, WB".split(", "),
    "kitContents": "Sheep polyclonal anti-FSH antibody labeled with acridinium ester. Mouse monoclonal anti-FSH antibody covalently coupled to paramagnetic particles.",
}

token = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJrVmp2XzE1N0JNcUVqOEZjZGk1X3c1Qkp6empaanBzUXNKRXduRUd2NnpVIn0.eyJleHAiOjE2NzMzNDQ0MzUsImlhdCI6MTY3MzM0NDEzNSwiYXV0aF90aW1lIjoxNjczMzQzODIzLCJqdGkiOiI5OGE2MTQzNS05M2UxLTRhYzEtYThmZC0wODMwNTkyNjI5NmQiLCJpc3MiOiJodHRwOi8vYWNjb3VudHMuYXJlZy9hdXRoL3JlYWxtcy9hcmVnIiwiYXVkIjpbIndlYi1jbGllbnQiLCJhY2NvdW50Il0sInN1YiI6IjljMTc3NzZiLTNlNzgtNGUzMC04MGMzLWUyOTBiMDYxMTU5MyIsInR5cCI6IkJlYXJlciIsImF6cCI6IndlYi1jbGllbnQiLCJzZXNzaW9uX3N0YXRlIjoiMzM1NzdjNmYtMDA4NC00OWE1LWFlY2EtYWZkNWI1MWVlZmVmIiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLWFyZWciXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGFkbWluaXN0cmF0b3Itc2NvcGUgZW1haWwiLCJzaWQiOiIzMzU3N2M2Zi0wMDg0LTQ5YTUtYWVjYS1hZmQ1YjUxZWVmZWYiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJhIGEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhQGFhLml0IiwiZ2l2ZW5fbmFtZSI6ImEiLCJmYW1pbHlfbmFtZSI6ImEiLCJlbWFpbCI6ImFAYWEuaXQifQ.F_OKUgJn4lMGpHBBEIWfIjg6r5BaiGTtNUHTRwRhq2vT9EI4Qg-JE5WiutvxjNwih27kmwkwVkN62TWPLq32TGDueSiOQjhTZzJSBKscVGLunaQqt1PGUh4uh_Z2Y-KTaOKc_1edVmwgOKqWVQaSc_71Egdh5nDjsUDOzo5761y0fIR1Xh5O_sMImPh4iv3iEZRE25GrBB6NrMVamJ09zLoRyLsvYjaU8V0oDsabg_gtyoxlUG5Gq8p_-UkruXtLQxDhpCKV6_XnQrfEwGVaD-MqNhY1lO9czFD6aLng2wtSANHozwmBHg5uHkn7gZYedn5XmsYD3tCjLPoE9S_13Q'


# class UserTestCase(TestCase):
#     def setUp(self):
#         pass
#
#     def test_create(self):
#         user = jwt.decode(token, options={"verify_exp": False}, algorithms='RS256')
#

class AntibodiesTestCase(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        ab = create_antibody(AddAntibodyDTO(**example_ab), "aaaa")
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

        new_ant = AddAntibodyDTO(**example_ab)
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
            create_antibody(AddAntibodyDTO(**example_ab), "bbb")
            self.fail("Should detect duplicate antibody")
        except DuplicatedAntibody as e:
            da = e.antibody
            assert da.accession != da.abId
            assert da.abId == ab.abId

        assert VendorDomain.objects.all().count() == 1
        assert Vendor.objects.all().count() == 1

        # Test search

        assert len(fts_antibodies(search="N176A").items) == 2
        assert len(fts_antibodies(search="N176A 35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1

    def test_update(self):
        user_id = "aaaa"
        new_name = "My updated abName"
        ab = create_antibody(AddAntibodyDTO(**example_ab), user_id)
        user_antibodies = get_user_antibodies(user_id, 0, 1)
        ab_to_update = user_antibodies.items[0]
        self.assertNotEqual(ab.abName, new_name)
        assert ab.abId == ab_to_update.abId
        ab_update_example = dict(example_ab)
        ab_update_example['abName'] = new_name
        updated_ab = update_antibody(user_id, ab_to_update.accession, UpdateAntibody(**ab_update_example))
        self.assertEquals(updated_ab.abName, new_name)
        ab_update_example['vendorName'] = 'Vendor Update Test'
        with self.assertRaises(AntibodyDataException):
            update_antibody(user_id, ab_to_update.accession, AddAntibody(**ab_update_example))


class VendorAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_force_delete_vendor(self):
        # Create data
        vendor = Vendor.objects.create()
        
        ab1 = Antibody.objects.create(vendor=vendor, url='https://example.com')

        ab2 = Antibody.objects.create(vendor=vendor, url='https://example.com')

        self.assertEquals(len(Vendor.objects.all()), 1)
        self.assertEquals(len(VendorDomain.objects.all()), 1)

        domain = VendorDomain.objects.create(vendor=vendor)

        self.assertEquals(ab1.vendor, vendor)
        self.assertEquals(ab2.vendor, vendor)
        self.assertEquals(domain.vendor, vendor)
        self.assertEquals(len(Antibody.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 1)
        self.assertEquals(len(VendorDomain.objects.all()), 2)

        # Instanciante and tests
        va = VendorAdmin(Vendor, self.site)
        va._force_delete(vendor)
        self.assertEquals(len(Antibody.objects.all()), 0)
        self.assertEquals(len(VendorDomain.objects.all()), 0)
        self.assertEquals(len(Vendor.objects.all()), 1)

    def test_swap_ownership_antibodies(self):
        # Create data
        v1 = Vendor.objects.create(name="v1")
        v2 = Vendor.objects.create(name="v2")
        ab1 = Antibody.objects.create(vendor=v1, url='https://example.com')

        ab2 = Antibody.objects.create(vendor=v1, url='https://example.com')

        domain = VendorDomain.objects.create(vendor=v1)

        self.assertEquals(ab1.vendor, v1)
        self.assertIn(ab1, v1.antibody_set.all())
        self.assertEquals(ab2.vendor, v1)
        self.assertIn(ab2, v1.antibody_set.all())
        self.assertEquals(domain.vendor, v1)
        self.assertEquals(len(Antibody.objects.all()), 2)
        self.assertEquals(len(Vendor.objects.all()), 2)
        self.assertEquals(len(VendorDomain.objects.all()), 2)

    #     # Instanciante and tests
    #     va = VendorAdmin(Vendor, self.site)
    #     va._swap_ownership(v1, v2)

    #     self.assertIn(ab1, v2.antibody_set.all())
    #     self.assertIn(ab2, v2.antibody_set.all())
    #     self.assertNotIn(ab1, v1.antibody_set.all())
    #     self.assertNotIn(ab2, v1.antibody_set.all())
    #     self.assertIn(domain, v2.vendordomain_set.all())
    #     self.assertNotIn(domain, v1.vendordomain_set.all())
    #     self.assertEquals(len(Antibody.objects.all()), 2)
    #     self.assertEquals(len(Vendor.objects.all()), 2)
    #     self.assertEquals(len(VendorDomain.objects.all()), 1)
