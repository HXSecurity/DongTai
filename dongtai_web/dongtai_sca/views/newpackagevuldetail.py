import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.asset_vul_v2 import IastAssetVulV2
from dongtai_common.serializers.assetvulv2 import PackageVulSerializer
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

logger = logging.getLogger(__name__)


_NewResponseSerializer = get_response_serializer(PackageVulSerializer())


class PackageVulDetail(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        responses={200: _NewResponseSerializer},
        tags=[_("Component")],
        summary="组件漏洞详情",
    )
    def get(self, request, vul_id):
        asset_vul = IastAssetVulV2.objects.filter(vul_id=vul_id).first()
        if asset_vul:
            return R.success(
                data=PackageVulSerializer(asset_vul).data,
            )
        return R.failure()
