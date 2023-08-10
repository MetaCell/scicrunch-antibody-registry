from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_antibody_lastedit_time_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DROP MATERIALIZED VIEW IF EXISTS antibody_search;
            CREATE MATERIALIZED VIEW antibody_search AS 
            SELECT ix, 
            (
                setweight(to_tsvector('english'::regconfig, 
                    COALESCE(ab_name, ''::text) || ' ' ||
                    COALESCE(clone_id, ''::text)
                ), 'A'::"char") ||
                
                setweight(to_tsvector('english'::regconfig, 
                    COALESCE(api_vendor.vendor, ''::text) || ' ' ||
                    COALESCE(api_specie.name, ''::text) || ' ' || 
                    COALESCE(STRING_AGG(related_species.name, ' '), '') || ' ' ||
                    COALESCE(target_subregion, ''::text) || ' ' ||
                    COALESCE(clonality, ''::text) || ' ' ||
                    COALESCE(target_modification, ''::text) || ' ' ||
                    COALESCE(epitope, ''::text) || ' ' || 
                    COALESCE(product_isotype, ''::text) || ' ' ||
                    COALESCE(product_conjugate, ''::text) || ' ' ||
                    COALESCE(product_form, ''::text) || ' ' || 
                    COALESCE(kit_contents, ''::text)
                ), 'C'::"char") ||
                
                setweight(to_tsvector('english'::regconfig, 
                    COALESCE(comments, ''::text) || ' ' ||
                    COALESCE(curator_comment, ''::text)
                ), 'D'::"char")
            ) AS search_vector,
            defining_citation,
            disc_date,
            status
            FROM api_antibody 
            LEFT JOIN api_vendor ON api_vendor.id = api_antibody.vendor_id
            LEFT JOIN api_specie ON api_specie.id = api_antibody.source_organism_id
            LEFT JOIN api_antibodyspecies AS abs ON abs.antibody_id = api_antibody.ix
            LEFT JOIN api_specie AS related_species ON abs.specie_id = related_species.id
            GROUP BY api_antibody.ix, api_vendor.vendor, api_specie.name;
            """,
            reverse_sql='''
            DROP MATERIALIZED VIEW antibody_search;
            '''
        ),
        migrations.RunSQL(
            sql="""CREATE UNIQUE INDEX IF NOT EXISTS antibody_search_idx
                    ON antibody_search
                    (ix);
                    """,
        ),
        migrations.RemoveField(
            model_name='antibody',
            name='target_species_raw',
        ),
    ]
