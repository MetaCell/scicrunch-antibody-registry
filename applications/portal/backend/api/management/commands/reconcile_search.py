from django.core.management.base import BaseCommand

from api.repositories.maintainance import reconcile_search_table


class Command(BaseCommand):
    help = ("Recompute all antibody_search rows. The table is maintained "
            "row-by-row from database triggers; this full reconcile repairs "
            "any drift and serves as the initial fill on fresh environments.")

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=50000,
                            help="antibodies recomputed per transaction")

    def handle(self, *args, **options):
        total = reconcile_search_table(batch_size=options["batch_size"])
        self.stdout.write(self.style.SUCCESS(
            f"Reconciled {total} antibody_search rows"))
