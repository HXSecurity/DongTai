#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/25 15:03
# software: PyCharm
# project: webapi
import logging

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger("django")


class UserToken(UserEndPoint):
    name = "iast-v1-user-token"
    description = _("Get OpenAPI token")

    def get(self, request):
        token, success = Token.objects.get_or_create(user=request.user)

        return R.success(data={'token': token.key})
