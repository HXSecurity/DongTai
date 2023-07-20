#!/usr/bin/env python
# datetime:2020/10/23 11:56
import logging
import time

from django.core.cache import cache
from django.db.models import Q, QuerySet
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.project import VulValidation
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const
from dongtai_common.utils.systemsettings import get_vul_validate
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from dongtai_web.vul_log.vul_log import log_recheck_vul

logger = logging.getLogger("dongtai.openapi")


def update_agent_cache(agent_id, data):
    cache.set(f"heartbeat-{agent_id}", data, timeout=521)


def check_agent_incache(agent_id):
    return bool(cache.get(f"heartbeat-{agent_id}"))


@ReportHandler.register(const.REPORT_HEART_BEAT)
class HeartBeatHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.req_count = None
        self.cpu = None
        self.memory = None
        self.network = None
        self.report_queue = None
        self.method_queue = None
        self.replay_queue = None
        self.return_queue = None

    def parse(self):
        self.cpu = self.detail.get("cpu")
        self.memory = self.detail.get("memory")
        self.disk = self.detail.get("disk")
        self.req_count = self.detail.get("reqCount", None)
        self.report_queue = self.detail.get("reportQueue", 0)
        self.method_queue = self.detail.get("methodQueue", 0)
        self.replay_queue = self.detail.get("replayQueue", 0)
        self.return_queue = self.detail.get("returnQueue", None)

    def has_permission(self):
        self.agent = IastAgent.objects.filter(id=self.agent_id, user=self.user_id).first()
        return self.agent

    def save_heartbeat(self):
        default_dict = {"dt": int(time.time())}
        if not check_agent_incache(self.agent_id):
            IastHeartbeat.objects.update_or_create(agent_id=self.agent_id, defaults=default_dict)
            IastAgent.objects.update_or_create(pk=self.agent_id, defaults={"is_running": 1, "online": 1})
        if self.return_queue == 1:
            default_dict["req_count"] = self.req_count
            default_dict["report_queue"] = self.report_queue
            default_dict["method_queue"] = self.method_queue
            default_dict["replay_queue"] = self.replay_queue
        elif self.return_queue == 0:
            if self.req_count is not None:
                default_dict["req_count"] = self.req_count
            default_dict["memory"] = self.memory
            default_dict["cpu"] = self.cpu
            default_dict["disk"] = self.disk
            IastHeartbeat.objects.update_or_create(agent_id=self.agent_id, defaults=default_dict)
        else:
            default_dict["memory"] = self.memory
            default_dict["cpu"] = self.cpu
            default_dict["req_count"] = self.req_count
            default_dict["report_queue"] = self.report_queue
            default_dict["method_queue"] = self.method_queue
            default_dict["replay_queue"] = self.replay_queue
            default_dict["disk"] = self.disk
            IastHeartbeat.objects.update_or_create(agent_id=self.agent_id, defaults=default_dict)
        update_agent_cache(self.agent_id, default_dict)

    def get_result(self, msg=None):
        logger.info(f"return_queue: {self.return_queue}")
        if (self.return_queue is None or self.return_queue == 1) and vul_recheck_state(self.agent_id):
            try:
                project_agents = (
                    IastAgent.objects.values_list("id", flat=True)
                    .filter(
                        bind_project_id=self.agent.bind_project_id,
                        language=self.agent.language,
                    )
                    .union(
                        addtional_agenti_ids_query_filepath_simhash(
                            self.agent.filepathsimhash, language=self.agent.language
                        ),
                        addtional_agent_ids_query_deployway_and_path(
                            self.agent.servicetype,
                            self.agent.server.path,
                            self.agent.server.hostname,
                            language=self.agent.language,
                        ),
                    )
                )
                project_agents = list(project_agents)
                if project_agents is None:
                    logger.info(_("There is no probe under the project"))
                logger.info(f"project_agent_ids : {project_agents}")
                replay_queryset = IastReplayQueue.objects.values(
                    "id",
                    "relation_id",
                    "uri",
                    "method",
                    "scheme",
                    "header",
                    "params",
                    "body",
                    "replay_type",
                ).filter(agent_id__in=project_agents, state__in=[const.WAITING, const.SOLVING],)[:200]
                if len(replay_queryset) == 0:
                    logger.info(_("Replay request does not exist"))

                (
                    success_ids,
                    success_vul_ids,
                    failure_ids,
                    failure_vul_ids,
                    replay_requests,
                ) = ([], [], [], [], [])
                for replay_request in replay_queryset:
                    if replay_request["uri"]:
                        replay_requests.append(replay_request)
                        success_ids.append(replay_request["id"])
                        if replay_request["replay_type"] == const.VUL_REPLAY:
                            success_vul_ids.append(replay_request["relation_id"])
                    else:
                        failure_ids.append(replay_request["id"])
                        if replay_request["replay_type"] == const.VUL_REPLAY:
                            failure_vul_ids.append(replay_request["relation_id"])

                timestamp = int(time.time())
                IastReplayQueue.objects.filter(id__in=success_ids, state=const.SOLVING).update(
                    update_time=timestamp, state=const.SOLVED
                )
                IastReplayQueue.objects.filter(id__in=success_ids, state=const.WAITING).update(
                    update_time=timestamp, state=const.SOLVING
                )
                IastReplayQueue.objects.filter(id__in=failure_ids).update(update_time=timestamp, state=const.SOLVED)

                log_recheck_vul(
                    self.agent.user.id,
                    self.agent.user.username,
                    success_vul_ids,
                    "验证中",
                )
                IastVulnerabilityModel.objects.filter(id__in=failure_vul_ids).update(latest_time=timestamp, status_id=1)
                logger.info(_("Reproduction request issued successfully"))
                logger.debug([i["id"] for i in replay_requests])
            except Exception as e:
                logger.info(
                    _("Replay request query failed, reason: {}").format(e),
                    exc_info=True,
                )
            else:
                return replay_requests

        return []

    def save(self):
        self.save_heartbeat()

    def get_agent(self, agent_id):
        return IastAgent.objects.filter(id=agent_id, user=self.user_id).first()


