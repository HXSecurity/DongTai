#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/13 下午5:56
# project: dongtai-webapi
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from base import R
from iast.base.user import UserTokenEndPoint
from iast.serializers.vul import VulForPluginSerializer


class VulnListEndPoint(UserTokenEndPoint):
    def get(self, request):
        agent_name = request.query_params.get('name')
        if not agent_name:
            return R.failure(msg="please input agent name.")

        agent = IastAgent.objects.filter(
            token=agent_name,
            id__in=self.get_auth_agents_with_user(request.user)
        ).first()
        if not agent:
            return R.failure(msg="Not found agent_name!")

        queryset = IastVulnerabilityModel.objects.values('id', 'type', 'url', 'http_method', 'top_stack',
                                                         'bottom_stack').filter(
            agent=agent)

        if queryset:
            url = request.query_params.get('url')
            if url and url != '':
                queryset = queryset.filter(url__icontains=url)

            order = request.query_params.get('order', '-latest_time')
            if order:
                queryset = queryset.order_by(order)

            page = request.query_params.get('page', 1)
            page_size = request.query_params.get("pageSize", 20)
            page_summary, page_data = self.get_paginator(queryset, page, page_size)

            return R.success(page=page_summary, data=VulForPluginSerializer(page_data, many=True).data)
        else:
            return R.success(page=[], data=[])
