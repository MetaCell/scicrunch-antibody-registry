from django.db import migrations

from api.management.commands.backfill_antibody_owner import BACKFILL_SQL

# Rows whose keycloak id has no synced Member stay NULL -- the frozen
# uid/uploader_uid columns retain the original id, so the backfill can be
# re-run later with `manage.py backfill_antibody_owner`.


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_antibody_owner_antibodyfiles_uploader"),
        ("cloudharness_django", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(sql=sql, reverse_sql=migrations.RunSQL.noop)
        for sql in BACKFILL_SQL
    ]
