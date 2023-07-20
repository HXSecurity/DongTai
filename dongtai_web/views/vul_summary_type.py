#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vul_level import IastVulLevel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.strategy import IastStrategyModel

from dongtai_web.base.agent import get_project_vul_count, get_hook_type_name
from dongtai_web.base.project_version import (
    get_project_version,
    get_project_version_by_id,
)
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.vul import VulSummaryResponseDataSerializer
from django.utils.text import format_lazy
from dongtai_common.models.hook_type import HookType
from django.db.models import Q

_ResponseSerializer = get_response_serializer(VulSummaryResponseDataSerializer())


class VulSummaryType(UserEndPoint):
    name = "rest-api-vulnerability-summary-type"
    description = _("Applied vulnerability overview")

    @extend_schema_with_envcheck(
        [
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
                "description": _("Name of Project"),
            },
            {
                "name": "level",
                "type": int,
                "description": format_lazy(
                    "{} : {}", _("Level of vulnerability"), "1,2,3,4"
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
                    ",".join(["type", "type", "first_time", "latest_time", "url"]),
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
                    "data": {
                        "level": [
                            {"level": "HIGH", "count": 116, "level_id": 1},
                            {"level": "INFO", "count": 0, "level_id": 4},
                        ],
                        "type": [
                            {"type": "Path Traversal", "count": 79},
                            {"type": "Insecure Hash Algorithms", "count": 1},
                            {"type": "Arbitrary Server Side Forwards", "count": 1},
                        ],
                    },
                    "level_data": [],
                },
            }
        ],
        tags=[_("Vulnerability")],
        summary=_("Vulnerability Summary"),
        description=_(
            "Use the following conditions to view the statistics of the number of vulnerabilities in the project."
        ),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        """
        :param request:
        :return:
        """

        end = {"status": 201, "msg": "success", "level_data": [], "data": {}}

        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        queryset = IastVulnerabilityModel.objects.filter()

        language = request.query_params.get("language")
        if language:
            auth_agents = auth_agents.filter(language=language)

        project_id = request.query_params.get("project_id")
        if project_id and project_id != "":
            version_id = request.GET.get("version_id", None)
            if not version_id:
                current_project_version = get_project_version(project_id)
            else:
                current_project_version = get_project_version_by_id(version_id)
            auth_agents = auth_agents.filter(
                bind_project_id=project_id,
                project_version_id=current_project_version.get("version_id", 0),
            )

        queryset = queryset.filter(agent__in=auth_agents)

        status = request.query_params.get("status")
        if status:
            queryset = queryset.filter(status__name=status)
        status_id = request.query_params.get("status_id")
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        level = request.query_params.get("level")
        if level:
            try:
                level = int(level)
            except BaseException:
                return R.failure(_("Parameter error"))
            queryset = queryset.filter(level=level)

        vul_type = request.query_params.get("type")
        if vul_type:
            hook_types = HookType.objects.filter(name=vul_type).all()
            strategys = IastStrategyModel.objects.filter(vul_name=vul_type).all()
            q = Q(hook_type__in=hook_types) | Q(strategy__in=strategys)
            queryset = queryset.filter(q)

        url = request.query_params.get("url")
        if url and url != "":
            queryset = queryset.filter(url__icontains=url)

        q = Q()
        queryset = queryset.filter(q)

        # 汇总 level
        vul_level = IastVulLevel.objects.all()
        vul_level_metadata = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if vul_level:
            for level_item in vul_level:
                DEFAULT_LEVEL[level_item.name_value] = 0
                vul_level_metadata[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value
        level_summary = (
            queryset.values("level").order_by("level").annotate(total=Count("level"))
        )
        for temp in level_summary:
            DEFAULT_LEVEL[levelIdArr[temp["level"]]] = temp["total"]
        end["data"]["level"] = [
            {"level": _key, "count": _value, "level_id": vul_level_metadata[_key]}
            for _key, _value in DEFAULT_LEVEL.items()
        ]

        # 汇总 type
        type_summary = (
            queryset.values(
                "hook_type_id", "strategy_id", "hook_type__name", "strategy__vul_name"
            )
            .order_by("hook_type_id")
            .annotate(total=Count("hook_type_id"))
        )
        type_summary = list(type_summary)

        vul_type_list = [
            {"type": get_hook_type_name(_).lower().strip(), "count": _["total"]}
            for _ in type_summary
        ]

        tempdic = {}
        for vul_type in vul_type_list:
            if tempdic.get(vul_type["type"], None):
                tempdic[vul_type["type"]]["count"] += vul_type["count"]
            else:
                tempdic[vul_type["type"]] = vul_type
        vul_type_list = tempdic.values()
        end["data"]["type"] = sorted(
            vul_type_list, key=lambda x: x["count"], reverse=True
        )

        return R.success(data=end["data"], level_data=end["level_data"])
