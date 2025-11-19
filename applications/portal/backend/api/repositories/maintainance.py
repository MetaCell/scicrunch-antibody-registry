import os
from django.db import connection
from cloudharness import log
from api.utilities.functions import catalog_number_chunked


def refresh_antibody_stats():
    """
    Refresh the antibody statistics cache table for CURATED antibodies only.
    Runs in a separate thread to avoid blocking the main request.
    """
    import threading
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


def refresh_search_view():
    import threading
    sync_execution = os.getenv('TEST', False)

    def refresh_search_view_thread():
        log.info("Refreshing search view")
        with connection.cursor() as cursor:
            cursor.execute(f"REFRESH MATERIALIZED VIEW {'CONCURRENTLY' if not sync_execution else ''} antibody_search;")
        if not sync_execution:
            connection.commit()
    if not sync_execution:
        threading.Thread(target=refresh_search_view_thread).start()
    else:
        refresh_search_view_thread()


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
