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

logger = logging.getLogger('dongtai-webapi')


class ScaDetailView(UserEndPoint):
    name = "api-v1-scas"
    description = ""

    def get(self, request, id):
        user = request.user

        try:
            agents = self.get_auth_agents_with_user(user)
            dependency = Asset.objects.filter(agent__in=agents, id=id).first()

            if dependency is None:
                return R.failure(msg=_('Components do not exist or have no right to access'))
            data = ScaSerializer(dependency).data
            data['vuls'] = list()
            
            
            smas = ScaMavenArtifact.objects.filter(signature=data['signature_value']).values("aid", "safe_version")
            for sma in smas:
                svds = ScaArtifactDb.objects.filter(id=sma['aid']).values(
                    'cve_id', 'cwe_id', 'title', 'overview', 'teardown', 'reference', 'level'
                )
                if len(svds) == 0:
                    continue

                svd = svds[0]
                data['vuls'].append({
                    'safe_version': sma['safe_version'] if sma['safe_version'] else _('The current version has stopped maintenance or no secure version'),
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
