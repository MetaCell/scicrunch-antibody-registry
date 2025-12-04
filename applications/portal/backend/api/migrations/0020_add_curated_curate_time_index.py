# Generated migration for adding composite index for last_update optimization

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_initialize_antibody_stats'),
    ]

    operations = [
        # Add composite index for optimizing last_update queries
        migrations.RunSQL(
            sql="""
            CREATE INDEX IF NOT EXISTS idx_antibody_curated_curate_time 
            ON api_antibody(status, curate_time DESC) 
            WHERE status = 'CURATED' AND curate_time IS NOT NULL;
            """,
            reverse_sql="""
            DROP INDEX IF EXISTS idx_antibody_curated_curate_time;
            """
        ),
    ]
