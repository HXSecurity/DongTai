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

from dongtai_web.dongtai_sca.utils import get_asset_id_by_aggr_id
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from rest_framework_dataclasses.serializers import DataclassSerializer
from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


#@dataclass
#class Language:
#    language: str
#    count: int
#
#
#@dataclass
#class Level:
#    level: str
#    count: int
#    level_id: int
#
#
#@dataclass
#class License:
#    license: str
#    count: int
#
#
#@dataclass
#class Data:
#    level: List[Level]
#    language: List[Language]
#    license: List[License]


class PackageVulsListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))


class PackeageVulsSerializer(serializers.ModelSerializer):

    class Meta:
        model = IastAssetVulV2
        fields = '__all__'


NewPackageVulSResponseSerializer = get_response_serializer(
    PackeageVulsSerializer(many=True))


class NewPackageVuls(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        request=PackageVulsListArgsSerializer,
        responses={200: NewPackageVulSResponseSerializer})
    def get(self, request, package_name, package_version):
        ser = PackageListArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        asset_vuls = IastAssetVulV2.objects.filter(
            iastvulassetrelationv2__asset__package_name=pacakge_name,
            iastvulassetrelationv2__asset__version=package_version).order_by(
                '-id').all()
        page_info, data = self.get_paginator(asset_vuls,
                                             ser.validated_data['page'],
                                             ser.validated_data['page_size'])

        return R.success(data=PackeageVulsSerializer(data, many=True).data,
                         page=page_info)
