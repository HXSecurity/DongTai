#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Q

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.asset import Asset
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck
from django.utils.text import format_lazy

from dongtai_web.utils import get_model_order_options


class ScaSidebarList(UserEndPoint):
    @extend_schema_with_envcheck(
        [
            {
                "name": "language",
                "type": str,
                "description": _("programming language"),
            },
            {
                "name": "level",
                "type": str,
                "description": _("Level of vulnerability"),
            },
            {
                "name": "app",
                "type": str,
            },
            {
                "name": "order",
                "type": str,
                "description": format_lazy(
                    "{} : {}",
                    _("Sorted index"),
                    ",".join(["package_name", "version", "language", "level", "dt"]),
                ),
            },
        ],
        tags=[_("Component")],
        summary=_("Component List"),
        description=_(
            "Use the specified project information to obtain the corresponding component."
        ),
    )
    def get(self, request):
        """
        :param request:
        :return:
        """
        language = request.query_params.get("language", None)
        level = request.query_params.get("level", None)
        app_name = request.query_params.get("app", None)
        order = request.query_params.get("order", None)

        condition = Q()
        if language:
            condition = condition & Q(language=language)
        if level:
            condition = condition & Q(level=level)
        if app_name:
            condition = condition & Q(app_name=app_name)

        if order and order in get_model_order_options(Asset):
            queryset = (
                Asset.objects.values("package_name", "version", "level", "dt")
                .filter(condition)
                .order_by(order)
            )
        else:
            queryset = (
                Asset.objects.values("package_name", "version", "level", "dt")
                .filter(condition)
                .order_by("-dt")
            )

        page_size = 10
        page_summary, queryset = self.get_paginator(queryset, page_size=page_size)
        return R.success(
            data=[obj for obj in queryset],
            page=page_summary,
            total=page_summary["alltotal"],
        )
