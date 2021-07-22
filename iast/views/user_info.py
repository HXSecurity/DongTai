#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午2:58
# software: PyCharm
# project: lingzhi-webapi
import logging

from django.contrib.auth.models import Group

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint

logger = logging.getLogger("django")


class UserInfoEndpoint(UserEndPoint):
    """
    用户登录
    """
    name = "api-v1-user-info"
    description = "用户信息"

    def get(self, request):
        user = request.user
        group = Group.objects.filter(user=user).order_by("-id").first()

        return R.success(data={
            'username': user.get_username(),
            'role': 2 if group.name == 'talent_admin' else 1 if group.name == 'system_admin' else 0,
            'role_name': group.name
        })
