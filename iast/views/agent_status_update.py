#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/27 下午6:23
# project: dongtai-webapi
import time

from django.db.models import Q

from base import R
from iast.base.agent import AgentEndPoint
from iast.models.agent import IastAgent


class AgentStatusUpdate(AgentEndPoint):
    def get(self, request):
        timestamp = int(time.time())
        queryset = IastAgent.objects.filter(user=request.user)
        no_heart_beat_queryset = queryset.filter((Q(server=None) & Q(latest_time__lt=(timestamp - 600))), is_running=1)
        no_heart_beat_queryset.update(is_running=0)

        heart_beat_queryset = queryset.filter(server__update_time__lt=(timestamp - 600), is_running=1)
        heart_beat_queryset.update(is_running=0)

        return R.success(msg='引擎状态更新成功')
