#!/usr/bin/env python
# datetime:2020/10/23 11:56
import logging
import os
import time

from dongtai_common.models.agent import (
    IastAgent,
    IastAgentDiskList,
)
from dongtai_common.utils import const
from dongtai_protocol.report.handler.heartbeat_handler import update_heartbeat
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler

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
        self.disk_list = self.detail.get("diskList")

    def has_permission(self):
        self.agent = IastAgent.objects.filter(id=self.agent_id).first()
        return self.agent

    def save_heartbeat(self):
        default_dict = {"dt": int(time.time())}
        default_dict["memory"] = self.memory
        default_dict["cpu"] = self.cpu
        default_dict["disk"] = get_disk_from_disk_list(self.disk_list, self.agent.jvm_user_dir)
        update_heartbeat.delay(agent_id=self.agent_id, defaults=default_dict)
        IastAgentDiskList.objects.create(agent=self.agent_id, data=self.disk_list)

    def get_result(self, msg=None):
        return []

    def save(self):
        self.save_heartbeat()

    def get_agent(self, agent_id):
        return IastAgent.objects.filter(id=agent_id).first()


def get_disk_from_disk_list(disk_list: list, agent_jvm_dir: str):
    total_space_bytes = 0
    usable_space_bytes = 0
    for disk in disk_list:
        for partition in disk["partitionList"]:
            if is_dir_under_another_dir(agent_jvm_dir, partition["mountPoint"]):
                return get_disk_rate_dict(partition["totalSpaceBytes"], partition["usableSpaceBytes"])
            total_space_bytes += partition["totalSpaceBytes"]
            usable_space_bytes += partition["usableSpaceBytes"]
    return get_disk_rate_dict(total_space_bytes, usable_space_bytes)


def get_disk_rate_dict(total_space_bytes: int, usable_space_bytes: int):
    return (total_space_bytes - usable_space_bytes) / total_space_bytes


def is_dir_under_another_dir(subdir: str, parent_dir: str) -> bool:
    """Returns True if the subdirectory is under the parent directory, False otherwise.

    Args:
      subdir: The subdirectory path.
      parent_dir: The parent directory path.

    Returns:
      True if the subdirectory is under the parent directory, False otherwise.
    """

    # Normalize the paths.
    subdir = os.path.normpath(subdir)
    parent_dir = os.path.normpath(parent_dir)

    # Check if the subdirectory path starts with the parent directory path.
    return subdir.startswith(parent_dir)
