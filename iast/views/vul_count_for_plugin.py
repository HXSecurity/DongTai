#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai.models.agent import IastAgent
from dongtai.models.vulnerablity import IastVulnerabilityModel

from dongtai.endpoint import R
from dongtai.endpoint import MixinAuthEndPoint
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck


class VulCountForPluginEndPoint(MixinAuthEndPoint):
    @extend_schema_with_envcheck([
        {
            'name': "name",
            'type': str,
        },
    ])
    def get(self, request):
        agent_name = request.query_params.get('name')
        if not agent_name:
            return R.failure(msg=_("Please input agent name."))

        agent = IastAgent.objects.filter(token=agent_name,
                                         id__in=self.get_auth_agents_with_user(
                                             request.user)).first()
        if not agent:
            return R.failure(msg=_("agent_name not found"))

        return R.success(
            data=IastVulnerabilityModel.objects.values('id').filter(
                agent=agent).count())
