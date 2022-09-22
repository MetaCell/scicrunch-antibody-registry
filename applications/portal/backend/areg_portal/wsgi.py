"""
WSGI config for the areg_portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "areg_portal.settings")

application = get_wsgi_application()

# init the auth service
from cloudharness_django.services import init_services

init_services()

# start the kafka event listener
import cloudharness_django.services.events
