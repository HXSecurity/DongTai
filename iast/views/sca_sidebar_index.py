#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:15
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Q

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset


class ScaSidebarList(UserEndPoint):
    def get(self, request):
        """
        获取三方组件列表
        - 支持排序
        - 支持搜索
        - 支持分页
        :param request:
        :return:
        """
        # 提取过滤条件：
        language = request.query_params.get('language', None)
        level = request.query_params.get('level', None)
        app_name = request.query_params.get('app', None)
        order = request.query_params.get('order', None)

        condition = Q(user=request.user)
        if language:
            condition = condition & Q(language=language)
        if level:
            condition = condition & Q(level=level)
        if app_name:
            condition = condition & Q(app_name=app_name)

        if order:
            queryset = Asset.objects.values(
                'package_name',
                'version',
                'language',
                'level',
                'dt'
            ).filter(condition).order_by(order)
        else:
            queryset = Asset.objects.values(
                'package_name',
                'version',
                'language',
                'level',
                'dt'
            ).filter(condition).order_by('-dt')

        page_size = 10
        page_summary, queryset = self.get_paginator(queryset, page_size=page_size)
        return R.success(data=queryset, page=page_summary, total=page_summary['alltotal'])
