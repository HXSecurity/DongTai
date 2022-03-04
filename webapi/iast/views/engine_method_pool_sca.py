#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
from dongtai.endpoint import AnonymousAndUserEndPoint, R
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.asset import Asset

from iast.serializers.sca import ScaSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai.models.sca_maven_db import ScaMavenDb

_ResponseSerializer = get_response_serializer(
    data_serializer=ScaSerializer(many=True), )


class EngineMethodPoolSca(AnonymousAndUserEndPoint):
    @extend_schema_with_envcheck(
        [{
            'name': "method_pool_id",
            'type': int,
            'required': True
        }],
        tags=[_('Method Pool')],
        summary=_('Method Pool Component'),
        description=_("Get the component information list of the tainted call chain."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        method_pool_id = request.query_params.get('method_pool_id')

        if method_pool_id is None:
            return R.failure(msg=_('method_pool_id is empty'))

        method_pool = MethodPool.objects.filter(
            id=method_pool_id).values('agent_id').first()
        if method_pool is None:
            return R.failure(msg=_('method_pool does not exist'))

        agent_id = method_pool['agent_id']
        auth_agents = self.get_auth_and_anonymous_agents(request.user)
        if auth_agents is None or auth_agents.filter(
                id=agent_id).values('id').exists() is False:
            return R.failure(msg=_('method_pool has no permission'))

        project_data = auth_agents.filter(id=agent_id).values(
            'bind_project_id', 'project_version_id').first()
        project_id = project_data['bind_project_id']
        project_version_id = project_data['project_version_id']

        queryset = Asset.objects.filter(agent_id=agent_id)
        license_dict = {
            i['sha_1']: i['license']
            for i in ScaMavenDb.objects.filter(sha_1__in=queryset.values(
                'signature_value')).values('license', 'sha_1')
        }
        return R.success(
            data=ScaSerializer(queryset.select_related('level', 'agent'),
                               context={
                                   'license_dict': license_dict
                               },
                               many=True).data)
