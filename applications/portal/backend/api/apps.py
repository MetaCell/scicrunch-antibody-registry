from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from api.signals import clear_antibody_cache
        from api.repositories.maintainance import ensure_search_table_populated
        # one-time background fill of antibody_search after migration 0023
        # (no-op once filled)
        ensure_search_table_populated()
        # Register exception handlers after app is ready
        # Temporarily commented out to test
        # from api.api import api
        # from api.helpers.response_helpers import add_exception_handlers
        # add_exception_handlers(api)
        return super().ready()