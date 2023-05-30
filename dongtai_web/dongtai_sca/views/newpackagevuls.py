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
    package_name = serializers.CharField(help_text=_("pacakge name"))
    package_version = serializers.CharField(help_text=_("package version"))


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
    def post(self, request):
        return JsonResponse({})
