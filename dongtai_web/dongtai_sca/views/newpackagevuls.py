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

from dongtai_web.dongtai_sca.utils import get_asset_id_by_aggr_id
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from dongtai_common.serializers.assetvulv2 import PackageVulSerializer
from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


class PackageVulsListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))


NewPackageVulSResponseSerializer = get_response_serializer(
    PackageVulSerializer(many=True))


class NewPackageVuls(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        tags=[_('Component')],
        summary="组件漏洞列表",
        parameters=[PackageVulsListArgsSerializer],
        responses={200: NewPackageVulSResponseSerializer})
    def get(self, request, language_id, package_name, package_version):
        ser = PackageVulsListArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        asset_vuls = IastAssetVulV2.objects.filter(
            iastvulassetrelationv2__asset__language_id=language_id,
            iastvulassetrelationv2__asset__package_name=package_name,
            iastvulassetrelationv2__asset__version=package_version).order_by(
                '-id').all()
        page_info, data = self.get_paginator(asset_vuls,
                                             ser.validated_data['page'],
                                             ser.validated_data['page_size'])

        return R.success(data=PackageVulSerializer(data, many=True).data,
                         page=page_info)
