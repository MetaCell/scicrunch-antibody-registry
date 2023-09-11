import os
import logging 

from django.db import migrations


def create_kc_client_and_roles(apps, schema_editor):
    if os.environ.get("KUBERNETES_SERVICE_HOST", None):
        # running in K8S so create the KC client and roles
        
        from cloudharness_django.services import get_auth_service, get_user_service, init_services

        init_services()
        try:
            get_auth_service().create_client()
        except:
            logging.error("Cannot create client", exc_info=True)
        try:
            get_user_service().sync_kc_users_groups()
        except:
            logging.error("Cannot sync roles and services", exc_info=True)


class Migration(migrations.Migration):

    dependencies = [
        ("cloudharness_django", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_kc_client_and_roles),
    ]
