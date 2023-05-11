def refresh_search_view():
    import threading
    def refresh_search_view_thread():
        cursor = connection.cursor()
        cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY antibody_search;")
    threading.Thread(target=refresh_search_view_thread).start()