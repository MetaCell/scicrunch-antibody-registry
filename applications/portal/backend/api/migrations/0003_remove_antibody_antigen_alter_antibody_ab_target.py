# Generated by Django 4.1.4 on 2023-05-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_alter_antibody_ab_target"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="antibody",
            name="antigen",
        ),
        migrations.AlterField(
            model_name="antibody",
            name="ab_target",
            field=models.CharField(
                blank=True,
                db_column="ab_target",
                db_index=True,
                max_length=1024,
                null=True,
                verbose_name="Target antigen",
            ),
        ),
    ]
