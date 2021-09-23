#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai.models.agent import IastAgent
from dongtai.models.vulnerablity import IastVulnerabilityModel

from dongtai.endpoint import R
from dongtai.endpoint import MixinAuthEndPoint
from iast.serializers.vul import VulForPluginSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import get_model_order_options


class VulListEndPoint(MixinAuthEndPoint):
    def get(self, request):
        agent_name = request.query_params.get('name')
        if not agent_name:
            return R.failure(msg=_("Please input agent name."))

        agent = IastAgent.objects.filter(
            token=agent_name,
            id__in=self.get_auth_agents_with_user(request.user)
        ).first()
        if not agent:
            return R.failure(msg=_("agent_name not found"))

        queryset = IastVulnerabilityModel.objects.values('id', 'hook_type_id', 'url', 'http_method', 'top_stack',
                                                         'bottom_stack').filter(
            agent=agent)

        if queryset:
            url = request.query_params.get('url')
            if url and url != '':
                queryset = queryset.filter(url__icontains=url)

            order = request.query_params.get('order', '-latest_time')
            if order and order in get_model_order_options(IastVulnerabilityModel):
                queryset = queryset.order_by(order)

            page = request.query_params.get('page', 1)
            page_size = request.query_params.get("pageSize", 20)
            page_summary, page_data = self.get_paginator(queryset, page, page_size)

            return R.success(page=page_summary, data=VulForPluginSerializer(page_data, many=True).data)
        else:
            return R.success(page=[], data=[])
