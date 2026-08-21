"""Replace the antibody_search materialized view with a trigger-maintained table.

The materialized view required a full recompute of every row on each curated
antibody save (REFRESH MATERIALIZED VIEW CONCURRENTLY). It is replaced by a
plain table kept up to date row-by-row from database triggers, so every write
path (ORM, raw SQL, bulk import) is covered and a save costs O(1).

This migration is DDL-only and runs in milliseconds: the old view is renamed
to antibody_search_legacy and its content is copied into the new table in the
background at application startup (see
api.repositories.maintainance.ensure_search_table_populated), so the
run-migrations init container never blocks on a data fill.
"""
from django.db import migrations

# Single source of truth for the search row computation, shared by the
# triggers, the initial fill and the reconcile job. The expression is the
# same as the former materialized view definition (see migration 0012).
CREATE_ROW_COMPUTE_FUNCTION = """
CREATE OR REPLACE FUNCTION antibody_search_row_compute(a api_antibody)
RETURNS antibody_search
LANGUAGE sql STABLE
AS $antibody_search_row_compute$
SELECT a.ix,
(
    setweight(to_tsvector('english'::regconfig, (((
    COALESCE(a.ab_name, ''::text) || ' '::text) ||
            COALESCE(a.clone_id, ''::text) || ' '::text))
), 'A'::"char") ||

    setweight(to_tsvector('english'::regconfig, (((((((((((((((((((((((((
        COALESCE(v.vendor, ''::text) || ' '::text) ||
        COALESCE(s.name, ''::text) || ' '::text) ||
        COALESCE(a.target_subregion, ''::text) || ' '::text) ||
            COALESCE(a.clonality, ''::text)) || ' '::text) ||
        COALESCE(a.target_modification, ''::text)) || ' '::text) ||
        COALESCE(a.epitope, ''::character varying)::text) || ' '::text) ||
        COALESCE(a.product_isotype, ''::character varying)::text) || ' '::text) ||
        COALESCE(a.ab_target, ''::character varying)::text) || ' '::text) ||
        COALESCE(a.ab_target_entrez_gid, ''::character varying)::text) || ' '::text) ||
        COALESCE(a.uniprot_id, ''::character varying)::text) || ' '::text) ||
        COALESCE(a.product_isotype, ''::character varying)::text) || ' '::text) ||
    COALESCE(a.product_conjugate, ''::text) ||
    COALESCE(a.product_form, ''::character varying)::text) || ' '::text) ||
    COALESCE(a.target_species_raw, ''::character varying)::text) || ' '::text) ||
    COALESCE(a.kit_contents, ''::character varying)::text) || ' '::text)), 'C'::"char") ||
    setweight(to_tsvector('english'::regconfig, (((
        COALESCE(a.comments, ''::text) || ' '::text) ||
                COALESCE(a.curator_comment, ''::text) || ' '::text))
    ), 'D'::"char")

) AS search_vector,
CASE
    WHEN a.defining_citation ~ '^[0-9,]+$' THEN CAST(SPLIT_PART(a.defining_citation, ',', 1) AS INTEGER)
    ELSE 10000000
END AS defining_citation,
CASE
    WHEN a.disc_date IS NOT NULL THEN 1
    ELSE 0
END AS disc,
a.status
FROM (SELECT 1) AS _
LEFT JOIN api_vendor v ON v.id = a.vendor_id
LEFT JOIN api_specie s ON s.id = a.source_organism_id
$antibody_search_row_compute$;
"""

