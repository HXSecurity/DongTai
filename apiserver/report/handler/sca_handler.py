#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi
import json
import logging
import time

from dongtai.models.asset import Asset
from dongtai.models.sca_maven_artifact import ScaMavenArtifact
from dongtai.models.sca_maven_db import ScaMavenDb
from dongtai.models.sca_vul_db import ScaVulDb
from dongtai.models.vul_level import IastVulLevel
from dongtai.utils import const
from django.utils.translation import gettext_lazy as _
from dongtai.models.project import IastProject

from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.report_handler_factory import ReportHandler
import requests
from AgentServer import settings


logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_SCA)
class ScaHandler(IReportHandler):

    def parse(self):
        self.package_path = self.detail.get('packagePath')
        self.package_signature = self.detail.get('packageSignature')
        self.package_name = self.detail.get('packageName')
        self.package_algorithm = self.detail.get('packageAlgorithm')

    def save(self):
        if all([self.agent_id, self.package_path, self.package_name]) is False:
            logger.warning(_("Data is incomplete, data: {}").format(json.dumps(self.report)))
        else:
            search_query = ""
            if self.agent.language == "JAVA":
                version = self.package_name.split('/')[-1].replace('.jar', '').split('-')[-1]
                search_query = "hash=" + self.package_signature
            elif self.agent.language == "PYTHON":
                # @todo agent上报版本 or 捕获全量pip库
                version = self.package_name.split('/')[-1].split('-')[-1]
                name = self.package_name.replace("-" + version, "")
                search_query = "ecosystem={}&name={}&version={}".format("PyPI", name, version)
            if search_query != "":
                package_name = self.package_name
                level = 'info'
                try:
                    url = settings.SCA_URL + "/api/package_vul/?" + search_query
                    resp = requests.get(url=url)
                    resp = json.loads(resp.content)
                    maven_model = resp.get("data", {}).get("package", {})
                    if maven_model is None:
                        maven_model = {}
                    vul_list = resp.get("data", {}).get("vul_list", {})
                    package_name = maven_model.get('aql', self.package_name)
                    version = maven_model.get('version', version)
                    vul_count = len(vul_list)
                    levels = []
                    for vul in vul_list:
                        _level = vul.get("vul_package", {}).get("severity", "none")
                        if _level and _level not in levels:
                            levels.append(_level)
                    if len(levels) > 0:
                        levels = [_['vul_level'] for _ in levels]
                        if 'high' in levels:
                            level = 'high'
                        elif 'high' in levels:
                            level = 'high'
                        elif 'medium' in levels:
                            level = 'medium'
                        elif 'low' in levels:
                            level = 'low'
                        else:
                            level = 'info'

                except Exception as e:
                    logger.info("get package_vul failed:{}".format(e))

                try:
                    level = IastVulLevel.objects.get(name=level)
                    current_version_agents = self.get_project_agents(self.agent)
                    asset_count = 0
                    if current_version_agents:
                        asset_count = Asset.objects.values("id").filter(signature_value=self.package_signature,
                                                                        agent__in=current_version_agents).count()

                    if asset_count == 0:
                        Asset.objects.create(
                            package_name=package_name,
                            package_path=self.package_path,
                            signature_algorithm=self.package_algorithm,
                            signature_value=self.package_signature,
                            dt=time.time(),
                            version=version,
                            level=level,
                            vul_count=vul_count,
                            agent=self.agent
                        )
                    project = IastProject.objects.filter(pk=self.agent.bind_project_id).first()
                    if project:
                        project.update_latest()
                except Exception as e:
                    logger.error(_('SCA data resolution failed, reasons: {}').format(e))

@ReportHandler.register(const.REPORT_SCA + 1)
class ScaBulkHandler(ScaHandler):
    def parse(self):
        self.packages = self.detail.get('packages')
        self.package_path = self.detail.get('packagePath')
        self.package_signature = self.detail.get('packageSignature')
        self.package_name = self.detail.get('packageName')
        self.package_algorithm = self.detail.get('packageAlgorithm')

    def save(self):
        for package in self.packages:
            self.package_path = package.get('packagePath', None)
            self.package_signature = package.get('packageSignature', None)
            self.package_name = package.get('packageName', None)
            self.package_algorithm = package.get('packageAlgorithm', None)
            super().save()
