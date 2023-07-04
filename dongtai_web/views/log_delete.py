#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from django.contrib.admin.models import LogEntry
from dongtai_common.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema


class LogDelete(UserEndPoint):
    name = 'api-v1-log-delete'
    description = _('Log delete')

    @extend_schema(
        deprecated=True,
        summary=_('Log delete'),
        tags=[_("Logs")]
    )
    def post(self, request):
        ids = request.data.get('ids')
        if ids:
            ids = [int(id.strip()) for id in ids.split(',')]
            user = request.user
            if user.is_superuser == 1:
                LogEntry.objects.filter(id__in=ids).delete()
                return R.success(msg=_('success'))
            users = self.get_auth_users(user)
            user_ids = list(users.values_list('id', flat=True))
            LogEntry.objects.filter(id__in=ids, user_id__in=user_ids).delete()
            return R.success(msg=_('success'))
        else:
            return R.failure(status=203, msg=_('The data to be deleted should not be empty'))
