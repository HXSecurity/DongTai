import logging
from dataclasses import dataclass

from django.db.models import Count, F, Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework_dataclasses.serializers import DataclassSerializer

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.assetv2 import AssetV2Global, IastAssetLicense
from dongtai_web.dongtai_sca.scan.utils import get_language, get_level, get_license
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

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
    level: list[Level]
    language: list[Language]
    license: list[License]


def item_data_transfrom(
    summary_dict,
    function,
    key,
    new_key,
):
    summary_dict[new_key] = function(summary_dict[key])
    return summary_dict


def data_transfrom(dict_list, function, key, new_key):
    return [item_data_transfrom(x, function, key, new_key) for x in dict_list]


class PackageSummaryArgsSerializer(serializers.Serializer):
    project_id = serializers.IntegerField(required=False, help_text=_("Page index"))
    project_version_id = serializers.IntegerField(required=False, help_text=_("Page index"))


class PackeageScaSummarySerializer(DataclassSerializer):
    class Meta:
        dataclass = Data


FullSummaryResponseSerializer = get_response_serializer(PackeageScaSummarySerializer(many=True))


class NewPackageSummary(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        parameters=[PackageSummaryArgsSerializer],
        tags=[_("Component")],
        summary="组件概况",
        responses={200: FullSummaryResponseSerializer},
    )
    def get(self, request):
        ser = PackageSummaryArgsSerializer(data=request.query_params)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        license_q = Q()
        if "project_id" in ser.validated_data:
            q = q & Q(assetv2__project_id=ser.validated_data["project_id"])
            license_q = license_q & Q(asset__assetv2__project_id=ser.validated_data["project_id"])
        if "project_version_id" in ser.validated_data:
            q = q & Q(assetv2__project_version_id=ser.validated_data["project_version_id"])
            license_q = license_q & Q(asset__assetv2__project_version_id=ser.validated_data["project_version_id"])
        queryset = AssetV2Global.objects.filter(q)
        license_queryset = IastAssetLicense.objects.filter(license_q)
        language_summary_list = queryset.values("language_id").annotate(count=Count("language_id"))
        level_summary_list = queryset.values("level").annotate(level_id=F("level"), count=Count("level"))
        license_summary_list = license_queryset.values("license_id").annotate(count=Count("license_id"))
        return R.success(
            data={
                "language": data_transfrom(language_summary_list, get_language, "language_id", "language"),
                "license": data_transfrom(license_summary_list, get_license, "license_id", "license"),
                "level": data_transfrom(level_summary_list, get_level, "level_id", "level"),
            }
        )
