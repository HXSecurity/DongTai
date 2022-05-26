#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai_common.endpoint import R
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import TalentAdminEndPoint


class SystemInfo(TalentAdminEndPoint):
    name = "api-v1-system-info"
    description = _("API - System Information Page")

    def get(self, request):
        return R.success()
