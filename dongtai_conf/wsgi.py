"""
WSGI config for dongtai_conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from _typeshed import Incomplete
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dongtai_conf.settings')

application: Incomplete = get_wsgi_application()
