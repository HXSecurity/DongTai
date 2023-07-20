#!/usr/bin/env python
# datetime:2020/8/11 15:02
import logging
from datetime import datetime

from django.contrib.auth import logout
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import AnonymousAuthEndPoint
from dongtai_conf import settings

logger = logging.getLogger("django")


class UserLogout(AnonymousAuthEndPoint):
    name = "api-v1-user-logout"
    description = _("Sign out")

    @extend_schema(
        summary=_("Sign out"),
        tags=[_("User")],
    )
    def get(self, request):
        logout(request)
        response = JsonResponse({"status": 201, "msg": _("Sign out successfully")})
        request.session.delete()
        response.delete_cookie(
            key=settings.CSRF_COOKIE_NAME, domain=settings.SESSION_COOKIE_DOMAIN
        )
        response.delete_cookie(key="sessionid", domain=settings.SESSION_COOKIE_DOMAIN)
        return response
