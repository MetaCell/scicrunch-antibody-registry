from django.test import TestCase
from api.models import Antibody, STATUS
from api.management.commands.scicrunch_citation import Command
from api.services.antibody_service import *
from unittest.mock import patch
from api.utilities.exceptions import FetchCitationMetricFailed
from api.services.ingest_service import RateLimiter
import time
from api.tests.data.test_data import TEST_ANTIBODIES_FOR_SCICRUNCH_CITATION


class ScicrunchCitationMetricCronJobTests(TestCase):
    def setUp(self):
        pass

    def test_scicrunch_citation_django_command(self):
        """
        INSTRUCTION: Check the citation metric - it could change - 137 citations - for ab_id - AB_90755
        saying - "We found 137 mentions in open access literature"
        https://scicrunch.org/resources/data/record/nif-0000-07730-1/AB_90755/resolver
        """
        command = Command()

        # run the command before adding the antibody - this should fail... since the antibody is not present in the database
        try:
            command.handle()
        except SystemExit as e:
            self.assertEqual(e.code, 1)

        # add the antibodies found in Scicrunch website to the DB
        for testab in TEST_ANTIBODIES_FOR_SCICRUNCH_CITATION[:4]:
            ab = Antibody.objects.create(
                ab_id=testab["ab_id"],
                ab_name=testab["ab_name"],
                status=STATUS.CURATED
            )
            ab.save()

        # run the command
        command.handle()

        # now check for all the antibodies - if the number of citation is as expected. 
        for testab in TEST_ANTIBODIES_FOR_SCICRUNCH_CITATION[:4]:
            a = Antibody.objects.get(ab_id=testab["ab_id"])
            self.assertEqual(
                a.citation, 
                testab["expected_citation"]
            )
        
        # Add an antibody not present in the Scicrunch website
        unknown_id_antibody = TEST_ANTIBODIES_FOR_SCICRUNCH_CITATION[4]
        ab2 = Antibody.objects.create(
            ab_id=unknown_id_antibody["ab_id"],  ## unknown Id [100]
            ab_name=unknown_id_antibody["ab_name"],
            status=STATUS.CURATED
        )
        ab2.save()

        command.handle()
        
        # Antibody with unknown_id should not have any citation - hence it should be 0
        a2 = Antibody.objects.get(ab_id=unknown_id_antibody["ab_id"])
        self.assertEqual(a2.citation, 0)


    def test_rate_limiter(self):
        limiter = RateLimiter(max_requests_per_second=10)
        
        # test if allows 10 requests per second
        t1 = time.time()
        for i in range(1, 28):
            if i == 11:
                t2 = time.time()
            limiter.add_request()
        t3 = time.time()
        self.assertGreaterEqual(t2-t1, 1)
        self.assertGreaterEqual(t3-t1, 2)
        

