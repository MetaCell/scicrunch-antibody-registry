# Generated by Django 4.1.4 on 2023-04-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0018_alter_antibodyfiles_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="antibody",
            name="show_link",
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="vendor",
            name="show_link",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]