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

from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.report_handler_factory import ReportHandler

logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_SCA)
class ScaHandler(IReportHandler):

    def parse(self):
        self.package_path = self.detail.get('package_path')
        self.package_signature = self.detail.get('package_signature')
        self.package_name = self.detail.get('package_name')
        self.package_algorithm = self.detail.get('package_algorithm')

    def save(self):
        if all([self.agent_id, self.package_path, self.package_name, self.package_signature,
                self.package_algorithm]) is False:
            logger.warning(_("Data is incomplete, data: {}").format(json.dumps(self.report)))
        else:
            if self.agent:
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
                except Exception as e:
                    logger.error(_('SCA data resolution failed, reasons: {}').format(e))
