# Generated by Django 4.2.9 on 2024-04-05 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0010_auto_20240315_0451"),
    ]

    operations = [
        migrations.AddField(
            model_name="antibody",
            name="citation",
            field=models.IntegerField(blank=True, db_index=True, null=True),
        )
    ]