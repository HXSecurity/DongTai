#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:15
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from base import R
from iast.base.agent import get_agents_with_project
from iast.base.sca import ScaEndPoint
from dongtai.models.asset import Asset
from iast.serializers.sca import ScaSerializer
from iast.base.project_version import get_project_version


class ScaList(ScaEndPoint):
    def get(self, request):
        """
        获取三方组件列表
        - 支持排序
        - 支持搜索
        - 支持分页
        :param request:
        :return:
        """
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)

        language = request.query_params.get('language')
        if language:
            auth_agents = auth_agents.filter(language=language)

        queryset = Asset.objects.filter(agent__in=auth_agents)

        order = request.query_params.get('order', None)
        package_kw = request.query_params.get('keyword', None)

        project_id = request.query_params.get('project_id', None)
        if project_id and project_id != '':
            # 获取项目当前版本信息
            current_project_version = get_project_version(project_id, auth_users)
            agents = self.get_auth_agents(auth_users).filter(
                bind_project_id=project_id,
                online=1,
                project_version_id=current_project_version.get("version_id", 0)
            )
            queryset = queryset.filter(agent__in=agents)
        project_name = request.query_params.get('project_name')
        if project_name and project_name != '':
            agent_ids = get_agents_with_project(project_name, auth_users)
            if agent_ids:
                queryset = queryset.filter(agent_id__in=agent_ids)

        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        if package_kw and package_kw.strip() != '':
            queryset = queryset.filter(package_name__icontains=package_kw)

        if order:
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-dt')

        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 20)
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=ScaSerializer(page_data, many=True).data, page=page_summary)
