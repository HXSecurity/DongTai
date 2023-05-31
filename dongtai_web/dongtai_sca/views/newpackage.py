import logging

from dongtai_common.models import User
from dongtai_web.dongtai_sca.models import Package
from django.http import JsonResponse
from rest_framework import views
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from dongtai_common.endpoint import R, UserEndPoint
from django.db.models import Q, F
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer
from rest_framework import serializers

from dongtai_web.dongtai_sca.utils import get_asset_id_by_aggr_id
from dongtai_common.models.assetv2 import AssetV2, AssetV2Global
from rest_framework.serializers import ValidationError

logger = logging.getLogger(__name__)


class PackageListArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    language_ids = serializers.ListField(
        required=False,
        child=serializers.IntegerField(help_text=_('language')))
    license_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(help_text=_('license')))
    level_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(help_text=_('level')))
    project_id = serializers.IntegerField(required=False,
                                          help_text=_('Page index'))
    project_version_id = serializers.IntegerField(required=False,
                                                  help_text=_('Page index'))
    keyword = serializers.CharField(required=False,
                                    help_text=_("search_keyword"))
    order_field = serializers.ChoiceField(['vul_count', 'level'],
                                          default='vul_count')
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
        ser = PackageListArgsSerializer(data=request.POST)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if 'level_id' in ser.validated_data:
            q = q & Q(level_id__in=ser.validated_data['level_id'])
        if 'language_id' in ser.validated_data:
            q = q & Q(language_id__in=ser.validated_data['language_id'])
        if 'license_id' in ser.validated_data:
            q = q & Q(license_id__in=ser.validated_data['license_id'])
        if 'project_id' in ser.validated_data:
            q = q & Q(assetv2__project_id=ser.validated_data['project_id'])
        if 'project_version_id' in ser.validated_data:
            q = q & Q(assetv2__project_version_id=ser.
                      validated_data['project_version_id'])
        if 'keyword' in ser.validated_data:
            q = q & Q(aql__contains=ser.validated_data['keyword'])
        order = '-' if ser.validated_data[
            'order'] == 'desc' else '' + ser.validated_data['order_field']
        page_info, data = self.get_paginator(
            AssetV2Global.objects.filter(q).order_by(order).values().all(),
            ser.validated_data['page'], ser.validated_data['page_size'])
        return R.success(data=PackeageScaAssetSerializer(data, many=True),
                         page=page_info)
