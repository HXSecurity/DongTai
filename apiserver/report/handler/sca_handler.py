#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi
import json
import logging
import time

from apiserver.models.agent import IastAgent
from apiserver.models.asset import IastAsset
from apiserver.models.sca_maven_artifact import ScaMavenArtifact
from apiserver.models.sca_maven_db import ScaMavenDb
from apiserver.models.sca_vul_db import ScaVulDb
from apiserver.models.vul_level import IastVulLevel
from apiserver.report.handler.report_handler_interface import IReportHandler

logger = logging.getLogger("django")


class ScaHandler(IReportHandler):

    def parse(self):
        self.package_path = self.detail.get('package_path')
        self.package_signature = self.detail.get('package_signature')
        self.package_name = self.detail.get('package_name')
        self.package_algorithm = self.detail.get('package_algorithm')
        self.agent_name = self.detail.get('agent_name')
        self.language = self.detail.get('language')

    def save(self):
        if all([self.agent_name, self.package_path, self.package_name, self.package_signature,
                self.package_algorithm]) is False:
            logger.warn(f"数据不完整，数据：{json.dumps(self.report)}")
        else:
            agent = IastAgent.objects.get(token=self.agent_name, user=self.user_id)
            if agent:
                # 查询当前版本并保存，跟进signature查询maven_db库，查出aql与当前版本
                smd = ScaMavenDb.objects.filter(sha_1=self.package_signature).values("version", "aql").first()
                _version = self.package_path.split('/')[-1].replace('.jar', '').split('-')[-1]
                version = smd.get('version', _version) if smd else _version
                package_name = smd.get('aql', self.package_name) if smd else self.package_name
                # 查询漏洞数量并保存：根据aql查询漏洞数量，根据漏洞查询危害等级跟进signature查询maven_db库，查出aql与当前版本，根据aql查询漏洞数量
                aids = ScaMavenArtifact.objects.filter(signature=self.package_signature).values("aid")
                if len(aids) > 0:
                    aids = [_['aid'] for _ in aids]
                vul_count = len(aids)
                # 查询漏洞危害等级并保存
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

                # 查询当前应用并保存
                level = IastVulLevel.objects.get(name=level)

                try:
                    IastAsset(
                        user=self.user_id,
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
