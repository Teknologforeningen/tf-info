"""
WSGI config for info_reborn project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ENV = sys.path.append(os.path.join(BASE_DIR,'../.env'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import dotenv
dotenv.read_dotenv(ENV)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
