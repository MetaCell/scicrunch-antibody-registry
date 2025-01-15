# Generated by Django 4.2.11 on 2025-01-03 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_remove_antibodysearch_citations_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Partner",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=512)),
                ("url", models.URLField(db_index=True, max_length=2048)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="partners"),
                ),
            ],
            options={
                "verbose_name_plural": "Partners",
                "ordering": ("name",),
            },
        ),
    ]