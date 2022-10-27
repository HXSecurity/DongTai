"""
ASGI config for dongtai_conf project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from _typeshed import Incomplete
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dongtai_conf.settings')

application: Incomplete = get_asgi_application()
