#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:40
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import TalentAdminEndPoint


class SystemInfo(TalentAdminEndPoint):
    name = "api-v1-system-info"
    description = "api - 系统信息页面"

    def get(self, request):
        return R.success()
