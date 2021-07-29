#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/29 下午4:56
# project: dongtai-webapi
from dongtai.endpoint import AnonymousAndUserEndPoint, R
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.asset import Asset

from iast.serializers.sca import ScaSerializer


class EngineMethodPoolSca(AnonymousAndUserEndPoint):
    def get(self, request):
        method_pool_id = request.query_params.get('method_pool_id')
        # 根据method pool id 查询agent id
        if method_pool_id is None:
            return R.failure(msg='method_pool_id is empty')

        method_pool = MethodPool.objects.filter(id=method_pool_id).values('agent_id').first()
        if method_pool is None:
            return R.failure(msg='method_pool does not exist')

        agent_id = method_pool['agent_id']
        auth_agents = self.get_auth_and_anonymous_agents(request.user)
        if auth_agents is None or auth_agents.filter(id=agent_id).values('id').exists() is False:
            return R.failure(msg='method_pool has no permission')

        project_data = auth_agents.filter(id=agent_id).values('bind_project_id', 'project_version_id').first()
        project_id = project_data['bind_project_id']
        project_version_id = project_data['project_version_id']

        #
        queryset = Asset.objects.filter(agent_id=agent_id)

        return R.success(data=ScaSerializer(queryset, many=True).data)
