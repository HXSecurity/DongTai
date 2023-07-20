#!/usr/bin/env python
from typing import Any
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.strategy import IastStrategyModel

from dongtai_web.base.agent import (
    get_agents_with_project,
    get_user_project_name,
    get_user_agent_pro,
    get_all_server,
)
from dongtai_web.base.project_version import (
    get_project_version,
    get_project_version_by_id,
)
from dongtai_web.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from dongtai_common.models.hook_type import HookType
from django.db.models import Q
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

from django.utils.text import format_lazy

from dongtai_web.utils import get_model_order_options
from rest_framework import serializers


class _VulsEndPointResponseSerializer(VulSerializer):
    index = serializers.IntegerField()
    project_name = serializers.CharField(
        help_text=_("name of project"), default=_("The application has not been binded")
    )
    project_id = serializers.IntegerField(help_text=_("Id of Project"), default=0)
    server_name = serializers.CharField(default="JavaApplication")
    server_type = serializers.CharField()
    level_type = serializers.IntegerField()
    level = serializers.CharField()

    class Meta:
        model = VulSerializer.Meta.model
        fields = [
            *VulSerializer.Meta.fields,
            "index",
            "project_name",
            "project_id",
            "server_name",
            "server_type",
            "level_type",
            "level",
        ]


_ResponseSerializer = get_response_serializer(
    _VulsEndPointResponseSerializer(many=True)
)


