#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project import IastProject, ProjectStatus
from dongtai_web.serializers.project import (
    ProjectSerializer,
    get_vul_levels_dict,
    get_project_language,
    get_agent_count,
)
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

logger = logging.getLogger("django")


class _ProjectsArgsSerializer(serializers.Serializer):
    pageSize = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(min_value=1, default=1, help_text=_("Page index"))
    name = serializers.CharField(
        default=None,
        help_text=_("The name of the item to be searched, supports fuzzy search."),
    )
    status = serializers.ChoiceField(
        ProjectStatus.choices,
        default=None,
        allow_null=True,
        help_text="".join([f" {i.label}: {i.value} " for i in ProjectStatus]),
    )
    exclude_vul_status = serializers.IntegerField(
        default=None,
        allow_null=True,
        min_value=0,
        max_value=10,
        help_text=_("The exclude vulnerability status."),
    )


_SuccessSerializer = get_response_serializer(ProjectSerializer(many=True))


class Projects(UserEndPoint):
    name = "api-v1-projects"
    description = _("View item list")

    @extend_schema_with_envcheck(
        [_ProjectsArgsSerializer],
        tags=[_("Project")],
        summary=_("Projects List"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
        response_schema=_SuccessSerializer,
    )
    def get(self, request):
        ser = _ProjectsArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page: int = ser.validated_data.get("page", 1)
                page_size: int = ser.validated_data.get("pageSize", 20)
                name: str = ser.validated_data.get("name")
                status: int | None = ser.validated_data.get("status")
                exclude_vul_status: int | None = ser.validated_data.get(
                    "exclude_vul_status"
                )
            else:
                return R.failure(data="Can not validation data.")
        except ValidationError as e:
            return R.failure(data=e.detail)

        department = request.user.get_relative_department()
        queryset = IastProject.objects.filter(department__in=department).order_by(
            "-latest_time"
        )
        if name:
            queryset = queryset.filter(name__icontains=name)
        if status is not None:
            queryset = queryset.filter(status=status)
        queryset = queryset.select_related("user")
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        vul_levels_dict = get_vul_levels_dict(
            page_data, exclude_vul_status=exclude_vul_status
        )
        project_language_dict = get_project_language(page_data)
        agent_count_dict = get_agent_count(page_data)
        return R.success(
            data=ProjectSerializer(
                page_data,
                many=True,
                context={
                    "vul_levels_dict": vul_levels_dict,
                    "project_language_dict": project_language_dict,
                    "agent_count_dict": agent_count_dict,
                },
                exclude_vul_status=exclude_vul_status,
            ).data,
            page=page_summary,
        )
