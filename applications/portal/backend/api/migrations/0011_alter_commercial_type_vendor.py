# Generated by Django 4.2.9 on 2024-04-21 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20240315_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='commercial_type',
            field=models.CharField(choices=[('commercial', 'commercial'), ('personal', 'personal'), ('non-profit', 'non-profit'), ('other', 'other')], db_index=True, default='commercial', max_length=32, null=True),
        ),
    ]