# Generated by Django 4.0.6 on 2022-09-21 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_antibody_ab_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='antibody',
            name='applications',
            field=models.TextField(null=True),
        ),
    ]