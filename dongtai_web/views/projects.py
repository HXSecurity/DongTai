#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

import logging

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project import IastProject
from dongtai_web.serializers.project import ProjectSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers

logger = logging.getLogger("django")

class _ProjectsArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    name = serializers.CharField(
        default=None,
        help_text=_(
            "The name of the item to be searched, supports fuzzy search."))


_SuccessSerializer = get_response_serializer(ProjectSerializer(many=True))


class Projects(UserEndPoint):
    name = "api-v1-projects"
    description = _("View item list")

    @extend_schema_with_envcheck(
        [_ProjectsArgsSerializer],
        tags=[_('Project')],
        summary=_('Projects List'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
        response_schema=_SuccessSerializer,
    )
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
