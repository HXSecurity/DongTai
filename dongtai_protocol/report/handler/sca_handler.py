#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi
import json
import logging

from dongtai_common.utils import const
from django.utils.translation import gettext_lazy as _
from dongtai_web.dongtai_sca.scan.utils import update_one_sca, new_update_one_sca
from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
import requests
from dongtai_conf import settings

logger = logging.getLogger("dongtai.openapi")


@ReportHandler.register(const.REPORT_SCA)
class ScaHandler(IReportHandler):
    def parse(self):
        self.package_path = self.detail.get("packagePath")
        self.package_signature = self.detail.get("packageSignature")
        self.package_name = self.detail.get("packageName")
        self.package_algorithm = self.detail.get("packageAlgorithm")
        self.package_version = self.detail.get("packageVersion", "")

    @staticmethod
    def send_to_engine(
        agent_id,
        package_path,
        package_signature,
        package_name,
        package_algorithm,
        package_version,
    ):
        try:
            logger.info(
                f"[+] 处理SCA请求[{agent_id}, {package_path}, {package_signature}, {package_name}, {package_algorithm} {package_version}]正在下发扫描任务"
            )
            if package_signature:
                new_update_one_sca.delay(
                    agent_id,
                    package_path,
                    package_signature,
                    package_name,
                    package_algorithm,
                    package_version,
                )
            else:
                update_one_sca.delay(
                    agent_id,
                    package_path,
                    package_signature,
                    package_name,
                    package_algorithm,
                    package_version,
                )
            logger.info(
                f"[+] 处理SCA请求[{agent_id}, {package_path}, {package_signature}, {package_name}, {package_algorithm} {package_version}]任务下发完成"
            )
        except Exception as e:
            logger.info(
                f"[-] Failure: sca package [{agent_id} {package_path} {package_signature} {package_name} {package_algorithm} {package_version}], Error: {e}"
            )

    def save(self):
        if all([self.agent_id, self.package_path, self.package_name]) is False:
            logger.warning(
                _("Data is incomplete, data: {}").format(json.dumps(self.report))
            )
        else:
            # post to dongtai engine async deal
            ScaHandler.send_to_engine(
                self.agent_id,
                self.package_path,
                self.package_signature,
                self.package_name,
                self.package_algorithm,
                self.package_version,
            )


@ReportHandler.register(const.REPORT_SCA + 1)
class ScaBulkHandler(ScaHandler):
    def parse(self):
        self.packages = self.detail.get("packages")
        self.package_path = self.detail.get("packagePath")
        self.package_signature = self.detail.get("packageSignature")
        self.package_name = self.detail.get("packageName")
        self.package_algorithm = self.detail.get("packageAlgorithm")
        self.package_version = self.detail.get("packageVersion", "")

    def save(self):
        for package in self.packages:
            self.package_path = package.get("packagePath", None)
            self.package_signature = package.get("packageSignature", None)
            self.package_name = package.get("packageName", None)
            self.package_algorithm = package.get("packageAlgorithm", None)
            self.package_version = package.get("packageVersion", "")
            super().save()
