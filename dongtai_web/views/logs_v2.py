#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webapi
import logging
from datetime import datetime

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.log import IastLog
from dongtai_common.models.user import User

logger = logging.getLogger("dongtai-webapi")


class _LogsArgsSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(min_value=1, default=1, help_text=_("Page index"))
    startTime = serializers.DateTimeField(default=None, help_text=_("The start time."))
    endTime = serializers.DateTimeField(default=None, help_text=_("The end time."))


class _LogsDeleteSerializer(serializers.Serializer):
    ids = serializers.Field(default=None, help_text=_("Log ids to delete"))


class LogsV2Endpoint(UserEndPoint):
    name = "api-v2-logs"
    description = _("Log list")

    def make_key(self, request):
        self.cache_key = f"{request.user.id}_total_logs_id"
        self.cache_key_max_id = f"{request.user.id}_max_logs_id"

    def get_query_cache(self):
        total = cache.get(self.cache_key)
        max_id = cache.get(self.cache_key_max_id)
        return total, max_id

    def set_query_cache(self, queryset):
        total = queryset.values("id").count()
        if total > 0:
            max_id = queryset.values_list("id", flat=True).order_by("-id")[0]
        else:
            max_id = 0
        cache.set(self.cache_key, total, 60 * 60)
        cache.set(self.cache_key_max_id, max_id, 60 * 60)
        return total, max_id

    @extend_schema(
        parameters=[_LogsArgsSerializer],
        description="Get List of logs.",
        summary="Log List",
        tags=["Logs"],
    )
    def get(self, request: Request) -> JsonResponse:
        ser = _LogsArgsSerializer(data=request.GET)
        user: User = request.user  # type: ignore
        try:
            if ser.is_valid(True):
                page: int = ser.validated_data.get("page", 1)
                page_size: int = ser.validated_data.get("pageSize", 20)
                start_time: datetime | None = ser.validated_data.get("startTime", None)
                end_time: datetime | None = ser.validated_data.get("endTime", None)
            else:
                return R.failure(data="Can not validation data.")
        except ValidationError as e:
            return R.failure(data=e.detail)

        try:
            if user.is_system_admin():
                queryset = IastLog.objects.all()
            elif user.is_talent_admin():
                users = self.get_auth_users(user)
                user_ids = list(users.values_list("id", flat=True))
                queryset = IastLog.objects.filter(user_id__in=user_ids)
            else:
                queryset = IastLog.objects.filter(user=user)

            if start_time is not None and end_time is not None:
                queryset = queryset.filter(action_time__range=(start_time, end_time))
            elif start_time is not None:
                queryset = queryset.filter(action_time__gte=start_time)
            elif end_time is not None:
                queryset.filter(action_time__lte=end_time)

            # set cache key
            self.make_key(request)
            if page == 1:
                total, max_id = self.set_query_cache(queryset)
            else:
                total, max_id = self.get_query_cache()
                if not total or not max_id:
                    total, max_id = self.set_query_cache(queryset)
            # only read log_id
            cur_data = (
                queryset.filter(id__lte=max_id)
                .values_list("id", flat=True)
                .order_by("-id")[(page - 1) * page_size : page * page_size]
            )
            cur_ids = []
            for item in cur_data:
                cur_ids.append(item)
            # read log detail
            page_data = (
                IastLog.objects.filter(id__in=cur_ids)
                .order_by("-id")
                .select_related("user")
            )
            data = []
            for item in page_data:
                data.append(
                    {
                        "log_id": item.id,
                        "user_id": item.user.id,
                        "username": item.user.username,
                        "action_time": item.action_time.strftime("%Y-%m-%d %H:%M:%S"),
                        "module_name": item.module_name,
                        "function_name": item.function_name,
                        "operate_type": item.operate_type,
                        "access_ip": item.access_ip,
                    }
                )
            return R.success(data=data, total=total)
        except Exception as e:
            logger.error(e, exc_info=True)
            return R.success(data=list(), msg=_("failure"))

    @extend_schema(
        parameters=[_LogsDeleteSerializer],
        description="Delete Logs. "
        "Query param ids is optional, if not set ids, will delete all logs",
        summary="Delete Logs",
        tags=["Logs"],
    )
    def delete(self, request: Request) -> JsonResponse:
        ids: str | None = request.query_params.get("ids", None)
        user: User = request.user  # type: ignore
        if ids:
            id_list = [int(id.strip()) for id in ids.split(",")]
            if user.is_superuser == 1:
                IastLog.objects.filter(id__in=id_list).delete()
                return R.success(msg=_("success"))
            users = self.get_auth_users(user)
            user_ids = list(users.values_list("id", flat=True))
            IastLog.objects.filter(id__in=id_list, user_id__in=user_ids).delete()
            return R.success(msg=_("success"))
        else:
            now = datetime.now()
            if user.is_system_admin():
                IastLog.objects.filter(action_time__lt=now).delete()
            elif user.is_talent_admin():
                users = self.get_auth_users(user)
                IastLog.objects.filter(action_time__lt=now, user__in=users).delete()
            else:
                return R.failure(status=203, msg=_("no permission"))
            return R.success()
