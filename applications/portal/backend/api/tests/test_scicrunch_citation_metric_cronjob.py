from django.test import TestCase
from api.models import Antibody, STATUS
from api.management.commands.scicrunch_citation import get_json_body, Command
from api.services.antibody_service import *
from .data.test_data import example_ab


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
        ab = Antibody.objects.create(
            ab_id="90755", ab_name="test_ab_name", status=STATUS.CURATED
        )
        ab.save()

        # check that the citation of this should be null - before script
        self.assertIsNone(ab.citation)

        # run the command
        command.handle()

        # now it should be 137 - after the script
        a = Antibody.objects.get(ab_id=ab.ab_id)
        self.assertEqual(a.citation, 137)
