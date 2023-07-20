import logging

from django.db.models import F
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from result import Err, Ok, Result

from dongtai_common.endpoint import OpenApiEndPoint, R
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_config import (
    IastAgentConfig,
    IastCircuitConfig,
    IastCircuitMetric,
    IastCircuitTarget,
    MetricGroup,
    MetricOperator,
    MetricType,
    TargetOperator,
    TargetType,
)
from dongtai_common.utils.const import OPERATE_GET
from dongtai_common.utils.systemsettings import get_circuit_break
from dongtai_protocol.decrypter import parse_data

logger = logging.getLogger("dongtai.openapi")


class AgentConfigView(OpenApiEndPoint):
    @extend_schema(
        summary="agent配置",
        tags=["Agent服务端交互协议", OPERATE_GET],
        deprecated=True,
        description="Through agent_ Id get disaster recovery strategy",
        methods=["POST"],
    )
    def post(self, request):
        try:
            param = parse_data(request.read())
            agent_id = param.get("agentId", None)
            if agent_id is None:
                return R.failure(msg="agentId is None")
        except Exception as e:
            logger.error(e)
            return R.failure(msg="agentId is None")
        if not get_circuit_break():
            return R.success(msg=_("Successfully"), data={})
        user = request.user
        agent = IastAgent.objects.filter(pk=agent_id).first()
        data = {}
        if agent and agent.server_id:
            server = agent.server
            if server:
                config = (
                    IastAgentConfig.objects.filter(
                        user=user,
                        cluster_name__in=("", server.cluster_name),
                        cluster_version__in=("", server.cluster_version),
                        hostname__in=("", server.hostname),
                        ip__in=("", server.ip),
                    )
                    .order_by("priority")
                    .first()
                )
                if config:
                    data = config.details

        return R.success(data=data)


class AgentConfigv2View(OpenApiEndPoint):
    @extend_schema(
        summary="agent配置",
        tags=["Agent服务端交互协议", OPERATE_GET],
        deprecated=True,
        description="Through agent_ Id get disaster recovery strategy",
        methods=["POST"],
    )
    def post(self, request):
        try:
            param = parse_data(request.read())
            agent_id = int(param.get("agentId", None))
            if agent_id is None:
                return R.failure(msg="agentId is None")
        except Exception as e:
            logger.error(e)
            return R.failure(msg="agentId is None")
        if not get_circuit_break():
            return R.success(msg=_("Successfully"), data={})
        res = get_agent_config(agent_id)
        if isinstance(res, Err):
            return R.success(msg=_(res.value), data={})
        agent_config = res.value
        return R.success(msg=_("Successfully"), data=agent_config)


def get_agent_filter_details(agent_id):
    return (
        IastAgent.objects.filter(pk=agent_id)
        .values(
            "bind_project__name",
            "user__username",
            "server__protocol",
            "token",
            "server__ip",
            "server__path",
            "server__port",
            "language",
        )
        .annotate(
            PROJECT_NAME=F("bind_project__name"),
            ACCOUNT_NAME=F("user__username"),
            PROTOCOL=F("server__protocol"),
            AGENT_IP=F("server__ip"),
            AGENT_NAME=F("alias"),
            AGENT_PATH=F("server__path"),
            PORT=F("server__port"),
            AGENT_LANGUAGE=F("language"),
        )
        .first()
    )


def get_agent_config_by_scan(agent_id: int, mg: MetricGroup) -> Result:
    agent_detail = get_agent_filter_details(agent_id)
    queryset = (
        IastCircuitConfig.objects.filter(is_deleted=0, metric_group=mg, is_enable=1)
        .order_by("priority")
        .only("id")
    )
    for i in queryset:
        result_list = []
        for target in IastCircuitTarget.objects.filter(circuit_config_id=i.id).all():
            result_list.append(get_filter_by_target(target)(agent_detail))
        if all(result_list):
            return Ok(i.id)
    return Err("config not found")


def get_function(opt: TargetOperator):
    if opt == TargetOperator.EQUAL:
        return lambda x, y: x == y
    if opt == TargetOperator.NOT_EQUAL:
        return lambda x, y: x != y
    if opt == TargetOperator.CONTAIN:
        return lambda x, y: x in y
    if opt == TargetOperator.NOT_CONTAIN:
        return lambda x, y: x not in y
    return None


def get_filter_by_target(target):
    targetattr = TargetType(target.target_type).name
    opt_function = get_function(TargetOperator(target.opt))
    return lambda x: opt_function(x[targetattr], target.value)


def get_agent_config(agent_id: int) -> Result:
    data = {
        "enableAutoFallback": True,
        "performanceLimitRiskMaxMetricsCount": 30,
    }
    interval_list: list[int] = []
    for mg in MetricGroup:
        res = get_agent_config_by_scan(agent_id, mg)
        if isinstance(res, Err):
            continue
        config_id = res.value
        config = IastCircuitConfig.objects.filter(pk=config_id).first()
        if not config:
            continue
        metric_list = []
        for metric in IastCircuitMetric.objects.filter(
            circuit_config_id=config.id
        ).all():
            metric_list.append(convert_metric(metric))
        data[mg.name.lower()] = metric_list
        data[mg.name.lower() + "IsUninstall"] = False
        interval_list.append(config.interval)
    # if interval_list is [], there is mean no config found here.
    # because interval is required in create config.
    if not interval_list:
        return Err("No config found")
    data["performanceLimitRiskMaxMetricsCount"] = min(interval_list)
    return Ok(data)


def convert_metric(metric):
    return {
        "fallbackName": MetricType(metric.metric_type).name,
        "conditions": MetricOperator(metric.opt).name.lower(),
        "value": metric.value,
    }
