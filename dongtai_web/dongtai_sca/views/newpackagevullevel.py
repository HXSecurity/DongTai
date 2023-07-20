import logging
from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _
from rest_framework_dataclasses.serializers import DataclassSerializer

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_web.dongtai_sca.scan.utils import get_level
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

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
    @extend_schema_with_envcheck_v2(tags=[_("Component")], summary="组件漏洞等级", responses={200: _NewResponseSerializer})
    def get(self, request):
        return R.success(data=[{"id": level_id, "name_value": get_level(level_id)} for level_id in LEVEL_IDS])
