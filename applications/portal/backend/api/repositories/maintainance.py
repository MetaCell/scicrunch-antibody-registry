from django.db import connection


def refresh_search_view():
    import threading
    def refresh_search_view_thread():
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY antibody_search;")
    threading.Thread(target=refresh_search_view_thread).start()