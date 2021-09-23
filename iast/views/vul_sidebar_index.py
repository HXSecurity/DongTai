#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: idea
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType
from iast.utils import get_model_order_options

class VulSideBarList(UserEndPoint):
    def get(self, request):
        """
        :param request:
        :return:
        """
        queryset = IastVulnerabilityModel.objects.values(
            'app_name',
            'server_name',
            'level',
            'latest_time',
            'language',
            'hook_type_id',
            'uri',
        ).filter(agent__in=self.get_auth_agents_with_user(request.user))

        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)

        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        type = request.query_params.get('type')
        if type:
            queryset = queryset.filter(type=type)

        app_name = request.query_params.get('app')
        if app_name:
            queryset = queryset.filter(app_name=app_name)

        url = request.query_params.get('url')
        if url:
            queryset = queryset.filter(url=url)

        order = request.query_params.get('order')
        if order and order in get_model_order_options(IastVulnerabilityModel):
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-latest_time')

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        page_summary, queryset = self.get_paginator(queryset, page=page, page_size=page_size)
        for obj in queryset:
            hook_type = HookType.objects.filter(pk=obj['hook_type_id']).first()
            return hook_type.name if hook_type else ''
        return R.success(page=page_summary,
                         total=page_summary['alltotal'],
                         data=queryset)
