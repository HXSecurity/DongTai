#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 11:47
# software: PyCharm
# project: webapi
import logging

from rest_framework.request import Request

from base import R
from iast.base.sca import ScaEndPoint
from dongtai_models.models.asset import Asset
from dongtai_models.models.project import IastProject
from dongtai_models.models.sca_artifact_db import ScaArtifactDb
from dongtai_models.models.sca_maven_artifact import ScaMavenArtifact
from iast.serializers.sca import ScaSerializer

logger = logging.getLogger('dongtai-webapi')


class ScaDetailView(ScaEndPoint):
    """
    当前用户详情
    """
    name = "api-v1-scas"
    description = ""

    def get(self, request: Request, id):
        user = request.user

        try:
            agents = self.get_auth_agents_with_user(user)
            dependency = Asset.objects.filter(agent__in=agents, id=id).first()

            if dependency is None:
                return R.failure(msg='组件不存在或无权限访问')
            data = ScaSerializer(dependency).data
            project_id = dependency.agent.bind_project_id
            iast_info = IastProject.objects.values('name').filter(id=project_id).first()
            if iast_info:
                data['project_name'] = iast_info['name']
            else:
                data['project_name'] = ""
            data['vuls'] = list()
            # 替换英文vul_type为中文漏洞类型
            # 查询组件对应的漏洞数据，如果无法查找到则标记为无
            smas = ScaMavenArtifact.objects.filter(signature=data['signature_value']).values("aid", "safe_version")
            for sma in smas:
                svds = ScaArtifactDb.objects.filter(id=sma['aid']).values(
                    'cve_id', 'cwe_id', 'title', 'overview', 'teardown', 'reference', 'level'
                )
                if len(svds) > 0:
                    svd = svds[0]
                    data['vuls'].append({
                        'safe_version': sma['safe_version'] if sma['safe_version'] else '当前版本已停止维护或暂无安全版本',
                        'vulcve': svd['cve_id'],
                        'vulcwe': svd['cwe_id'],
                        'vulname': svd['title'],
                        'overview': svd['overview'],
                        'teardown': svd['teardown'],
                        'reference': svd['reference'],
                        'level': svd['level'],
                    })
            return R.success(data=data)
        except Exception as e:
            logger.error(e)
            return R.failure(msg='组件信息查询失败')
