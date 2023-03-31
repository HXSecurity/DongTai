import logging
import json

from django.db.models import Q, F, Count
from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import UserEndPoint, R
from rest_framework.viewsets import ViewSet
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.core.cache import cache
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.dast_integration import IastDastIntegration
from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from dongtai_common.models.profile import IastProfile

logger = logging.getLogger('dongtai-webapi')


class DastVulsSettingsArgsSerializer(serializers.Serializer):
    strategy_id = serializers.ListField(child=serializers.IntegerField(),
                                        required=True,
                                        help_text=_("strategy_id"))

    validation_status = serializers.BooleanField(
        required=True, help_text=_("cross validation status enable"))


class DastManageEndPoint(UserEndPoint, viewsets.ViewSet):

    @extend_schema_with_envcheck(request=DastVulsSettingsArgsSerializer,
                                 summary=_('Dast Vul Settings'),
                                 description=_("Dast Vul Settings"),
                                 tags=[_('Dast Vul')])
    def change_validation_settings(self, request):
        ser = DastVulsSettingsArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        key = 'dast_validation_settings'
        try:
            obj, created = IastProfile.objects.update_or_create(
                {
                    'key': key,
                    'value': json.dumps(dict(ser.validated_data))
                },
                key=key)
        except Exception as e:
            logger.error(e, exc_info=e)
            return R.failure(msg=_("Update {} failed").format(key))
        return R.success()

    @extend_schema_with_envcheck(request=DastVulsSettingsArgsSerializer,
                                 summary=_('Dast Vul Settings'),
                                 description=_("Dast Vul Settings"),
                                 tags=[_('Dast Vul')])
    def get_validation_settings(self, request):
        key = 'dast_validation_settings'
        profile = IastProfile.objects.filter(key=key).values_list(
            'value', flat=True).first()
        if profile is None:
            return R.failure(
                msg=_("Failed to get {} configuration").format(key))
        data = json.loads(profile)
        return R.success(data=data)

    @extend_schema_with_envcheck(summary=_('Dast Vul Settings Doc'),
                                 description=_("Dast Vul Settings Doc"),
                                 tags=[_('Dast Vul')])
    def get_doc_url(self, request):
        return R.success(data={
            "url":
            "https://i0x0fy4ibf.feishu.cn/docx/GGpUdYopaoxD4oxnOlncKKbsnRh"
        })
