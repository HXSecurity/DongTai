#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.base.agent import get_agents_with_project, get_user_project_name, \
    get_user_agent_pro, get_all_server
from iast.base.project_version import get_project_version, get_project_version_by_id
from iast.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from dongtai.models.hook_type import HookType
from django.db.models import Q


class VulsEndPoint(UserEndPoint):

    def get(self, request):
        """
        :param request:
        :return:
        """
        end = {
            "status": 201,
            "msg": "success",
            "data": []
        }
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        if auth_agents is None:
            return R.success(page={}, data=[], msg=_('No data'))

        language = request.query_params.get('language')
        if language:
            auth_agents = auth_agents.filter(language=language)

        queryset = IastVulnerabilityModel.objects.values(
            'id', 'hook_type_id', 'url', 'uri', 'agent_id', 'level_id',
            'http_method', 'top_stack', 'bottom_stack', 'taint_position',
            'latest_time', 'first_time',
            'status_id').filter(agent__in=auth_agents)

        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        type_ = request.query_params.get('type')
        if type_:
            hook_type = HookType.objects.filter(name=type_).first()
            hook_type_id = hook_type.id if hook_type else 0
            queryset = queryset.filter(hook_type_id=hook_type_id)

        project_name = request.query_params.get('project_name')
        if project_name:
            agent_ids = get_agents_with_project(project_name, auth_users)
            queryset = queryset.filter(agent_id__in=agent_ids)

        project_id = request.query_params.get('project_id')
        if project_id:

            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
            agents = auth_agents.filter(
                bind_project_id=project_id,
                project_version_id=current_project_version.get("version_id", 0))
            queryset = queryset.filter(agent_id__in=agents)

        url = request.query_params.get('url', None)
        if url and url != '':
            queryset = queryset.filter(url__icontains=url)
        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status__name=status)

        status_id = request.query_params.get('status_id')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        order = request.query_params.get('order')
        if order:
            if order == 'type':
                order = 'hook_type_id'
            if order == '-type':
                order = '-hook_type_id'
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-latest_time')

        q = ~Q(hook_type_id=0)
        queryset = queryset.filter(q)
        projects_info = get_user_project_name(auth_users)
        agentArr = get_user_agent_pro(auth_users, projects_info.keys())
        agentPro = agentArr['pidArr']
        agentServer = agentArr['serverArr']
        server_ids = agentArr['server_ids']
        allServer = get_all_server(server_ids)
        allType = IastVulLevel.objects.all().order_by("id")
        allTypeArr = {}
        if allType:
            for item in allType:
                allTypeArr[item.id] = item.name_value

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get("pageSize", 20)
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        datas = VulSerializer(page_data, many=True).data
        pro_length = len(datas)
        if pro_length > 0:
            for index in range(pro_length):
                item = datas[index]
                item['index'] = index
                item['project_name'] = projects_info.get(
                    agentPro.get(item['agent_id'], 0),
                    _("The application has not been binded"))
                item['project_id'] = agentPro.get(item['agent_id'], 0)
                item['server_name'] = allServer.get(
                    agentServer.get(item['agent_id'], 0), "JavaApplication")
                item['server_type'] = VulSerializer.split_container_name(
                    item['server_name'])

                item['level_type'] = item['level_id']
                item['level'] = allTypeArr.get(item['level_id'], "")
                end['data'].append(item)
        end['page'] = page_summary
        return R.success(page=page_summary, data=end['data'])
