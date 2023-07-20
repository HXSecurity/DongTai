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

from dongtai_common.models.assetv2 import (
    AssetV2,
    AssetV2Global,
    IastPackageGAInfo,
)
from dongtai_common.serializers.assetv2 import PackeageScaAssetDetailSerializer

logger = logging.getLogger(__name__)


class PackageListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    languages = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_("language"))
    )
    licenses = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_("license"))
    )
    levels = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_("level"))
    )
    project_id = serializers.IntegerField(default=1, help_text=_("Page index"))
    project_version_id = serializers.IntegerField(default=1, help_text=_("Page index"))
    keyword = serializers.CharField(help_text=_("search_keyword"))
    order_field = serializers.CharField(help_text=_("order_field"))
    order = serializers.CharField(help_text=_("order"))


_NewResponseSerializer = get_response_serializer(PackeageScaAssetDetailSerializer())


class PackageDetail(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        tags=[_("Component")],
        summary=_("Component Detail"),
        responses={200: _NewResponseSerializer},
    )
    def get(self, request, language_id, package_name, package_version):
        asset = AssetV2Global.objects.filter(
            language_id=language_id,
            package_name=package_name,
            version=package_version,
        ).first()
        if asset:
            return R.success(data=PackeageScaAssetDetailSerializer(asset).data)
        return R.failure()
