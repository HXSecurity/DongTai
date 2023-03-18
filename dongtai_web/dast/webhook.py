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

logger = logging.getLogger('dongtai-webapi')


class DastIntegrationSerializer(serializers.ModelSerializer):
    dt_uuid_id = serializers.ListField(child=serializers.CharField())
    dongtai_vul_type = serializers.ListField(child=serializers.CharField())
    agent_id = serializers.ListField(child=serializers.CharField())
    vul_level = serializers.ChoiceField(['HIGH', 'MEDIUM', 'LOW', 'NOTE'])

    class Meta:
        model = IastDastIntegration
        fields = [
            'detail',
            'vul_level',
            'urls',
            'payload',
            'create_time',
            'vul_type',
            'request_messages',
            'dt_uuid_id',
            'dongtai_vul_type',
            'dast_tag',
            'agent_id',
            'target',
        ]


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
        ser = DastIntegrationSerializer(data=request.data)
        try:
            if ser.is_valid(False):
                pass
        except ValidationError as e:
            return R.failure(data=e, status_code=422)
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
