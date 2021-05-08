#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 上午10:52
# software: PyCharm
# project: lingzhi-webapi

import logging

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.project import IastProject
from iast.serializers.project import ProjectSerializer

logger = logging.getLogger("django")


class Projects(UserEndPoint):
    """
    创建用户，默认只能创建普通用户
    """
    name = "api-v1-projects"
    description = "查看项目列表"

    def get(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 20)
        name = request.query_params.get('name')

        users = self.get_auth_users(request.user)
        queryset = IastProject.objects.filter(user__in=users).order_by('-latest_time')

        if name:
            queryset = queryset.filter(name__icontains=name)

        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=ProjectSerializer(page_data, many=True).data, page=page_summary)
