from django.db import connection
from cloudharness import log

def refresh_search_view():
    import threading
    def refresh_search_view_thread():
        log.info("Refreshing search view")
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY antibody_search;")
    threading.Thread(target=refresh_search_view_thread).start()