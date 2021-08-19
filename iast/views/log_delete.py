#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry
from dongtai.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _


class LogDelete(UserEndPoint):
    name = 'api-v1-log-delete'
    description = _('Log delete')

    def post(self, request):
        ids = request.data.get('ids')
        if ids:
            ids = [int(id.strip()) for id in ids.split(',')]

            user = request.user
            if user.is_talent_admin():
                LogEntry.objects.filter(id__in=ids).delete()
            else:
                LogEntry.objects.filter(id__in=ids, user=user).delete()

            return R.success(msg=_('success'))
        else:
            return R.failure(status=203, msg=_('The data to be deleted should not be empty'))
