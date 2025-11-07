"""
WSGI config for the neuroglass_research project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import logging

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_baseapp.settings")
os.system("python manage.py migrate")
application = get_wsgi_application()

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