CREATE_TRIGGERS = """
-- Bulk loaders can suspend the sync triggers for the current transaction with
--   SET LOCAL antibody_search.skip_sync = 'on'
-- and fill the table set-based instead (see Ingestor._swap_antibodies).
CREATE OR REPLACE FUNCTION antibody_search_sync_trigger()
RETURNS trigger
LANGUAGE plpgsql
AS $antibody_search_sync_trigger$
DECLARE
    r antibody_search;
BEGIN
    IF current_setting('antibody_search.skip_sync', true) = 'on' THEN
        RETURN NULL;
    END IF;
    r := antibody_search_row_compute(NEW);
    INSERT INTO antibody_search (ix, search_vector, defining_citation, disc, status)
    VALUES (r.ix, r.search_vector, r.defining_citation, r.disc, r.status)
    ON CONFLICT (ix) DO UPDATE SET
        search_vector = EXCLUDED.search_vector,
        defining_citation = EXCLUDED.defining_citation,
        disc = EXCLUDED.disc,
        status = EXCLUDED.status;
    RETURN NULL;
END;
$antibody_search_sync_trigger$;

CREATE TRIGGER antibody_search_sync
AFTER INSERT OR UPDATE ON api_antibody
FOR EACH ROW EXECUTE FUNCTION antibody_search_sync_trigger();

-- vendor and specie names are baked into the search vector: fan out to the
-- related antibodies when they change
CREATE OR REPLACE FUNCTION antibody_search_vendor_sync_trigger()
RETURNS trigger
LANGUAGE plpgsql
AS $antibody_search_vendor_sync_trigger$
BEGIN
    IF current_setting('antibody_search.skip_sync', true) = 'on' THEN
        RETURN NULL;
    END IF;
    INSERT INTO antibody_search (ix, search_vector, defining_citation, disc, status)
    SELECT r.ix, r.search_vector, r.defining_citation, r.disc, r.status
    FROM api_antibody a
    CROSS JOIN LATERAL antibody_search_row_compute(a) AS r
    WHERE a.vendor_id = NEW.id
    ON CONFLICT (ix) DO UPDATE SET
        search_vector = EXCLUDED.search_vector,
        defining_citation = EXCLUDED.defining_citation,
        disc = EXCLUDED.disc,
        status = EXCLUDED.status;
    RETURN NULL;
END;
$antibody_search_vendor_sync_trigger$;

CREATE TRIGGER antibody_search_vendor_sync
AFTER UPDATE ON api_vendor
FOR EACH ROW
WHEN (OLD.vendor IS DISTINCT FROM NEW.vendor)
EXECUTE FUNCTION antibody_search_vendor_sync_trigger();

CREATE OR REPLACE FUNCTION antibody_search_specie_sync_trigger()
RETURNS trigger
LANGUAGE plpgsql
AS $antibody_search_specie_sync_trigger$
BEGIN
    IF current_setting('antibody_search.skip_sync', true) = 'on' THEN
        RETURN NULL;
    END IF;
    INSERT INTO antibody_search (ix, search_vector, defining_citation, disc, status)
    SELECT r.ix, r.search_vector, r.defining_citation, r.disc, r.status
    FROM api_antibody a
    CROSS JOIN LATERAL antibody_search_row_compute(a) AS r
    WHERE a.source_organism_id = NEW.id
    ON CONFLICT (ix) DO UPDATE SET
        search_vector = EXCLUDED.search_vector,
        defining_citation = EXCLUDED.defining_citation,
        disc = EXCLUDED.disc,
        status = EXCLUDED.status;
    RETURN NULL;
END;
$antibody_search_specie_sync_trigger$;

CREATE TRIGGER antibody_search_specie_sync
AFTER UPDATE ON api_specie
FOR EACH ROW
WHEN (OLD.name IS DISTINCT FROM NEW.name)
EXECUTE FUNCTION antibody_search_specie_sync_trigger();
"""

FORWARD = """
DROP MATERIALIZED VIEW IF EXISTS antibody_search_legacy;
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_matviews
               WHERE schemaname = current_schema() AND matviewname = 'antibody_search') THEN
        ALTER MATERIALIZED VIEW antibody_search RENAME TO antibody_search_legacy;
    END IF;
END $$;
ALTER INDEX IF EXISTS antibody_search_idx RENAME TO antibody_search_legacy_idx;
ALTER INDEX IF EXISTS antibody_search_fts_idx RENAME TO antibody_search_legacy_fts_idx;

CREATE TABLE antibody_search (
    ix integer PRIMARY KEY REFERENCES api_antibody (ix) ON DELETE CASCADE,
    search_vector tsvector,
    defining_citation integer NOT NULL DEFAULT 0,
    disc integer NOT NULL,
    status character varying(12)
);
CREATE INDEX antibody_search_fts_idx ON antibody_search USING gin (search_vector);
"""

