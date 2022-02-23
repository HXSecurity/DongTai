#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.contrib.admin.models import LogEntry
import logging

from dongtai.endpoint import UserEndPoint, R
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from math import ceil
logger = logging.getLogger('dongtai-webapi')


class LogsEndpoint(UserEndPoint):
    name = 'api-v1-logs'
    description = _('Log list')

    def parse_args(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        page_size = page_size if page_size < 50 else 50
        return page, page_size, request.user

    def get(self, request):
        try:
            page, page_size, user = self.parse_args(request)
            users = self.get_auth_users(user)
            user_ids = list(users.values_list('id',flat=True))
            queryset = LogEntry.objects.filter(user__in=users)
            cache_key = f"{request.user.id}_{page_size}_logs_id"
            data_in_cache = cache.get(cache_key)
            if not data_in_cache:
                total = LogEntry.objects.filter(
                    user_id__in=user_ids).values('id').count()
                max_id = LogEntry.objects.filter(user_id__in=user_ids).values_list(
                        'id', flat=True).order_by('-action_time')[0]
                log_ids = list(
                    LogEntry.objects.filter(user_id__in=user_ids).values_list(
                        'id', flat=True).order_by('-action_time')
                    [(page_size) * (int(page) - 1):(page_size) *
                     (int(page) - 1) + page_size * 5])
                page_dict = {}
                num_pages = ceil(total / page)
                for page_num in range(page, page + 5):
                    log_id_chunk = log_ids[page_size *
                                           (page_num - 1):page_size *
                                           (page_num - 1) + page_size]
                    page_dict[page_num] = log_id_chunk
                data_in_cache = {
                    'page_summary': {
                        "alltotal": total,
                        "num_pages": num_pages,
                        "page_size": page_size
                    },
                    'page_dict': page_dict,
                    'max_id': max_id,
                }
                cache.set(cache_key,data_in_cache,60)
                final_log_ids = data_in_cache['page_dict'][page]
            elif not data_in_cache.get('page_dict', {}).get(page, []):
                log_ids = list(
                    LogEntry.objects.filter(
                        user_id__in=user_ids,
                        pk__lte=data_in_cache['max_id']).values_list(
                            'id', flat=True).order_by('-action_time')
                    [(page_size) * (int(page) - 1):(page_size) *
                     (int(page) - 1) + page_size * 5])
                data_in_cache['page_dict'][page] = log_ids
                cache.set(cache_key,data_in_cache,60)
                final_log_ids = data_in_cache['page_dict'][page]
            else:
                final_log_ids = data_in_cache['page_dict'][page]
            page_data = LogEntry.objects.filter(
                pk__in=final_log_ids).select_related('content_type', 'user')
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
                return R.success(data=data, total=data_in_cache['page_summary']['alltotal'])
            else:
                return R.failure(msg=_('No permission to access'), status=203)
        except Exception as e:
            logger.error(e,exc_info=True)
            return R.success(data=list(), msg=_('failure'))
