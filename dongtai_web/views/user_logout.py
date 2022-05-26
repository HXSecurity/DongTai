#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/11 15:02
# software: PyCharm
# project: webapi
import logging

from django.contrib.auth import logout
from django.http import JsonResponse
from dongtai_common.endpoint import AnonymousAuthEndPoint
from django.utils.translation import gettext_lazy as _

from dongtai_conf import settings

logger = logging.getLogger("django")
from datetime import datetime

class UserLogout(AnonymousAuthEndPoint):
    name = "api-v1-user-logout"
    description = _("Sign out")

    def get(self, request):
        if request.user.is_active:
            logout(request)
        response = JsonResponse({
            "status": 201,
            "msg": _('Sign out successfully')
        })
        response.delete_cookie(key=settings.CSRF_COOKIE_NAME,domain=settings.SESSION_COOKIE_DOMAIN)
        response.delete_cookie(key='sessionid',domain=settings.SESSION_COOKIE_DOMAIN)
        return response
