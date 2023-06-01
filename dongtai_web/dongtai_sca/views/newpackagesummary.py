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
from dongtai_common.models.assetv2 import AssetV2, AssetV2Global
from rest_framework_dataclasses.serializers import DataclassSerializer
from dataclasses import dataclass, field
from typing import List
from typing import Any
from dataclasses import dataclass
import json
from django.db.models import Q, F, Count
from dongtai_web.dongtai_sca.scan.utils import get_level, get_license, get_language

logger = logging.getLogger(__name__)


@dataclass
class Language:
    language: str
    count: int
    language_id: int


@dataclass
class Level:
    level: str
    count: int
    level_id: int


@dataclass
class License:
    license: str
    count: int
    license_id: int


@dataclass
class Data:
    level: List[Level]
    language: List[Language]
    license: List[License]


def item_data_transfrom(
    summary_dict,
    function,
    key,
    new_key,
):
    summary_dict[new_key] = function(summary_dict[key])
    return summary_dict


def data_transfrom(dict_list, function, key, new_key):
    return list(
        map(lambda x: item_data_transfrom(x, function, key, new_key),
            dict_list))


class PackageSummaryArgsSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(required=False, help_text=_('Page index'))
    project_version_id = serializers.IntegerField(required=False,
                                                  help_text=_('Page index'))


class PackeageScaSummarySerializer(DataclassSerializer):

    class Meta:
        dataclass = Data


FullSummaryResponseSerializer = get_response_serializer(
    PackeageScaSummarySerializer(many=True))


class NewPackageSummary(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        parameters=[PackageSummaryArgsSerializer],
        responses={200: FullSummaryResponseSerializer})
    def get(self, request):
        ser = PackageSummaryArgsSerializer(data=request.query_params)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if 'project_id' in ser.validated_data:
            q = q & Q(assetv2__project_id=ser.validated_data['project_id'])
        if 'project_version_id' in ser.validated_data:
            q = q & Q(assetv2__project_version_id=ser.
                      validated_data['project_version_id'])
        queryset = AssetV2Global.objects.filter(q)
        language_summary_list = queryset.values('language_id').annotate(
            count=Count('language_id'))
        level_summary_list = queryset.values('level_id').annotate(
            count=Count('level_id'))
        license_summary_list = queryset.annotate(
            license_id=F("iastassetlicense__license_id"),
            count=Count('iastassetlicense__license_id')).values(
                "license_id", "count")
        return R.success(
            data={
                "language":
                data_transfrom(language_summary_list, get_language,
                               "language_id", "language"),
                "license":
                data_transfrom(license_summary_list, get_license, "license_id",
                               "license"),
                "level":
                data_transfrom(level_summary_list, get_level, "level_id",
                               "level"),
            })
