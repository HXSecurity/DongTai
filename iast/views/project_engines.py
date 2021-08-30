#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _


class ProjectEngines(UserEndPoint):
    name = "api-v1-project-engines"
    description = _("View engine list")

    def get(self, request, pid):
        auth_users = self.get_auth_users(request.user)
        queryset = IastAgent.objects.filter(user__in=auth_users, online=const.RUNNING, bind_project_id__in=[0, pid]).values(
            "id", "token")
        data = []
        if queryset:
            for item in queryset:
                data.append({
                    'id': item['id'],
                    'token': item['token'],
                    'short_name': '-'.join(item['token'].split('-')[:-1]),
                })
        return R.success(data=data)
