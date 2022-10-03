# Generated by Django 4.0.6 on 2022-10-03 17:42

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.expressions
import django.db.models.functions.comparison
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_antibody_antibody_catalog_num_fts_idx'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='antibody',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.CombinedExpression(django.db.models.functions.text.Length(django.db.models.functions.comparison.Coalesce('defining_citation', django.db.models.expressions.Value(''))), '-', django.db.models.functions.text.Length(django.db.models.functions.comparison.Coalesce('defining_citation__remove_coma', django.db.models.expressions.Value('')))), descending=True), name='antibody_nb_citations_idx'),
        ),
        migrations.AddIndex(
            model_name='antibody',
            index=models.Index(django.db.models.expressions.OrderBy(django.db.models.expressions.CombinedExpression(django.db.models.expressions.CombinedExpression(django.db.models.functions.text.Length(django.db.models.functions.comparison.Coalesce('defining_citation', django.db.models.expressions.Value(''))), '-', django.db.models.functions.text.Length(django.db.models.functions.comparison.Coalesce('defining_citation__remove_coma', django.db.models.expressions.Value('')))), '-', django.db.models.expressions.CombinedExpression(django.db.models.expressions.Value(100), '+', django.db.models.functions.text.Length(django.db.models.functions.comparison.Coalesce('disc_date', django.db.models.expressions.Value(''))))), descending=True), name='antibody_nb_citations_idx2'),
        ),
        migrations.AddIndex(
            model_name='antibody',
            index=models.Index(fields=['-disc_date'], name='antibody_discontinued_idx'),
        ),
        migrations.AddIndex(
            model_name='antibody',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('ab_name', 'clone_id__normalize_relaxed', config='english', weight='A'), name='antibody_name_fts,idx'),
        ),
        migrations.AddIndex(
            model_name='antibody',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.CombinedSearchVector(django.contrib.postgres.search.SearchVector('ab_name', 'clone_id__normalize_relaxed', config='english', weight='A'), '||', django.contrib.postgres.search.SearchVector('ab_id', 'accession', 'commercial_type', 'uid', 'uid_legacy', 'url', 'subregion', 'modifications', 'epitope', 'clonality', 'product_isotype', 'product_conjugate', 'defining_citation', 'product_form', 'comments', 'applications', 'kit_contents', 'feedback', 'curator_comment', 'disc_date', 'status', config='english', weight='C'), django.contrib.postgres.search.SearchConfig('english')), name='antibody_all_fts_idx'),
        ),
        migrations.AddIndex(
            model_name='antibody',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('ab_id', 'accession', 'commercial_type', 'uid', 'uid_legacy', 'url', 'subregion', 'modifications', 'epitope', 'clonality', 'product_isotype', 'product_conjugate', 'defining_citation', 'product_form', 'comments', 'applications', 'kit_contents', 'feedback', 'curator_comment', 'disc_date', 'status', config='english', weight='C'), name='antibody_all_fts_idx2'),
        ),
        migrations.AddIndex(
            model_name='gene',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('symbol', config='english'), name='gene_symbol_fts_idx'),
        ),
        migrations.AddIndex(
            model_name='specie',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('name', config='english'), name='specie_name_fts_idx'),
        ),
        migrations.AddIndex(
            model_name='vendor',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('name', config='english'), name='vendor_name_fts_idx'),
        ),
    ]