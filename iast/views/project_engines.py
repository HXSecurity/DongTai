#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/8 下午12:03
# software: PyCharm
# project: lingzhi-webapi

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent


class ProjectEngines(UserEndPoint):
    name = "api-v1-project-engines"
    description = "查看引擎列表"

    def get(self, request, pid):
        auth_users = self.get_auth_users(request.user)
        queryset = IastAgent.objects.filter(user__in=auth_users, is_running=1, bind_project_id__in=[0, pid]).values(
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
