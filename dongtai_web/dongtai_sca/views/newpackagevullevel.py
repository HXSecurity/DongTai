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

from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from rest_framework_dataclasses.serializers import DataclassSerializer
from dongtai_web.dongtai_sca.scan.utils import get_level
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PackageVulLevel:
    name_value: str
    id: int


class PackeageVulLevelSerializer(DataclassSerializer):

    class Meta:
        dataclass = PackageVulLevel


_NewResponseSerializer = get_response_serializer(PackeageVulLevelSerializer())

LEVEL_IDS = [1, 2, 3, 4]


class PackageVulLevels(UserEndPoint):

    @extend_schema_with_envcheck_v2(tags=[_('Component')],
                                    summary="组件漏洞等级",
                                    responses={200: _NewResponseSerializer})
    def get(self, request):
        return R.success(data=[{
            "id": level_id,
            "name_value": get_level(level_id)
        } for level_id in LEVEL_IDS])
