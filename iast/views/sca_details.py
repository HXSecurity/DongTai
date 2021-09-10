#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/26 11:47
# software: PyCharm
# project: webapi
import logging

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from dongtai.models.sca_artifact_db import ScaArtifactDb
from dongtai.models.sca_maven_artifact import ScaMavenArtifact

from iast.serializers.sca import ScaSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck

logger = logging.getLogger('dongtai-webapi')


class ScaDetailView(UserEndPoint):
    name = "api-v1-scas"
    description = ""

    @extend_schema_with_envcheck(
        [],
        [],
        [{
            'name':
            _('Get data sample'),
            'description':
            _("The aggregation results are programming language, risk level, vulnerability type, project"
              ),
            'value': {
                "status": 201,
                "msg": "success",
                "data": {
                    "id": 12897,
                    "package_name": "log4j-to-slf4j-2.14.1.jar",
                    "version": "2.14.1",
                    "project_name": "demo",
                    "project_id": 67,
                    "project_version": "V1.0",
                    "language": "JAVA",
                    "agent_name":
                    "Mac OS X-localhost-v1.0.0-d24bf703ca62499ebdd12770708296f5",
                    "signature_value":
                    "ce8a86a3f50a4304749828ce68e7478cafbc8039",
                    "level": "INFO",
                    "level_type": 4,
                    "vul_count": 0,
                    "dt": 1631088844,
                    "vuls": []
                }
            }
        }],
        tags=[_('Component')],
        summary=_("Component Detail"),
        description=
        _("Get the details of the corresponding component by specifying the id."
          ),
    )
    def get(self, request, id):
        user = request.user

        try:
            agents = self.get_auth_agents_with_user(user)
            asset = Asset.objects.filter(agent__in=agents, id=id).first()

            if asset is None:
                return R.failure(msg=_(
                    'Components do not exist or no permission to access'))
            data = ScaSerializer(asset).data
            data['vuls'] = list()

            smas = ScaMavenArtifact.objects.filter(
                signature=data['signature_value']).values(
                    "aid", "safe_version")
            for sma in smas:
                svds = ScaArtifactDb.objects.filter(id=sma['aid']).values(
                    'cve_id', 'cwe_id', 'title', 'overview', 'teardown', 'reference', 'level'
                )
                if len(svds) == 0:
                    continue

                svd = svds[0]
                data['vuls'].append({
                    'safe_version': sma['safe_version'] if sma['safe_version'] else _('Current version stopped for maintenance or it is not a secure version'),
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
            return R.failure(msg=_('Component information query failed'))
