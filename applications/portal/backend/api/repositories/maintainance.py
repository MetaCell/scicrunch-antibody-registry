from django.db import connection
from cloudharness import log
from api.utilities.functions import catalog_number_chunked


def refresh_search_view():
    import threading
    def refresh_search_view_thread():
        log.info("Refreshing search view")
        with connection.cursor() as cursor:
            cursor.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY antibody_search;")
        connection.commit()
    threading.Thread(target=refresh_search_view_thread).start()


def rechunk_catalog_number(apps, schema_editor):
    Antibody = apps.get_model('api', 'Antibody')
    with connection.cursor() as cursor:
        for antibody in Antibody.objects.all().values('ix', 'catalog_num_search', 'catalog_num', 'cat_alt'):
            new_catalog_number_chunked = catalog_number_chunked(antibody['catalog_num'], antibody['cat_alt'])
            if new_catalog_number_chunked != antibody['catalog_num_search']:
                cursor.execute(f"UPDATE api_antibody SET catalog_num_search = {new_catalog_number_chunked} WHERE ix={antibody['ix']};") 
    connection.commit()
