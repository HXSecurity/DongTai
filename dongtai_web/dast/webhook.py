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

PLUGIN_VULTYPE_DICT = {}


def get_iast_vul_code(plugin_str: str) -> list:
    if plugin_str.startswith("path-traversal"):
        return ["path-traversal"]
    if plugin_str.startswith("xss"):
        return ["reflected-xss"]
    if plugin_str.startswith("sqldet"):
        return [
            "sql-injection",
            "nosql-injection",
            "hql-injection",
        ]
    if plugin_str.startswith("cmd-injection"):
        return ["cmd-injection"]
    if plugin_str.startswith("redirect"):
        return ["unvalidated-redirect"]
    if plugin_str.startswith("ssrf"):
        return ["ssrf"]
    return []


def parse_xray_uuid(response: str, split_word="\r\n") -> str:
    res_list = response.split(split_word)
    for line in res_list:
        if line.startswith("Xray"):
            key_tuple = line.split(":")
            return key_tuple[1].strip()
    return ""


def parse_agent_id(response: str, split_word="\r\n") -> str:
    res_list = response.split(split_word)
    for line in res_list:
        if line.startswith("AgentId"):
            key_tuple = line.split(":")
            return key_tuple[1].strip()
    return ""


def bind_vul_messages(agent_id, uuid, strategy_ids, response):
    agent = IastAgent.objects.filter(pk=agent_id).first()
    if not agent:
        return
    cache.set(
        f"response-{agent_id}-{uuid}",
        {
            "res": response,
            "strategy_ids": strategy_ids,
        },
        timeout=60 * 5,
    )
    vul_ids = cache.get(f"vul_ids-{agent_id}-{uuid}")
    vuls = IastVulnerabilityModel.objects.filter(pk__in=vul_ids).all()
    for vul in vuls:
        dastintegration = IastDastIntegration.objects.create(
            vul_id=vul.id,
            uuid=uuid,
            data=response,
        )


def bind_xray_messages(agent_id, uuid, vul_ids):
    cache.set(f"vul_ids-{agent_id}-{uuid}", vul_ids, timeout=60 * 5)
    data = cache.get(f"response-{agent_id}-{uuid}")
    vuls = IastVulnerabilityModel.objects.filter(pk__in=vul_ids).all()
    for vul in vuls:
        dastintegration = IastDastIntegration.objects.create(
            vul_id=vul.id,
            uuid=uuid,
            data=response,
        )


class XrayWebhook(AnonymousAuthEndPoint):
    name = "api-v1-xray-webhook"
    description = _("Xray Webhook")

    def post(self, request):
        if "type" in request.data and request.data["type"] == "web_statistic":
            logger.debug(request.data)
        elif "type" in request.data and request.data["type"] == "web_vuln":
            iast_vul_codes = get_iast_vul_code(
                request.data['data']['detail']['plugin'])
            strategy_ids = list(
                IastStrategyModel.objects.filter(
                    vul_type__in=iast_vul_codes).value_list(
                        'pk',
                        flat=True,
                    ).all())
            for reqres_pair in request.data['data']['detail']['snapshot']:
                req, res = reqres_pair
                uuid = parse_xray_uuid(res)
                if uuid:
                    (agent_id, uuid) = uuid.split(".")
                    bind_vul_messages(agent_id, uuid, strategy_ids,
                                      request.data)
                    break
        return R.success()


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
                            'project_version_id',
                        ).distinct(), )
        dast_list = []
        vul_level_id = VUL_LEVEL_DICT[ser.validated_data['vul_level']]
        for field in [
                'dt_uuid_id', 'dongtai_vul_type', 'agent_id', 'vul_level'
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
