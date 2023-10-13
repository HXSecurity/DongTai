#!/usr/bin/env python
# datetime:2020/10/23 11:56
import logging
import time
from typing import Any

from celery import shared_task
from celery_singleton import Singleton
from django.core.cache import cache
from django.db.models import Q, QuerySet
from django.utils.translation import gettext_lazy as _

from dongtai_common.models.agent import (
    IastAgent,
    IastAgentDiskList,
)
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.project import VulValidation
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.utils import const
from dongtai_common.utils.systemsettings import get_vul_validate
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from dongtai_web.vul_log.vul_log import log_recheck_vul
from dongtai_protocol.report.handler.heartbeat_handler import update_heartbeat
from dongtai_common.models.agent import IastAgentDiskList

logger = logging.getLogger("dongtai.openapi")


@ReportHandler.register(const.REPORT_METRIC)
class ReportMetricHandler(IReportHandler):
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
        self.disk = self.detail.get("disk")  # extend now
        self.disk_list = self.detail.get("diskList")

    def has_permission(self):
        self.agent = IastAgent.objects.filter(id=self.agent_id).first()
        return self.agent

    def save_heartbeat(self):
        default_dict = {"dt": int(time.time())}
        default_dict["memory"] = self.memory
        default_dict["cpu"] = self.cpu
        default_dict["disk"] = self.disk
        update_heartbeat.delay(agent_id=self.agent_id, defaults=default_dict)
        IastAgentDiskList.objects.create(agent=self.agent_id, data=self.disk_list)

    def get_result(self, msg=None):
        return []

    def save(self):
        self.save_heartbeat()

    def get_agent(self, agent_id):
        return IastAgent.objects.filter(id=agent_id).first()
