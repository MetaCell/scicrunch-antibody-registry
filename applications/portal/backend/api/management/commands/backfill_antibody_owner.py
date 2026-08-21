import time

from django.core.management.base import BaseCommand
from django.db import connection

# Resolve the frozen keycloak-id columns (uid / uploader_uid) to Django users
# through cloudharness_django.Member (kc_id <-> user). Rows whose keycloak id
# has no synced Member stay NULL -- the frozen columns retain the original id,
# so this is safe to re-run any time. This is the only backfill path: it runs
# out-of-band (not in a migration) so pod startup is not held by the bulk
# UPDATEs -- run it once per environment after rollout, after
# `manage.py cloudharness sync`.
#
# Updates run in primary-key-ranged batches: api_antibody and (especially)
# api_historicalantibody carry ~30 secondary indexes each, so a single
# full-table UPDATE rewrites every row plus every index entry in one
# multi-hour transaction. Batches keep each transaction short (Django
# autocommit commits per statement), show progress, and make the command
# safe to interrupt and resume.

BACKFILLS = [
    {
        "label": "api_antibody.owner",
        "table": "api_antibody",
        "pk": "ix",
        "set": "owner_id = m.user_id",
        "guard": "t.owner_id IS NULL AND t.uid IS NOT NULL AND m.kc_id = t.uid",
    },
    {
        "label": "api_antibodyfiles.uploader",
        "table": "api_antibodyfiles",
        "pk": "id",
        "set": "uploader_id = m.user_id",
        "guard": "t.uploader_id IS NULL AND t.uploader_uid IS NOT NULL"
                 " AND t.uploader_uid <> '' AND m.kc_id = t.uploader_uid",
    },
    {
        # History rows are audit-only (admin history view) -- least urgent,
        # by far the largest table, hence last and skippable.
        "label": "api_historicalantibody.owner",
        "table": "api_historicalantibody",
        "pk": "history_id",
        "set": "owner_id = m.user_id",
        "guard": "t.owner_id IS NULL AND t.uid IS NOT NULL AND m.kc_id = t.uid",
        "historical": True,
    },
]


class Command(BaseCommand):
    help = (
        "Re-run the owner/uploader backfill from the frozen keycloak-id columns "
        "(uid / uploader_uid) through cloudharness_django.Member. Safe to run "
        "repeatedly, e.g. after `manage.py cloudharness sync` created new users. "
        "Runs in short per-batch transactions; interrupting and re-running is safe."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size", type=int, default=50000,
            help="Rows scanned per transaction (default 50000)")
        parser.add_argument(
            "--skip-historical", action="store_true",
            help="Skip the api_historicalantibody backfill (audit data only; "
                 "the biggest table by far)")

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        for spec in BACKFILLS:
            if spec.get("historical") and options["skip_historical"]:
                self.stdout.write(f"{spec['label']}: skipped")
                continue
            self._backfill(spec, batch_size)

    def _backfill(self, spec, batch_size):
        table, pk = spec["table"], spec["pk"]
        updated = 0
        last_pk = 0
        started = time.monotonic()
        with connection.cursor() as cursor:
            while True:
                # Advance by pk range, not by "rows still NULL": rows whose
                # keycloak id has no Member stay NULL forever and would
                # otherwise be re-selected on every batch.
                cursor.execute(
                    f"SELECT max({pk}) FROM (SELECT {pk} FROM {table}"
                    f" WHERE {pk} > %s ORDER BY {pk} LIMIT %s) b",
                    [last_pk, batch_size])
                upper = cursor.fetchone()[0]
                if upper is None:
                    break
                cursor.execute(
                    f"UPDATE {table} t SET {spec['set']}"
                    f" FROM cloudharness_django_member m"
                    f" WHERE t.{pk} > %s AND t.{pk} <= %s AND {spec['guard']}",
                    [last_pk, upper])
                updated += cursor.rowcount
                last_pk = upper
                self.stdout.write(
                    f"{spec['label']}: {updated} rows updated,"
                    f" {pk} <= {upper}, {time.monotonic() - started:.0f}s")
        self.stdout.write(self.style.SUCCESS(
            f"{spec['label']}: done, {updated} rows updated"))
