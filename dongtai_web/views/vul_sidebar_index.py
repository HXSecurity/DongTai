#!/usr/bin/env python

from dongtai_web.utils import get_model_order_options
from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.hook_type import HookType
from dongtai_web.utils import extend_schema_with_envcheck
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from dongtai_common.models.strategy import IastStrategyModel

VALUES = [
    "level",
    "latest_time",
    "language",
    "hook_type_id",
    "uri",
]


class VulSideBarList(UserEndPoint):
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
                "deprecated": True,
                "description": _("Type of vulnerability"),
            },
            {
                "name": "hook_type_id",
                "type": str,
                "description": _("ID of the vulnerability type"),
            },
            {
                "name": "level",
                "type": str,
                "description": format_lazy(
                    "{} : {}", _("Level of vulnerability"), "1,2,3,4"
                ),
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
                    "{} : {}", _("Sorted index"), ",".join(VALUES)
                ),
            },
        ],
        tags=[_("Vulnerability")],
        summary=_("Vulnerability List"),
        description=_("Get the list of vulnerabilities corresponding to the user."),
    )
    def get(self, request):
        """
        :param request:
        :return:
        """
        queryset = IastVulnerabilityModel.objects.values(
            "level",
            "latest_time",
            "hook_type_id",
            "uri",
        ).filter(agent__in=self.get_auth_agents_with_user(request.user))

        language = request.query_params.get("language", None)
        if language:
            queryset = queryset.filter(language=language)

        level = request.query_params.get("level", None)
        if level:
            queryset = queryset.filter(level=level)

        type = request.query_params.get("type", None)
        hook_type_id = request.query_params.get("hook_type_id", None)
        if hook_type_id:
            queryset = queryset.filter(hook_type_id=hook_type_id)
        elif type:
            hook_type = HookType.objects.filter(name=type).first()
            hook_type_id = hook_type.id if hook_type else None
            if hook_type_id:
                queryset = queryset.filter(hook_type_id=hook_type_id)

        url = request.query_params.get("url", None)
        if url:
            queryset = queryset.filter(url=url)

        order = request.query_params.get("order")
        if order and order in get_model_order_options(IastVulnerabilityModel):
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by("-latest_time")

        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("pageSize", 10))
        page_summary, queryset = self.get_paginator(
            queryset, page=page, page_size=page_size
        )
        for obj in queryset:
            hook_type = HookType.objects.filter(pk=obj["hook_type_id"]).first()
            hook_type_name = hook_type.name if hook_type else None
            strategy = IastStrategyModel.objects.filter(pk=obj["strategy_id"]).first()
            strategy_name = strategy.vul_name if strategy else None
            type_ = list(
                filter(lambda x: x is not None, [strategy_name, hook_type_name])
            )
            obj["type"] = type_[0] if type_ else ""
        return R.success(
            page=page_summary,
            total=page_summary["alltotal"],
            data=list(queryset),
        )
