#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webapi
import logging
from django.contrib.admin.models import LogEntry
from dongtai_common.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from drf_spectacular.utils import extend_schema

logger = logging.getLogger('dongtai-webapi')


class LogsEndpoint(UserEndPoint):
    name = 'api-v1-logs'
    description = _('Log list')

    def make_key(self, request):
        self.cache_key = f"{request.user.id}_total_logs_id"
        self.cache_key_max_id = f"{request.user.id}_max_logs_id"

    def get_query_cache(self):
        total = cache.get(self.cache_key)
        max_id = cache.get(self.cache_key_max_id)
        return total, max_id

    def set_query_cache(self, queryset):
        total = queryset.values('id').count()
        if total > 0:
            max_id = queryset.values_list('id', flat=True).order_by('-id')[0]
        else:
            max_id = 0
        cache.set(self.cache_key, total, 60 * 60)
        cache.set(self.cache_key_max_id, max_id, 60 * 60)
        return total, max_id

    def parse_args(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        page_size = page_size if page_size < 50 else 50
        return page, page_size, request.user

    @extend_schema(
        deprecated=True,
        summary="获取日志列表",
        tags=[_("Logs")]
    )
    def get(self, request):
        try:
            page, page_size, user = self.parse_args(request)

            if user.is_system_admin():
                queryset = LogEntry.objects.all()
            elif user.is_talent_admin():
                users = self.get_auth_users(user)
                user_ids = list(users.values_list('id', flat=True))
                queryset = LogEntry.objects.filter(user_id__in=user_ids)
            else:
                queryset = LogEntry.objects.filter(user=user)
            # set cache key
            self.make_key(request)
            if page == 1:
                total, max_id = self.set_query_cache(queryset)
            else:
                total, max_id = self.get_query_cache()
                if not total or not max_id:
                    total, max_id = self.set_query_cache(queryset)
            # only read log_id
            cur_data = queryset.filter(id__lte=max_id).values_list('id', flat=True).order_by('-id')[(page - 1) * page_size: page * page_size]
            cur_ids = []
            for item in cur_data:
                cur_ids.append(item)
            # read log detail
            page_data = LogEntry.objects.filter(id__in=cur_ids).order_by('-id').select_related('content_type', 'user')
            data = []
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
            return R.success(data=data, total=total)
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.success(data=list(), msg=_('failure'))
