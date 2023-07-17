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
from dongtai_common.serializers.assetvulv2 import PackageVulSerializer

logger = logging.getLogger(__name__)


class PackageListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    language_ids = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_('language')))
    license_ids = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_('license')))
    level_ids = serializers.ListField(
        child=serializers.IntegerField(default=1, help_text=_('level')))
    project_id = serializers.IntegerField(default=1, help_text=_('Page index'))
    project_version_id = serializers.IntegerField(default=1,
                                                  help_text=_('Page index'))
    keyword = serializers.CharField(help_text=_("search_keyword"))
    order_field = serializers.CharField(help_text=_("order_field"))
    order = serializers.CharField(help_text=_("order"))


_NewResponseSerializer = get_response_serializer(PackageVulSerializer())


class PackageVulDetail(UserEndPoint):

    @extend_schema_with_envcheck_v2(
        responses={200: _NewResponseSerializer},
        tags=[_('Component')],
        summary="组件漏洞详情",
    )
    def get(self, request, vul_id):
        asset_vul = IastAssetVulV2.objects.filter(vul_id=vul_id).first()
        if asset_vul:
            return R.success(data=PackageVulSerializer(asset_vul).data, )
        return R.failure()
