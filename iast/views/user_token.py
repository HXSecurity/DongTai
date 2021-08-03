#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 15:03
# software: PyCharm
# project: webapi
import logging

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from rest_framework.authtoken.models import Token

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

        return R.success(data={'token': token.key})
