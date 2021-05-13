#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/13 下午5:59
# project: dongtai-webapi
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from base import R
from iast.base.user import UserTokenEndPoint


class VulnCountForPluginEndPoint(UserTokenEndPoint):
    def get(self, request):
        agent_name = request.query_params.get('name')
        if not agent_name:
            return R.failure(msg="please input agent name.")

        agent = IastAgent.objects.filter(
            token=agent_name,
            id__in=self.get_auth_agents_with_user(request.user)
        ).first()
        if not agent:
            return R.failure(msg="Not found agent_name!")

        return R.success(data=IastVulnerabilityModel.objects.values('id').filter(agent=agent).count())
