from django.core.management.base import BaseCommand
from django.db import connection

# Resolve the frozen keycloak-id columns (uid / uploader_uid) to Django users
# through cloudharness_django.Member (kc_id <-> user). Rows whose keycloak id
# has no synced Member stay NULL -- the frozen columns retain the original id,
# so this is safe to re-run any time (also used by migration 0022).
BACKFILL_SQL = [
    """
    UPDATE api_antibody a SET owner_id = m.user_id
    FROM cloudharness_django_member m
    WHERE a.owner_id IS NULL AND a.uid IS NOT NULL AND m.kc_id = a.uid;
    """,
    """
    UPDATE api_historicalantibody h SET owner_id = m.user_id
    FROM cloudharness_django_member m
    WHERE h.owner_id IS NULL AND h.uid IS NOT NULL AND m.kc_id = h.uid;
    """,
    """
    UPDATE api_antibodyfiles f SET uploader_id = m.user_id
    FROM cloudharness_django_member m
    WHERE f.uploader_id IS NULL AND f.uploader_uid IS NOT NULL
      AND f.uploader_uid <> '' AND m.kc_id = f.uploader_uid;
    """,
]


class Command(BaseCommand):
    help = (
        "Re-run the owner/uploader backfill from the frozen keycloak-id columns "
        "(uid / uploader_uid) through cloudharness_django.Member. Safe to run "
        "repeatedly, e.g. after `manage.py cloudharness sync` created new users."
    )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for sql in BACKFILL_SQL:
                cursor.execute(sql)
                self.stdout.write(f"{cursor.rowcount} rows updated")
