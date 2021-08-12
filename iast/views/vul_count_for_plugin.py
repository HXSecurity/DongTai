#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai.models.agent import IastAgent
from dongtai.models.vulnerablity import IastVulnerabilityModel

from dongtai.endpoint import R
from dongtai.endpoint import MixinAuthEndPoint
from django.utils.translation import gettext_lazy as _


class VulCountForPluginEndPoint(MixinAuthEndPoint):
    def get(self, request):
        agent_name = request.query_params.get('name')
        if not agent_name:
            return R.failure(msg=_("please input agent name."))

        agent = IastAgent.objects.filter(
            token=agent_name,
            id__in=self.get_auth_agents_with_user(request.user)
        ).first()
        if not agent:
            return R.failure(msg=_("Not found agent_name!"))

        return R.success(data=IastVulnerabilityModel.objects.values('id').filter(agent=agent).count())
