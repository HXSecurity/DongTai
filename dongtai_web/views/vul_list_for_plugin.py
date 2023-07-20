#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.vulnerablity import IastVulnerabilityModel

from dongtai_common.endpoint import R
from dongtai_common.endpoint import MixinAuthEndPoint
from dongtai_web.serializers.vul import VulForPluginSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from dongtai_web.utils import get_model_order_options

_ResponseSerializer = get_response_serializer(VulForPluginSerializer(many=True))


class VulListEndPoint(MixinAuthEndPoint):
    @extend_schema_with_envcheck(
        [
            {
                "name": "page",
                "type": int,
                "default": 1,
                "required": False,
                "description": _("Page index"),
            },
            {
                "name": "pageSize",
                "type": int,
                "default": 20,
                "required": False,
                "description": _("Number per page"),
            },
            {
                "name": "name",
                "type": str,
                "description": _("Name of agent"),
            },
            {
                "name": "url",
                "type": str,
                "description": _("The URL corresponding to the vulnerability"),
            },
            {
                "name": "order",
                "type": str,
                "description": format_lazy(
                    "{} : {}",
                    _("Sorted index"),
                    ",".join(
                        [
                            "id",
                            "hook_type_id",
                            "url",
                            "http_method",
                            "top_stack",
                            "bottom_stack",
                        ]
                    ),
                ),
            },
        ],
        tags=[_("Vulnerability")],
        summary=_("Vulnerability List (with agent name)"),
        description=_(
            "Use the agent name to get the corresponding list of vulnerabilities"
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        agent_name = request.query_params.get("name", None)
        departmenttoken = request.query_params.get("departmenttoken", "")
        projectname = request.query_params.get("projectname", "")
        department = request.user.get_relative_department()
        if not agent_name:
            return R.failure(msg=_("Please input agent name."))
        departmenttoken = departmenttoken.replace("GROUP", "")
        agent = IastAgent.objects.filter(
            token=agent_name,
            department__token=departmenttoken,
            bind_project__name=projectname,
        ).last()
        if not agent:
            return R.failure(msg=_("agent_name not found"))

        queryset = IastVulnerabilityModel.objects.values(
            "id",
            "strategy_id",
            "hook_type_id",
            "url",
            "http_method",
            "top_stack",
            "bottom_stack",
            "level_id",
        ).filter(agent=agent)

        if queryset:
            url = request.query_params.get("url", None)
            if url and url != "":
                queryset = queryset.filter(url__icontains=url)

            order = request.query_params.get("order", "-latest_time")
            if order and order in get_model_order_options(IastVulnerabilityModel):
                queryset = queryset.order_by(order)

            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("pageSize", 20))
            page_summary, page_data = self.get_paginator(queryset, page, page_size)

            return R.success(
                page=page_summary,
                data=VulForPluginSerializer(page_data, many=True).data,
            )
        else:
            return R.success(page=[], data=[])
