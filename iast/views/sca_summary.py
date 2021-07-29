#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午12:23
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from dongtai.models.vul_level import IastVulLevel

from iast.base.agent import get_agents_with_project, get_sca_count
from iast.base.project_version import get_project_version
from iast.views.vul_summary import VulSummary


class ScaSummary(UserEndPoint):
    name = "rest-api-sca-summary"
    description = "三方组件概览"

    def get(self, request):
        """
        应用漏洞总览接口
        - 语言
        - 漏洞等级
        - 漏洞类型
        - 应用程序
        :param request:
        :return:
        """

        end = {
            "status": 201,
            "msg": "success",
            "data": {}
        }
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)

        language = request.query_params.get('language')
        if language:
            auth_agents = auth_agents.filter(language=language)

        project_id = request.query_params.get('project_id')
        if project_id and project_id != '':
            # 获取项目当前版本信息
            current_project_version = get_project_version(project_id, auth_users)
            auth_agents = auth_agents.filter(
                bind_project_id=project_id,
                online=1,
                project_version_id=current_project_version.get("version_id", 0)
            )

        queryset = Asset.objects.filter(agent__in=auth_agents)

        level = request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)

        package_kw = request.query_params.get('keyword', None)
        if package_kw and package_kw.strip() != '':
            queryset = queryset.filter(package_name__icontains=package_kw)

        level_summary = queryset.values('level').order_by('level').annotate(total=Count('level'))
        levelInfo = IastVulLevel.objects.all()
        levelNameArr = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if levelInfo:
            for level_item in levelInfo:
                DEFAULT_LEVEL[level_item.name_value] = 0
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

        end['data']['language'] = VulSummary.get_languages(queryset.values('agent_id'))
        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}
        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': levelNameArr[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]
        end['data']['projects'] = get_sca_count(auth_users, auth_agents.values('id'), project_id)

        return R.success(data=end['data'])
