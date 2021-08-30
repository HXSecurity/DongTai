#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
import time

from django.db.models import Q
from dongtai.endpoint import UserEndPoint, R

from dongtai.utils import const
from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _


class AgentStatusUpdate(UserEndPoint):
    def get(self, request):
        timestamp = int(time.time())
        queryset = IastAgent.objects.filter(user=request.user)
        no_heart_beat_queryset = queryset.filter((Q(server=None) & Q(latest_time__lt=(timestamp - 600))),
                                                 online=const.RUNNING)
        no_heart_beat_queryset.update(online=0)

        heart_beat_queryset = queryset.filter(server__update_time__lt=(timestamp - 600), online=const.RUNNING)
        heart_beat_queryset.update(online=0)

        return R.success(msg=_('Engine status was updated successfully.'))
