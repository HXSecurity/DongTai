"""
WSGI config for dongtai_conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

NOT_GEVENT = os.environ.get("NOT_GEVENT", 'FALSE') == 'TRUE'
if not NOT_GEVENT:
    from gevent import monkey
    monkey.patch_all()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dongtai_conf.settings')

application = get_wsgi_application()
