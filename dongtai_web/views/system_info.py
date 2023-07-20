#!/usr/bin/env python
# -*- coding:utf-8 -*-

from dongtai_common.endpoint import R
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import TalentAdminEndPoint


class SystemInfo(TalentAdminEndPoint):
    name = "api-v1-system-info"
    description = _("API - System Information Page")

    @extend_schema(summary=_("API - System Information Page"), tags=[_("System")])
    def get(self, request):
        return R.success()
