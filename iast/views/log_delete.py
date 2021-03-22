#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/5 下午1:22
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry

from base import R
from iast.base.user import UserEndPoint


class LogDelete(UserEndPoint):
    name = 'api-v1-log-delete'
    description = '日志删除'

    def post(self, request):
        ids = request.data.get('ids')
        if ids:
            ids = [int(id.strip()) for id in ids.split(',')]

            user = request.user
            if user.is_talent_admin():
                LogEntry.objects.filter(id__in=ids).delete()
            else:
                LogEntry.objects.filter(id__in=ids, user=user).delete()

            return R.success(msg='success')
        else:
            return R.failure(status=203, msg='待删除的数据不能为空')
