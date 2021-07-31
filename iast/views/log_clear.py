#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/5 下午1:23
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry
from dongtai.endpoint import UserEndPoint, R


class LogClear(UserEndPoint):
    name = 'api-v1-log-clear'
    description = '日志清空'

    def get(self, request):
        user = request.user
        if user.is_talent_admin():
            LogEntry.objects.all().delete()
        else:
            LogEntry.objects.filter(user=request.user).delete()

        return R.success()
