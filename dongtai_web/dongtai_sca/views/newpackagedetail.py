import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.assetv2 import (
    AssetV2Global,
)
from dongtai_common.serializers.assetv2 import PackeageScaAssetDetailSerializer
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

logger = logging.getLogger(__name__)


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
