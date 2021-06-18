#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi
import json
import logging
import time

from dongtai_models.models.asset import Asset
from dongtai_models.models.sca_maven_artifact import ScaMavenArtifact
from dongtai_models.models.sca_maven_db import ScaMavenDb
from dongtai_models.models.sca_vul_db import ScaVulDb
from dongtai_models.models.vul_level import IastVulLevel

from apiserver.report.handler.report_handler_interface import IReportHandler

logger = logging.getLogger("django")


class ScaHandler(IReportHandler):

    def parse(self):
        self.package_path = self.detail.get('package_path')
        self.package_signature = self.detail.get('package_signature')
        self.package_name = self.detail.get('package_name')
        self.package_algorithm = self.detail.get('package_algorithm')
        self.agent_name = self.detail.get('agent_name')
        self.project_name = self.detail.get('project_name', 'Demo Project')
        self.language = self.detail.get('language')

    def save(self):
        if all([self.agent_name, self.package_path, self.package_name, self.package_signature,
                self.package_algorithm]) is False:
            logger.warn(f"数据不完整，数据：{json.dumps(self.report)}")
        else:
            agent = self.get_agent(self.project_name, self.agent_name)
            if agent:
                smd = ScaMavenDb.objects.filter(sha_1=self.package_signature).values("version", "aql").first()
                _version = self.package_name.split('/')[-1].replace('.jar', '').split('-')[-1]
                version = smd.get('version', _version) if smd else _version
                package_name = smd.get('aql', self.package_name) if smd else self.package_name
                aids = ScaMavenArtifact.objects.filter(signature=self.package_signature).values("aid")
                if len(aids) > 0:
                    aids = [_['aid'] for _ in aids]
                vul_count = len(aids)
                levels = ScaVulDb.objects.filter(id__in=aids).values('vul_level')

                level = 'info'
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

                try:
                    level = IastVulLevel.objects.get(name=level)
                    current_version_agents = self.get_project_agents(agent)
                    asset_count = 0
                    if current_version_agents:
                        asset_count = Asset.objects.values(1).filter(signature_value=self.package_signature,
                                                                     agent__in=current_version_agents).count()

                    if asset_count == 0:
                        Asset(
                            package_path=self.package_path,
                            version=version,
                            vul_count=vul_count,
                            level=level,
                            package_name=package_name,
                            signature_value=self.package_signature,
                            signature_algorithm=self.package_algorithm,
                            dt=time.time(),
                            agent=agent,
                            language=self.language
                        ).save()
                except Exception as e:
                    pass
