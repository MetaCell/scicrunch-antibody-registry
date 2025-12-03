"""
ASGI config for the MNP Checkout project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import logging

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_baseapp.settings")

# migrate the Django models
os.system("python manage.py migrate")


application = get_asgi_application()

from cloudharness_django.services import init_services  # noqa E402

init_services()


if os.environ.get("USERS_SYNC", None):
    try:
        # init the auth service

        # start the kafka event listener
        from cloudharness_django.services.events import init_listener  # noqa E402

        init_listener()
    except Exception as e:
        logging.exception("Error starting the services")