class VulsEndPoint(UserEndPoint):
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
            {"name": "language", "type": str, "description": _("programming language")},
            {
                "name": "type",
                "type": str,
                "description": _("Type of vulnerability"),
            },
            {
                "name": "project_name",
                "type": str,
                "deprecated": True,
                "description": _("name of project"),
            },
            {
                "name": "level",
                "type": int,
                "deprecated": True,
                "description": format_lazy(
                    "{} : {}", _("Level of vulnerability"), "1,2,3,4"
                ),
            },
            {
                "name": "level",
                "type": int,
                "description": format_lazy(
                    "{} : {}", _("The id Level of vulnerability"), "1,2,3,4"
                ),
            },
            {
                "name": "project_id",
                "type": int,
                "description": _("Id of Project"),
            },
            {
                "name": "version_id",
                "type": int,
                "description": _(
                    "The default is the current version id of the project."
                ),
            },
            {
                "name": "status",
                "type": str,
                "deprecated": True,
                "description": _("Name of status"),
            },
            {
                "name": "status_id",
                "type": int,
                "description": _("Id of status"),
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
                    "type,level,first_time,latest_time,url",
                ),
            },
        ],
        [],
        [
            {
                "name": _("Get data sample"),
                "description": _(
                    "The aggregation results are programming language, risk level, vulnerability type, project"
                ),
                "value": {
                    "status": 201,
                    "msg": "success",
                    "data": [
                        {
                            "id": 12024,
                            "type": "Weak Random Number Generation",
                            "hook_type_id": 45,
                            "url": "http://localhost:81/captcha/captchaImage",
                            "uri": "/captcha/captchaImage",
                            "agent_id": 820,
                            "level_id": 3,
                            "http_method": "GET",
                            "top_stack": None,
                            "bottom_stack": None,
                            "taint_position": None,
                            "latest_time": 1631092302,
                            "first_time": 1631092263,
                            "language": "JAVA",
                            "status": "Confirmed",
                            "index": 0,
                            "project_name": "demo",
                            "project_id": 71,
                            "server_name": "Apache Tomcat/9.0.41",
                            "server_type": "apache tomcat",
                            "level_type": 3,
                            "level": "LOW",
                        }
                    ],
                    "page": {"alltotal": 1, "num_pages": 1, "page_size": 20},
                },
            }
        ],
        tags=[_("Vulnerability")],
        summary=_("Vulnerability List (with project)"),
        response_schema=_ResponseSerializer,
        description=_("Get the list of vulnerabilities corresponding to the project"),
    )
    def get(self, request):
        """
        :param request:
        :return:
        """
        end = {"status": 201, "msg": "success", "data": []}
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        try:
            page = int(request.query_params.get("page", 1))
            page_size = int(request.query_params.get("pageSize", 20))
        except ValueError:
            return R.failure(_("Parameter error"))
        if auth_agents is None:
            return R.success(page={}, data=[], msg=_("No data"))

        language = request.query_params.get("language")
        if language:
            auth_agents = auth_agents.filter(language=language)

        queryset = IastVulnerabilityModel.objects.values(
            "id",
            "hook_type_id",
            "url",
            "uri",
            "agent_id",
            "level_id",
            "http_method",
            "top_stack",
            "bottom_stack",
            "taint_position",
            "latest_time",
            "first_time",
            "strategy_id",
            "status_id",
        ).filter(agent__in=auth_agents)

        level = request.query_params.get("level")
        if level:
            try:
                level = int(level)
            except BaseException:
                return R.failure(_("Parameter error"))
            queryset = queryset.filter(level=level)

        type_ = request.query_params.get("type")
        type_id = request.query_params.get("hook_type_id")
        if type_id:
            hook_type = HookType.objects.filter(pk=type_id).first()
            hook_type_id = hook_type.id if hook_type else 0
            queryset = queryset.filter(hook_type_id=hook_type_id)
        elif type_:
            hook_types = HookType.objects.filter(name=type_).all()
            strategys = IastStrategyModel.objects.filter(vul_name=type_).all()
            q = Q(hook_type__in=hook_types, strategy_id=0) | Q(strategy__in=strategys)
            queryset = queryset.filter(q)

        project_name = request.query_params.get("project_name")
        if project_name:
            agent_ids = get_agents_with_project(project_name, auth_users)
            queryset = queryset.filter(agent_id__in=agent_ids)

        project_id = request.query_params.get("project_id")
        if project_id:
            version_id = request.GET.get("version_id", None)
            if not version_id:
                current_project_version = get_project_version(project_id)
            else:
                current_project_version = get_project_version_by_id(version_id)
            agents = auth_agents.filter(
                bind_project_id=project_id,
                project_version_id=current_project_version.get("version_id", 0),
            )
            queryset = queryset.filter(agent_id__in=agents)

        agent_id = request.query_params.get("agent_id")
        if agent_id:
            queryset = queryset.filter(agent_id=agent_id)

        url = request.query_params.get("url", None)
        if url and url != "":
            queryset = queryset.filter(url__icontains=url)
        status = request.query_params.get("status")
        if status:
            queryset = queryset.filter(status__name=status)

        status_id = request.query_params.get("status_id")
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        order = request.query_params.get("order")
        if order and order in [
            *get_model_order_options(IastVulnerabilityModel),
            "type",
            "-type",
        ]:
            if order == "type":
                order = "hook_type_id"
            if order == "-type":
                order = "-hook_type_id"
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by("-latest_time")

        projects_info = get_user_project_name(auth_users)
        agentArr = get_user_agent_pro(auth_users, projects_info.keys())
        agentPro = agentArr["pidArr"]
        agentServer = agentArr["serverArr"]
        server_ids = agentArr["server_ids"]
        allServer = get_all_server(server_ids)
        allType = IastVulLevel.objects.all().order_by("id")
        allTypeArr = {}
        if allType:
            for item in allType:
                allTypeArr[item.id] = item.name_value
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        datas = VulSerializer(page_data, many=True).data
        pro_length = len(datas)
        if pro_length > 0:
            for index in range(pro_length):
                item = datas[index]
                item["index"] = index
                item["project_name"] = projects_info.get(
                    agentPro.get(item["agent_id"], 0),
                    _("The application has not been binded"),
                )
                item["project_id"] = agentPro.get(item["agent_id"], 0)
                item["server_name"] = allServer.get(
                    agentServer.get(item["agent_id"], 0), "JavaApplication"
                )
                item["server_type"] = VulSerializer.split_container_name(
                    item["server_name"]
                )
                item["level_type"] = item["level_id"]
                item["level"] = allTypeArr.get(item["level_id"], "")
                end["data"].append(item)
        end["page"] = page_summary
        set_vul_inetration(end, request.user.id)
        return R.success(page=page_summary, data=end["data"])


def set_vul_inetration(end: dict[str, Any], user_id: int) -> None:
    pass
