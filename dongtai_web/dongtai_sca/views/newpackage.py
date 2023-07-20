import logging

from django.core.paginator import Paginator
from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, views
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models import User
from dongtai_common.models.assetv2 import AssetV2, AssetV2Global
from dongtai_common.serializers.assetv2 import PackeageScaAssetDetailSerializer
from dongtai_common.utils.const import OPERATE_GET
from dongtai_web.dongtai_sca.models import Package
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

logger = logging.getLogger(__name__)


class PackageListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    language_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(help_text=_("language"))
    )
    license_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(help_text=_("license"))
    )
    level_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(help_text=_("level"))
    )
    project_id = serializers.IntegerField(required=False, help_text=_("Page index"))
    project_version_id = serializers.IntegerField(
        required=False, help_text=_("Page index")
    )
    keyword = serializers.CharField(required=False, help_text=_("search_keyword"))
    order_field = serializers.ChoiceField(["vul_count", "level"], default="vul_count")
    order = serializers.ChoiceField(["desc", "asc"], default="desc")


class PackeageScaAssetSerializer(PackeageScaAssetDetailSerializer):
    class Meta:
        model = PackeageScaAssetDetailSerializer.Meta.model
        fields = [
            "id",
            "package_name",
            "signature_algorithm",
            "signature_value",
            "version",
            "level",
            "level_id",
            "level_name",
            "vul_count",
            "vul_critical_count",
            "vul_high_count",
            "vul_medium_count",
            "vul_low_count",
            "vul_info_count",
            "license_list",
            "language_id",
            "aql",
            "vul_count_groupby_level",
        ]


_NewResponseSerializer = get_response_serializer(PackeageScaAssetSerializer(many=True))


class PackageList(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        request=PackageListArgsSerializer,
        tags=[_("Component"), OPERATE_GET],
        summary=_("Component List"),
        responses={200: _NewResponseSerializer},
    )
    def post(self, request):
        ser = PackageListArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if "level_ids" in ser.validated_data and ser.validated_data["level_ids"]:
            q = q & Q(level__in=ser.validated_data["level_ids"])
        if "language_ids" in ser.validated_data and ser.validated_data["language_ids"]:
            q = q & Q(language_id__in=ser.validated_data["language_ids"])
        if "license_ids" in ser.validated_data and ser.validated_data["license_ids"]:
            q = q & Q(
                iastassetlicense__license_id__in=ser.validated_data["license_ids"]
            )
        if "project_id" in ser.validated_data:
            q = q & Q(assetv2__project_id=ser.validated_data["project_id"])
        if "project_version_id" in ser.validated_data:
            q = q & Q(
                assetv2__project_version_id=ser.validated_data["project_version_id"]
            )
        if "keyword" in ser.validated_data:
            q = q & Q(aql__contains=ser.validated_data["keyword"])
        order = (
            "-" if ser.validated_data["order"] == "desc" else ""
        ) + ser.validated_data["order_field"]
        page_info, data = self.get_paginator(
            AssetV2Global.objects.filter(q).order_by(order).all(),
            ser.validated_data["page"],
            ser.validated_data["page_size"],
        )
        return R.success(
            data=PackeageScaAssetSerializer(data, many=True).data, page=page_info
        )
