#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: lingzhi-webapi
import logging
import time
from dongtai_common.endpoint import R
from django.db.models import Q
from django.forms.models import model_to_dict
from dongtai_common.endpoint import UserEndPoint
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.api_route import IastApiRoute
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

logger = logging.getLogger("django")


class ProjectVersionArgSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    project_id = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    version_name = serializers.CharField(default=None,
                                         help_text=_("version_name "),
                                         required=False)


class ApiRouteArgSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    version_id = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    project_id = serializers.IntegerField(default=None,
                                          help_text=_('Project id'),
                                          required=False)
    is_cover = serializers.IntegerField(default=None,
                                        help_text=_('Project id'),
                                        required=False)


class NewProjectVersionList(UserEndPoint):
    name = "api-v1-project-version-delete"
    description = _("Delete application version information")

    @extend_schema_with_envcheck(
        [ProjectVersionArgSerializer],
        tags=[_('Project')],
        summary=_('Projects List'),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."),
    )
    def get(self, request):
        ser = ProjectVersionArgSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                version_name = ser.validated_data['version_name']
                project_id = ser.validated_data['project_id']
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if version_name:
            q = Q(version_name__contains=version_name)
        if project_id:
            q = Q(project_id=project_id)
        page_info, documents = self.get_paginator(
            IastProjectVersion.objects.filter(q).order_by('-id').all(), page,
            page_size)
        return R.success(
            data=[model_to_dict(document) for document in documents],
            page=page_info)


class NewApiRouteSearch(UserEndPoint):
    name = "api-v1-api-route-search"
    description = _("Delete application version information")

    @extend_schema_with_envcheck(
        request=ApiRouteArgSerializer,
        tags=[_('API Route')],
        summary=_('New api route search'),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."),
    )
    def post(self, request):
        ser = ApiRouteArgSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                project_id = ser.validated_data['project_id']
                version_id = ser.validated_data['version_id']
                is_cover = ser.validated_data['is_cover']
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if project_id:
            q = q & Q(project_id=project_id)
        if version_id:
            q = q & Q(project_version_id=version_id)
        if is_cover is not None:
            q = q & Q(is_cover=is_cover)

        page_info, documents = self.get_paginator(
            IastApiRoute.objects.filter(q).order_by('-id').values(
                'method__method', 'path', 'id', 'project_id',
                'project_version', 'controller', 'code_class', 'code_file',
                'is_cover').all(), page, page_size)
        documents = list(documents)
        for document in documents:
            document['method'] = {
                "httpmethods": document['method__method'].split("/")
            }
        return R.success(data=documents, page=page_info)
