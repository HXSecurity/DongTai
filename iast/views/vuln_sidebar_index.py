#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:15
# software: idea
# project: lingzhi-webapi
from django.db.models import Q
from rest_framework.request import Request

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.vulnerablity import IastVulnerabilityModel


class VulnSideBarList(UserEndPoint):
    def get(self, request: Request):
        """
        获取漏洞列表
        - 支持排序
        - 支持搜索
        - 支持分页
        :param request:
        :return:
        """
        queryset = IastVulnerabilityModel.objects.values(
            'app_name',
            'server_name',
            'level',
            'latest_time',
            'language',
            'type',
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
        if order:
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-latest_time')

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        page_summary, queryset = self.get_paginator(queryset, page=page, page_size=page_size)

        return R.success(page=page_summary, total=page_summary['alltotal'], data=queryset)
