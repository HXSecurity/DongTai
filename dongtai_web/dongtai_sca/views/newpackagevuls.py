import logging

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from dongtai_common.serializers.assetvulv2 import PackageVulSerializer
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

logger = logging.getLogger(__name__)


class PackageVulsListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))


NewPackageVulSResponseSerializer = get_response_serializer(PackageVulSerializer(many=True))


class NewPackageVuls(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        tags=[_("Component"), "集成"],
        summary="组件漏洞列表",
        parameters=[PackageVulsListArgsSerializer],
        responses={200: NewPackageVulSResponseSerializer},
    )
    def get(self, request, language_id, package_name, package_version):
        ser = PackageVulsListArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        asset_vuls = (
            IastAssetVulV2.objects.filter(
                ~Q(vul_name="") | ~Q(vul_name_zh=""),
                iastvulassetrelationv2__asset__language_id=language_id,
                iastvulassetrelationv2__asset__package_name=package_name,
                iastvulassetrelationv2__asset__version=package_version,
            )
            .order_by("-id")
            .all()
        )
        page_info, data = self.get_paginator(asset_vuls, ser.validated_data["page"], ser.validated_data["page_size"])

        return R.success(data=PackageVulSerializer(data, many=True).data, page=page_info)
