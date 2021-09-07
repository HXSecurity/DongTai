#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

import logging

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.project import IastProject
from iast.serializers.project import ProjectSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck

logger = logging.getLogger("django")


class Projects(UserEndPoint):
    name = "api-v1-projects"
    description = _("View item list")

    @extend_schema_with_envcheck([{
        'name': "name",
        'type': str,
    }])
    def get(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 20)
        name = request.query_params.get('name')

        users = self.get_auth_users(request.user)
        queryset = IastProject.objects.filter(
            user__in=users).order_by('-latest_time')

        if name:
            queryset = queryset.filter(name__icontains=name)

        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=ProjectSerializer(page_data, many=True).data,
                         page=page_summary)
