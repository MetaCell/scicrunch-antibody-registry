# Generated by Django 4.0.6 on 2023-08-11 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_antibody_uniprot_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendordomain',
            name='base_url',
            field=models.CharField(db_column='domain_name', db_index=True, max_length=2048, null=True),
        ),
    ]
