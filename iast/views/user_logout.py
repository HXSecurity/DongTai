#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/11 15:02
# software: PyCharm
# project: webapi
import logging

from django.contrib.auth import logout
from django.http import JsonResponse
from dongtai.endpoint import AnonymousAuthEndPoint

from webapi import settings

logger = logging.getLogger("django")


class UserLogout(AnonymousAuthEndPoint):
    """
    用户登录
    """
    name = "api-v1-user-logout"
    description = "退出登录"

    def get(self, request):
        if request.user.is_active:
            logout(request)
        response = JsonResponse({
            "status": 201,
            "msg": '退出成功'
        })
        response.delete_cookie(key=settings.CSRF_COOKIE_NAME)
        return response
