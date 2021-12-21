#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
import logging

from django.contrib.auth.models import Group

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class UserInfoEndpoint(UserEndPoint):
    name = "api-v1-user-info"
    description = _("User Info")

    def get(self, request):
        user = request.user
        group = Group.objects.filter(user=user).order_by("-id").first()

        return R.success(data={
            'userid': user.id if not user.is_anonymous else -1 ,
            'username': user.get_username(),
            'role': 2 if group.name == 'talent_admin' else 1 if group.name == 'system_admin' else 0,
            'role_name': group.name
        })
