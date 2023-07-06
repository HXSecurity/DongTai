import logging

from dongtai_common.models import User
from dongtai_web.dongtai_sca.models import Package
from django.http import JsonResponse
from rest_framework import views
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from dongtai_common.endpoint import R, UserEndPoint
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.db.models import Q, F, Value

from dongtai_common.models.assetv2 import AssetV2, AssetV2Global
from dongtai_common.models.project import IastProject
from rest_framework_dataclasses.serializers import DataclassSerializer
from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class RelationProject:
    project_id: int
    project_name: str


class RelationProjectArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    #    package_name = serializers.CharField(help_text=_("order_field"))
    #    package_version = serializers.CharField(help_text=_("order"))
    project_id = serializers.IntegerField(
        default=None, required=False, help_text=_("project with be the first"))


class RelationProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='name')
    project_id = serializers.IntegerField(source='id')

    class Meta:
        model = IastProject
        fields = ['project_id', 'project_name']


FullRelationProjectResponseSerializer = get_response_serializer(
    RelationProjectSerializer(many=True))


class NewPackageRelationProject(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        parameters=[RelationProjectArgsSerializer],
        tags=[_('Component')],
        summary="组件相关的项目版本",
        responses={200: FullRelationProjectResponseSerializer})
    def get(self, request, language_id, package_name, package_version):
        ser = RelationProjectArgsSerializer(data=request.query_params)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        departments = request.user.get_relative_department()
        queryset = IastProject.objects.filter(
            department__in=departments).order_by('-latest_time')
        assets_project_ids = AssetV2.objects.filter(
            language_id=language_id,
            package_name=package_name,
            version=package_version,
            project__in=queryset,
        ).values("project_id", ).distinct().order_by('-project_id').all()
        if ser.validated_data["project_id"]:
            assets_p1 = IastProject.objects.filter(
                Q(pk__in=assets_project_ids)
                & Q(pk=ser.validated_data["project_id"])).annotate(
                    order=Value(1)).all()
            assets_p2 = IastProject.objects.filter(
                Q(pk__in=assets_project_ids)
                & ~Q(pk=ser.validated_data["project_id"])).annotate(
                    order=Value(2)).order_by('-pk').all()
            assets = assets_p1.union(assets_p2).order_by('order', '-pk')
        else:
            assets = IastProject.objects.filter(
                Q(pk__in=assets_project_ids)).order_by('-pk').all()
        page_info, data = self.get_paginator(assets,
                                             ser.validated_data['page'],
                                             ser.validated_data['page_size'])
        return R.success(data=RelationProjectSerializer(data, many=True).data,
                         page=page_info)
