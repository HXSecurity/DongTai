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
from dongtai_common.models.assetv2 import AssetV2, AssetV2Global

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
    order_field = serializers.ChoiceField(['vul_count', 'level'],
                                          default='level')
    order = serializers.ChoiceField(['desc', 'asc'], default='desc')


class PackeageScaAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetV2Global
        fields = '__all__'


_NewResponseSerializer = get_response_serializer(
    PackeageScaAssetSerializer(many=True))


class PackageList(UserEndPoint):

    @extend_schema_with_envcheck_v2(request=PackageListArgsSerializer,
                                    responses={200: _NewResponseSerializer})
    def post(self, request):
        return JsonResponse({})
