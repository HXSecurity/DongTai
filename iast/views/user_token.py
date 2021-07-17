#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 15:03
# software: PyCharm
# project: webapi
import logging

from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from base import R
from iast.base.user import UserEndPoint
from webapi import settings

logger = logging.getLogger("django")


class UserToken(UserEndPoint):
    """
    当前用户详情
    """
    # 必须设置
    name = "iast-v1-user-token"
    description = "获取OpenApi Token"

    def get(self, request):
        token, success = Token.objects.get_or_create(user=request.user)

        if not request.user.upgrade_url:
            upgrade_url = settings.AGENT_UPGRADE_URL
        else:
            upgrade_url = request.user.upgrade_url

        return R.success(token=token.key, upgrade_url=upgrade_url)
