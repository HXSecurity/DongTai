#!/usr/bin/env python

import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.project import ProjectStatus
from dongtai_common.utils.request_type import Request
from dongtai_web.serializers.project import (
    ProjectSerializer,
    get_agent_count,
    get_project_language,
    get_vul_levels_dict,
)
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

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
    project_group_name = serializers.CharField(default=None, help_text="项目组名称")


_SuccessSerializer = get_response_serializer(ProjectSerializer(many=True))


class Projects(UserEndPoint):
    name = "api-v1-projects"
    description = _("View item list")

    @extend_schema_with_envcheck(
        [_ProjectsArgsSerializer],
        tags=[_("Project")],
        summary=_("Projects List"),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."),
        response_schema=_SuccessSerializer,
    )
    def get(self, request: Request):
        ser = _ProjectsArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page: int = ser.validated_data.get("page", 1)
                page_size: int = ser.validated_data.get("pageSize", 20)
                name: str = ser.validated_data.get("name")
                status: int | None = ser.validated_data.get("status")
                exclude_vul_status: int | None = ser.validated_data.get("exclude_vul_status")
                project_group_name: str | None = ser.validated_data.get("project_group_name")
            else:
                return R.failure(data="Can not validation data.")
        except ValidationError as e:
            return R.failure(data=e.detail)

        queryset = request.user.get_projects().order_by("-latest_time")
        if name:
            queryset = queryset.filter(name__icontains=name)
        if status is not None:
            queryset = queryset.filter(status=status)
        if project_group_name is not None:
            queryset = queryset.filter(iastprojectgroup__name__icontains=project_group_name)
        queryset = queryset.select_related("user").prefetch_related("iastprojectgroup_set")
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        vul_levels_dict = get_vul_levels_dict(page_data, exclude_vul_status=exclude_vul_status)
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