def get_k8s_deployment_id(hostname: str) -> str:
    return hostname[hostname.rindex("-")]


def addtional_agent_ids_query_deployway_and_path(deployway: str, path: str, hostname: str, language: str) -> QuerySet:
    if deployway == "k8s":
        deployment_id = get_k8s_deployment_id(hostname)
        logger.info(f"deployment_id : {deployment_id}")
        server_q = (
            Q(server__hostname__startswith=deployment_id)
            & Q(server__path=path)
            & Q(server__path="")
            & ~Q(server__hostname="")
        )
    elif deployway == "docker":
        server_q = Q(server__path=path) & ~Q(server__path="")
    else:
        server_q = (
            Q(server__path=str(path))
            & Q(server__hostname=str(hostname))
            & ~Q(server__path="")
            & ~Q(server__hostname="")
        )
    final_q = server_q & Q(language=language)
    return IastAgent.objects.filter(final_q).values_list("id", flat=True)


def addtional_agenti_ids_query_filepath_simhash(filepathsimhash: str, language: str) -> QuerySet:
    return IastAgent.objects.filter(filepathsimhash=filepathsimhash, language=language).values_list("id", flat=True)


def get_project_vul_validation_state(agent_id):
    state = IastAgent.objects.filter(pk=agent_id).values_list("bind_project__vul_validation", flat=True).first()
    if state is None:
        state = VulValidation.FOLLOW_GLOBAL
    return state


def vul_recheck_state(agent_id):
    project_level_validation = get_project_vul_validation_state(agent_id)
    global_state = get_vul_validate()
    if project_level_validation == VulValidation.FOLLOW_GLOBAL:
        return global_state
    return project_level_validation == VulValidation.ENABLE