# Reverse: back to the materialized view as defined in migration 0012.
# NOTE: recreating the view computes all rows, so a rollback blocks for the
# duration of a full refresh.
REVERSE = """
DROP TRIGGER IF EXISTS antibody_search_sync ON api_antibody;
DROP TRIGGER IF EXISTS antibody_search_vendor_sync ON api_vendor;
DROP TRIGGER IF EXISTS antibody_search_specie_sync ON api_specie;
DROP FUNCTION IF EXISTS antibody_search_sync_trigger();
DROP FUNCTION IF EXISTS antibody_search_vendor_sync_trigger();
DROP FUNCTION IF EXISTS antibody_search_specie_sync_trigger();
DROP FUNCTION IF EXISTS antibody_search_row_compute(api_antibody);
DROP TABLE IF EXISTS antibody_search;
DROP MATERIALIZED VIEW IF EXISTS antibody_search_legacy;

CREATE MATERIALIZED VIEW antibody_search AS
SELECT ix,
(
    setweight(to_tsvector('english'::regconfig, (((
    COALESCE(ab_name, ''::text) || ' '::text) ||
            COALESCE(clone_id, ''::text) || ' '::text))
), 'A'::"char") ||

    setweight(to_tsvector('english'::regconfig, (((((((((((((((((((((((((
        COALESCE(api_vendor.vendor, ''::text) || ' '::text) ||
        COALESCE(api_specie.name, ''::text) || ' '::text) ||
        COALESCE(target_subregion, ''::text) || ' '::text) ||
            COALESCE(clonality, ''::text)) || ' '::text) ||
        COALESCE(target_modification, ''::text)) || ' '::text) ||
        COALESCE(epitope, ''::character varying)::text) || ' '::text) ||
        COALESCE(product_isotype, ''::character varying)::text) || ' '::text) ||
        COALESCE(ab_target, ''::character varying)::text) || ' '::text) ||
        COALESCE(ab_target_entrez_gid, ''::character varying)::text) || ' '::text) ||
        COALESCE(uniprot_id, ''::character varying)::text) || ' '::text) ||
        COALESCE(product_isotype, ''::character varying)::text) || ' '::text) ||
    COALESCE(product_conjugate, ''::text) ||
    COALESCE(product_form, ''::character varying)::text) || ' '::text) ||
    COALESCE(target_species_raw, ''::character varying)::text) || ' '::text) ||
    COALESCE(kit_contents, ''::character varying)::text) || ' '::text)), 'C'::"char") ||
    setweight(to_tsvector('english'::regconfig, (((
        COALESCE(comments, ''::text) || ' '::text) ||
                COALESCE(curator_comment, ''::text) || ' '::text))
    ), 'D'::"char")

) AS search_vector,
CASE
    WHEN api_antibody.defining_citation ~ '^[0-9,]+$' THEN CAST(SPLIT_PART(api_antibody.defining_citation, ',', 1) AS INTEGER)
    ELSE 10000000
END as defining_citation,
CASE
    WHEN disc_date IS NOT NULL THEN 1
    ELSE 0
END AS disc,
status
FROM api_antibody
LEFT JOIN api_vendor ON api_vendor.id = api_antibody.vendor_id
LEFT JOIN api_specie ON api_specie.id = api_antibody.source_organism_id;

CREATE UNIQUE INDEX antibody_search_idx ON antibody_search (ix);
CREATE INDEX antibody_search_fts_idx ON antibody_search USING gin (search_vector);
"""


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_backfill_owner_from_member'),
    ]

    operations = [
        migrations.RunSQL(
            sql=FORWARD + CREATE_ROW_COMPUTE_FUNCTION + CREATE_TRIGGERS,
            reverse_sql=REVERSE,
        ),
    ]
