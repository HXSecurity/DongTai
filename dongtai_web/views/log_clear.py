#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry
from dongtai_common.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _


class LogClear(UserEndPoint):
    name = 'api-v1-log-clear'
    description = _('Log clear')

    def get(self, request):
        user = request.user
        if user.is_system_admin():
            LogEntry.objects.all().delete()
        # else:
        #     LogEntry.objects.filter(user=request.user).delete()

        return R.success()
