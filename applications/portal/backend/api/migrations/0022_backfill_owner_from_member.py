from django.db import migrations

# The owner/uploader backfill originally ran here, but the bulk UPDATEs over
# api_antibody / api_historicalantibody held the run-migrations init container
# (and thus pod startup) for minutes. It is idempotent and reads from the
# frozen uid/uploader_uid columns, so it now runs out-of-band instead:
# run `manage.py backfill_antibody_owner` once per environment after rollout
# (kept as an empty migration for environments that already applied it).


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0021_antibody_owner_antibodyfiles_uploader"),
    ]

    operations = []
