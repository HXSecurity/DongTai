#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry
from dongtai_common.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _
import datetime


class LogClear(UserEndPoint):
    name = 'api-v1-log-clear'
    description = _('Log clear')

    def get(self, request):
        user = request.user
        now = datetime.datetime.now()

        if user.is_system_admin():
            LogEntry.objects.filter(action_time__lt=now).delete()
        elif user.is_talent_admin():
            users = self.get_auth_users(user)
            LogEntry.objects.filter(action_time__lt=now, user__in=users).delete()
        else:
            return R.failure(status=203, msg=_('no permission'))
        return R.success()
