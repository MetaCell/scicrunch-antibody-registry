# Generated by Django 4.0.6 on 2022-09-20 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_antibody_cat_alt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='antibody',
            name='subregion',
            field=models.CharField(db_column='target_subregion', max_length=32, null=True),
        ),
    ]