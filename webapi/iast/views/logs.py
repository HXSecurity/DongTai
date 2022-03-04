#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.admin.models import LogEntry
import logging

from dongtai.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('dongtai-webapi')


class LogsEndpoint(UserEndPoint):
    name = 'api-v1-logs'
    description = _('Log list')

    def parse_args(self, request):
        page = request.query_params.get('page', 1)
        page_size = int(request.query_params.get('pageSize', 20))
        page_size = page_size if page_size < 50 else 50
        return page, page_size, request.user

    def get(self, request):
        try:
            page, page_size, user = self.parse_args(request)
            users = self.get_auth_users(user)
            queryset = LogEntry.objects.filter(user__in=users)

            summary, page_data = self.get_paginator(queryset=queryset, page=page, page_size=page_size)
            data = []
            if page_data:
                for item in page_data:
                    data.append({
                        "log_id": item.id,
                        "user_id": item.user.id,
                        "username": item.user.username,
                        "action_time": item.action_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "content_type": item.content_type.app_labeled_name,
                        "object_id": item.object_id,
                        "object_repr": item.object_repr,
                        "action_flag": item.action_flag,
                        "change_message": item.change_message,
                    })
                return R.success(data=data, total=summary['alltotal'])
            else:
                return R.failure(msg=_('No permission to access'), status=203)
        except Exception as e:
            logger.error(e)
            return R.success(data=list(), msg=_('failure'))
