import os
import threading

from django.db import connection, connections
from cloudharness import log
from api.utilities.functions import catalog_number_chunked

# advisory lock guarding the one-time antibody_search fill (arbitrary constant)
SEARCH_TABLE_FILL_LOCK = 810902

# Set-based upsert of antibody_search rows. The row computation lives in the
# antibody_search_row_compute SQL function (single source of truth, also used
# by the sync triggers) created in migration 0023.
SEARCH_UPSERT_SQL = """
    INSERT INTO antibody_search (ix, search_vector, defining_citation, disc, status)
    SELECT r.ix, r.search_vector, r.defining_citation, r.disc, r.status
    FROM api_antibody a
    CROSS JOIN LATERAL antibody_search_row_compute(a) AS r
    {where}
    ON CONFLICT (ix) DO UPDATE SET
        search_vector = EXCLUDED.search_vector,
        defining_citation = EXCLUDED.defining_citation,
        disc = EXCLUDED.disc,
        status = EXCLUDED.status;
"""


def refresh_antibody_stats():
    """
    Refresh the antibody statistics cache table for CURATED antibodies only.
    Runs in a separate thread to avoid blocking the main request.
    """
    sync_execution = os.getenv('TEST', False)

    def refresh_stats_thread():
        log.info("Refreshing antibody stats for CURATED status")
        try:
            from api.models import STATUS
            with connection.cursor() as cursor:
                # Upsert only CURATED status count
                cursor.execute("""
                    INSERT INTO api_antibody_stats (status, count, last_updated)
                    SELECT %s, COUNT(*), NOW()
                    FROM api_antibody
                    WHERE status = %s
                    ON CONFLICT (status)
                    DO UPDATE SET
                        count = EXCLUDED.count,
                        last_updated = EXCLUDED.last_updated;
                """, [STATUS.CURATED, STATUS.CURATED])
            if not sync_execution:
                connection.commit()
            log.info("Antibody stats refreshed successfully")
        except Exception as e:
            log.error(f"Error refreshing antibody stats: {e}")

    if not sync_execution:
        threading.Thread(target=refresh_stats_thread).start()
    else:
        refresh_stats_thread()


def reconcile_search_table(batch_size=50000):
    """
    Recompute every antibody_search row in batches of antibodies.

    antibody_search is maintained row-by-row from database triggers
    (migration 0023); this full recompute is the safety net against drift
    (e.g. a searchable column added without updating the triggers) and also
    serves as the initial fill on fresh environments. Batches keep
    transactions short so concurrent saves are never blocked for long.
    """
    total = 0
    last_ix = -1
    while True:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT max(ix), count(*) FROM (SELECT ix FROM api_antibody"
                " WHERE ix > %s ORDER BY ix LIMIT %s) AS batch",
                [last_ix, batch_size])
            max_ix, count = cursor.fetchone()
            if not count:
                break
            cursor.execute(
                SEARCH_UPSERT_SQL.format(where="WHERE a.ix > %s AND a.ix <= %s"),
                [last_ix, max_ix])
        total += count
        last_ix = max_ix
        log.info("antibody_search reconcile: %s rows processed", total)
    return total


def refresh_search_view():
    """
    Kept for backward compatibility: the antibody_search materialized view is
    now a table maintained by database triggers, so routine saves need no
    explicit refresh. This runs a full reconcile (see reconcile_search_table).
    """
    sync_execution = os.getenv('TEST', False)

    def reconcile_thread():
        try:
            reconcile_search_table()
        except Exception:
            log.exception("Error reconciling antibody_search")
        finally:
            connection.close()

    if not sync_execution:
        threading.Thread(target=reconcile_thread, daemon=True).start()
    else:
        reconcile_search_table()


def ensure_search_table_populated():
    """
    One-time, non-blocking fill of antibody_search after the
    materialized-view-to-table migration (0023).

    Called at application startup (ApiConfig.ready). The migration leaves the
    old view behind as antibody_search_legacy so the run-migrations init
    container is never blocked on a data fill; this copies its rows into the
    new table from a background thread and drops it.
    """
    import sys

    if os.getenv('TEST', False):
        return
    # only when serving the app: skip manage.py commands (migrate, ingest, ...)
    argv = sys.argv
    if argv and 'manage' in os.path.basename(argv[0]) and 'runserver' not in argv[1:2]:
        return
    threading.Thread(target=_populate_search_table_if_needed, daemon=True).start()


def _populate_search_table_if_needed():
    conn = connections['default']
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT pg_try_advisory_lock(%s)", [SEARCH_TABLE_FILL_LOCK])
            if not cursor.fetchone()[0]:
                return  # another process/replica is already filling
            try:
                cursor.execute(
                    "SELECT EXISTS (SELECT 1 FROM pg_matviews"
                    " WHERE matviewname = 'antibody_search_legacy')")
                if cursor.fetchone()[0]:
                    log.info("Filling antibody_search from the legacy materialized view")
                    # rows written by the sync triggers since the migration
                    # are fresher than the view: DO NOTHING on conflict
                    cursor.execute("""
                        INSERT INTO antibody_search (ix, search_vector, defining_citation, disc, status)
                        SELECT l.ix, l.search_vector, l.defining_citation, l.disc, l.status
                        FROM antibody_search_legacy l
                        JOIN api_antibody a ON a.ix = l.ix
                        ON CONFLICT (ix) DO NOTHING;
                    """)
                    cursor.execute("DROP MATERIALIZED VIEW antibody_search_legacy")
                    log.info("antibody_search filled, legacy materialized view dropped")
                cursor.execute(
                    "SELECT (NOT EXISTS (SELECT 1 FROM antibody_search))"
                    " AND EXISTS (SELECT 1 FROM api_antibody)")
                if cursor.fetchone()[0]:
                    # no legacy view to copy from (e.g. restored dump): full fill
                    log.info("antibody_search is empty: running a full reconcile")
                    reconcile_search_table()
            finally:
                cursor.execute("SELECT pg_advisory_unlock(%s)", [SEARCH_TABLE_FILL_LOCK])
    except Exception:
        log.exception("antibody_search initial fill failed")
    finally:
        conn.close()


def rechunk_catalog_number(Antibody_model):
    i = 0
    from api.models import STATUS
    with connection.cursor() as cursor:
        for antibody in Antibody_model.objects.filter(status=STATUS.CURATED).values('ix', 'catalog_num_search', 'catalog_num', 'cat_alt'):
            i = i + 1
            if i % 10000 == 0:
                print("Migrated", i)
            new_catalog_number_chunked = catalog_number_chunked(antibody['catalog_num'], antibody['cat_alt'])
            if new_catalog_number_chunked != antibody['catalog_num_search']:

                try:
                    cursor.execute(f"UPDATE api_antibody SET catalog_num_search = '{new_catalog_number_chunked}' WHERE ix={antibody['ix']};")
                except Exception as e:
                    log.exception("`%s` `%s` %s`", antibody['catalog_num_search'], antibody['catalog_num'], antibody['cat_alt'])
