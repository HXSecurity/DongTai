from apiserver.decrypter import parse_data
from dongtai.endpoint import OpenApiEndPoint, R
from dongtai.models.agent import IastAgent
from dongtai.models.agent_config import IastAgentConfig
from django.db.models import Q
from drf_spectacular.utils import extend_schema
import logging
from dongtai.utils.systemsettings import get_circuit_break
from django.utils.translation import gettext_lazy as _
from result import Ok, Err, Result
logger = logging.getLogger('dongtai.openapi')


class AgentConfigView(OpenApiEndPoint):

    @extend_schema(
        description='Through agent_ Id get disaster recovery strategy',
        responses=R,
        methods=['POST']
    )
    def post(self, request):
        try:
            # agent_id = request.data.get('agentId', None)
            param = parse_data(request.read())
            agent_id = param.get('agentId', None)
            if agent_id is None:
                return R.failure(msg="agentId is None")
        except Exception as e:
            logger.error(e)
            return R.failure(msg="agentId is None")
        if not get_circuit_break():
            return R.success(msg=_('Successfully'), data={})
        user = request.user
        agent = IastAgent.objects.filter(pk=agent_id).first()
        data = {}
        if agent and agent.server_id:
            server = agent.server
            if server:
                config = IastAgentConfig.objects.filter(
                    user=user,
                    cluster_name__in=('', server.cluster_name),
                    cluster_version__in=('', server.cluster_version),
                    hostname__in=('', server.hostname),
                    ip__in=('', server.ip)
                ).order_by('-priority').first()
                if config:
                    data = config.details

        return R.success(data=data)


class AgentConfigv2View(OpenApiEndPoint):

    def post(self, request):
        try:
            # agent_id = request.data.get('agentId', None)
            param = parse_data(request.read())
            agent_id = int(param.get('agentId', None))
            if agent_id is None:
                return R.failure(msg="agentId is None")
        except Exception as e:
            logger.error(e)
            return R.failure(msg="agentId is None")
        if not get_circuit_break():
            return R.success(msg=_('Successfully'), data={})
        res = get_agent_config(agent_id)
        if isinstance(res, Err):
            return R.success(msg=_(Err.value), data={})
        agent_config = res.value
        return R.success(msg=_('Successfully'), data=agent_config)


def get_agent_config(agent_id: int) -> Result:
    data = {
        "enableAutoFallback":
        True,
        "performanceLimitRiskMaxMetricsCount":
        30,
        "systemIsUninstall":
        True,
        "jvmIsUninstall":
        True,
        "applicationIsUninstall":
        True,
        "system": [{
            "fallbackName": "cpuUsagePercentage",
            "conditions": "greater",
            "value": 100
        }, {
            "fallbackName": "sysMemUsagePercentage",
            "conditions": "greater",
            "value": 100
        }, {
            "fallbackName": "sysMemUsageUsed",
            "conditions": "greater",
            "value": 100000000000
        }],
        "jvm": [{
            "fallbackName": "jvmMemUsagePercentage",
            "conditions": "greater",
            "value": 100
        }, {
            "fallbackName": "jvmMemUsageUsed",
            "conditions": "greater",
            "value": 100000000000
        }, {
            "fallbackName": "threadCount",
            "conditions": "greater",
            "value": 100000
        }, {
            "fallbackName": "daemonThreadCount",
            "conditions": "greater",
            "value": 1000000
        }, {
            "fallbackName": "dongTaiThreadCount",
            "conditions": "greater",
            "value": 1000000
        }],
        "application": [{
            "fallbackName": "hookLimitTokenPerSecond",
            "conditions": "greater",
            "value": 10000
        }, {
            "fallbackName": "heavyTrafficLimitTokenPerSecond",
            "conditions": "greater",
            "value": 100000000
        }]
    }
    return Ok(data)
