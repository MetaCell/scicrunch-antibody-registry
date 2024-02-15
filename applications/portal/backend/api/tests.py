from django.test import TestCase
from django.contrib.admin.sites import AdminSite
import jwt
from api.services.antibody_service import *
from api.services.search_service import fts_antibodies
from api.models import Vendor, VendorDomain
from api.repositories.maintainance import refresh_search_view
from openapi.models import (
    AddAntibody as AddAntibodyDTO,
    Status,
    CommercialType,
    Clonality, UpdateAntibody, AddAntibody,
)

from .admin import VendorAdmin
from .models import Vendor, Antibody, VendorDomain, VendorSynonym, Specie
from api.utilities.functions import catalog_number_chunked

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
    "definingCitation": "defining defining defining",
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

example_ab2 =  {
    "clonality": "polyclonal",
    "epitope": "OTTHUMP00000018992",
    "comments": "ENCODE PROJECT External validation DATA SET is released testing lot unknown for any cell type or tissues; status is awaiting lab characterization",
    "url": "https://www.encodeproject.org/antibodies/ENCAB558DXQ/",
    "abName": "Antibody against Drosophila melanogaster Snr1",
    "abTarget": "Snr1",
    "catalogNum": "ENCAB558DXQ",
    "cloneId": "ENCAB558DXQsasa",
    "commercialType": "commercial",
    "definingCitation": "citation citation citation",
    "productConjugate": "string",
    "productForm": "string",
    "productIsotype": "string",
    "sourceOrganism": "rabbit",
    "targetSpecies": ["Drosophila melanogaster"],
    "uniprotId": "uuiid",
    "vendorName": "Andrew Dingwall",
    "applications": ["ELISA"],
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
        self.assertEquals(ab.vendorName, "My vendorname")
        self.assertTrue( 'www.bdbiosciences.com' in ab.vendorUrl)
        self.assertEquals(ab.status, Status.QUEUE)
        self.assertEquals(ab.url, example_ab['url'])

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
        new_ant.url = "https://www.ab.com/My-antibody" # should add this domain to the vendor
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

        try:
            duplicated = AddAntibodyDTO(**example_ab)
            duplicated.vendorName = "My vendor synonym" # should keep the same vendor and add a synonym
            create_antibody(duplicated, "bbb")
            self.fail("Should detect duplicate antibody")
        except DuplicatedAntibody as e:
            da = e.antibody
            assert da.accession != da.abId
            assert da.abId == ab.abId
            assert da.status == Status.QUEUE
            assert da.vendorId == ab.vendorId
            assert da.vendorName == "My vendorname"
            
            synonyms = VendorSynonym.objects.filter(vendor__id=da.vendorId)
            assert len(synonyms) == 1

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

        # Search by catalog number
        self.assertEquals(len(fts_antibodies(search="N176A").items), 2)
        assert len(fts_antibodies(search="N176A 35").items) == 1
        assert len(fts_antibodies(search="N176A|35").items) == 1
        assert len(fts_antibodies(search="N17").items) == 0

        assert len(fts_antibodies(search="N17").items) == 0

        # Search in plain fields

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

        # ab_by_accession = get_antibody_by_accession(ab.accession)
        # assert ab_by_accession.abId == ab.abId
        # assert ab_by_accession.accession == ab.accession
        # assert ab_by_accession.vendorName == ab.vendorName

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

        dao = Antibody.objects.get(ab_id=ab.abId)
        dao.species.set([])
        dao.save()
        assert dao.species.count() == 0
        assert len(dao.target_species_raw) == 0

        dao.target_species_raw = "mouse"
        dao.species.add(Specie.objects.get(name="human"))
        dao.save()
        assert dao.species.count() == 2
        assert 'human' in dao.target_species_raw 
        assert 'mouse' in dao.target_species_raw

        dao.target_species_raw = "mouse,human,rat,human,mouse"
        dao.save()
        assert dao.species.count() == 3

    def test_catalog_number_chunked(self):
        # FOUND
        SEARCH_CATALOG_TERM_1 = 'N1002'
        SEARCH_CATALOG_TERM_2 = 'N0304-AB635P-L'
        SEARCH_CATALOG_TERM_3 = 'N0304-AB635'

        # NOT FOUND
        SEARCH_CATALOG_TERM_4 = 'K0202'
        SEARCH_CATALOG_TERM_5 = 'N0304-AB635P-S'
        SEARCH_CATALOG_TERM_6 = 'N0304-AB635P-'
        SEARCH_CATALOG_TERM_7 = 'N1002-AbRED-S'
        SEARCH_CATALOG_TERM_8 = 'N0304-AB6'
        SEARCH_CATALOG_TERM_9 = 'N1002-AbRED'

        # Create antibodies
        chunk_term_1 = catalog_number_chunked(SEARCH_CATALOG_TERM_1)
        assert set(chunk_term_1.split(' ')) == set('n 1002'.split(' '))

        chunk_term_2 = catalog_number_chunked(SEARCH_CATALOG_TERM_2)
        assert set(chunk_term_2.split(' ')) == set('n 0304 ab 635 p l pl'.split(' '))

        chunk_term_3 = catalog_number_chunked(SEARCH_CATALOG_TERM_3)
        assert set(chunk_term_3.split(' ')) == set('n 0304 ab 635'.split(' '))

        chunk_term_4 = catalog_number_chunked(SEARCH_CATALOG_TERM_4)
        assert set(chunk_term_4.split(' ')) == set('k 0202'.split(' '))

        chunk_term_5 = catalog_number_chunked(SEARCH_CATALOG_TERM_5)
        assert set(chunk_term_5.split(' ')) == set('n 0304 ab 635 p s ps'.split(' '))

        chunk_term_6 = catalog_number_chunked(SEARCH_CATALOG_TERM_6)
        assert set(chunk_term_6.split(' ')) == set('n 0304 ab 635 p'.split(' '))

        chunk_term_7 = catalog_number_chunked(SEARCH_CATALOG_TERM_7)
        assert set(chunk_term_7.split(' ')) == set('n 1002 abred s abreds'.split(' '))

        chunk_term_8 = catalog_number_chunked(SEARCH_CATALOG_TERM_8)
        assert set(chunk_term_8.split(' ')) == set('n 0304 ab 6'.split(' '))

        chunk_term_9 = catalog_number_chunked(SEARCH_CATALOG_TERM_9)
        assert set(chunk_term_9.split(' ')) == set('n 1002 abred'.split(' '))
        
        SEARCH_CATALOG_TERM_10 = 'N0304-AB635P-L'
        SEARCH_CATALOG_ALT_TERM_10 = 'N0304-AB635P-S'
        chunk_term_10 = catalog_number_chunked(SEARCH_CATALOG_TERM_10, SEARCH_CATALOG_ALT_TERM_10)
        assert set(chunk_term_10.split(' ')) == set('n 0304 ab 635 p l s pl ps n0304ab635pl'.split(' '))



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


