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
from iast.models.vulnerablity import IastVulnerabilityModel


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
        # 提取过滤条件：
        user_id = 1
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 10)
        language = request.query_params.get('language', None)
        level = request.query_params.get('level', None)
        type = request.query_params.get('type', None)
        app_name = request.query_params.get('app', None)
        url = request.query_params.get('url', None)
        order = request.query_params.get('order', None)
        # 如果django ORM的order_by方法存在漏洞，则增加此限制，暂时不进行限制
        # if order is not None and order not in ['vul_app', '-vul_app']:
        #    end['status'] = '202'
        #    return R.failure(status=202)

        condition = Q(user_id=user_id)
        if language:
            condition = condition & Q(language=language)
        if level:
            condition = condition & Q(level=level)
        if type:
            condition = condition & Q(type=type)
        if app_name:
            condition = condition & Q(app_name=app_name)
        if url:
            condition = condition & Q(url=url)

        if order:
            datas = IastVulnerabilityModel.objects.values(
                'app_name',
                'server_name',
                'level',
                'latest_time',
                'language',
                'type',
                'uri',
            ).filter(condition).order_by(order)
        else:
            datas = IastVulnerabilityModel.objects.values(
                'app_name',
                'server_name',
                'level',
                'latest_time',
                'language',
                'type',
                'uri',
            ).filter(condition).order_by('-latest_time')

        page_summary, queryset = self.get_paginator(datas, page=page, page_size=page_size)

        return R.success(page=page_summary, total=page_summary['alltotal'], data=queryset)
