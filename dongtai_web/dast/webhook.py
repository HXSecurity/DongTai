import logging
import json

from django.utils.translation import gettext_lazy as _
from dongtai_common.endpoint import AnonymousAuthEndPoint, R
from rest_framework.viewsets import ViewSet
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.core.cache import cache
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.dast_integration import IastDastIntegration
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_conf.settings import DAST_TOKEN

logger = logging.getLogger('dongtai-webapi')


class DastIntegrationRequestMessagesSerializer(serializers.Serializer):
    request = serializers.CharField()
    response = serializers.CharField()


class DastIntegrationSerializer(serializers.Serializer):
    dt_uuid_id = serializers.ListField(child=serializers.CharField(),
                                       required=True)
    dongtai_vul_type = serializers.ListField(child=serializers.CharField(),
                                             required=True)
    agent_id = serializers.ListField(child=serializers.CharField(),
                                     required=True)
    request_messages = serializers.ListField(
        child=DastIntegrationRequestMessagesSerializer(), required=True)
    vul_level = serializers.ChoiceField(['HIGH', 'MEDIUM', 'LOW', 'NOTE'],
                                        required=True)
    urls = serializers.ListField(child=serializers.CharField(), required=True)
    detail = serializers.CharField(required=True, allow_blank=True)
    payload = serializers.CharField(required=True, allow_blank=True)
    dast_tag = serializers.CharField(required=True)
    target = serializers.CharField(required=True, allow_blank=True)
    vul_name = serializers.CharField(required=True)
    create_time = serializers.IntegerField(required=True)
    vul_type = serializers.CharField(required=True)


VUL_LEVEL_DICT = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3,
    "NOTE": 5,
}


class DastWebhook(AnonymousAuthEndPoint):
    name = "api-v1-dast-webhook"
    description = _("Dast Webhook")

    @extend_schema_with_envcheck(request=DastIntegrationSerializer,
                                 summary=_('Dast Webhook push vul'),
                                 description=_("Dast Webhook push vul"),
                                 tags=[_('Dast Webhook')])
    def post(self, request):
        used_token = request.headers.get(
            'X-Dongtai-Dast-Vul-Api-Authorization', '')
        if used_token != DAST_TOKEN:
            return R.failure(msg="Authorization check failed", status_code=401)
        ser = DastIntegrationSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            logger.debug(request.data)
            logger.info(e.detail)
            return R.failure(data=e.detail, status_code=422)
        project_info_set = list(
            IastAgent.objects.filter(
                pk__in=(int(i)
                        for i in ser.validated_data['agent_id'])).values_list(
                            'bind_project_id',
                            'project_version_id').distinct(), )
        dast_list = []
        vul_level_id = VUL_LEVEL_DICT[ser.validated_data['vul_level']]
        for field in [
                'dt_uuid_id',
                'dongtai_vul_type',
                'agent_id',
                'vul_level',
        ]:
            del ser.validated_data[field]
        for project_id, project_version_id in project_info_set:
            dastintegration = IastDastIntegration(
                project_id=project_id,
                project_version_id=project_version_id,
                vul_level_id=vul_level_id,
                **ser.validated_data)
            dast_list.append(dastintegration)
        dasts = IastDastIntegration.objects.bulk_create(dast_list)
        if dasts:
            return R.success(status_code=201)
        return R.failure(status_code=412)
