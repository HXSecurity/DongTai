#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午12:23
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.base.agent import get_project_vul_count
from iast.base.project_version import get_project_version


class VulSummary(UserEndPoint):
    name = "rest-api-vulnerability-summary"
    description = "应用漏洞概览"

    @staticmethod
    def get_languages(agent_items):
        default_language = {"JAVA": 0, "PYTHON": 0}
        agent_ids = dict()
        for agent_item in agent_items:
            agent_id = agent_item['agent_id']
            if agent_id not in agent_ids:
                agent_ids[agent_id] = 0
            agent_ids[agent_id] = agent_ids[agent_id] + 1

        language_agents = dict()
        language_items = IastAgent.objects.filter(id__in=agent_ids.keys()).values('id', 'language')
        for language_item in language_items:
            language_agents[language_item['id']] = language_item['language']

        for agent_id, count in agent_ids.items():
            default_language[language_agents[agent_id]] = count + default_language[language_agents[agent_id]]
        return [{'language': _key, 'count': _value} for _key, _value in default_language.items()]

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
            "level_data": [],
            "data": {}
        }

        # 提取过滤条件
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        queryset = IastVulnerabilityModel.objects.all()

        vul_level = IastVulLevel.objects.all()
        vul_level_metadata = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if vul_level:
            for level_item in vul_level:
                DEFAULT_LEVEL[level_item.name_value] = 0
                vul_level_metadata[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

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

        queryset = queryset.filter(agent__in=auth_agents)

        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        vul_type = request.query_params.get('type')
        if vul_type:
            queryset = queryset.filter(type=vul_type)

        url = request.query_params.get('url')
        if url and url != '':
            queryset = queryset.filter(url__icontains=url)

        level_summary = queryset.values('level').order_by('level').annotate(total=Count('level'))
        type_summary = queryset.values('type').order_by('type').annotate(total=Count('type'))

        end['data']['language'] = self.get_languages(queryset.values('agent_id'))

        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}

        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': vul_level_metadata[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]

        vul_type_list = [{"type": _['type'], "count": _['total']} for _ in type_summary]
        end['data']['type'] = sorted(vul_type_list, key=lambda x: x['count'], reverse=True)
        end['data']['projects'] = get_project_vul_count(users=auth_users, queryset=queryset, auth_agents=auth_agents,
                                                        project_id=project_id)

        return R.success(data=end['data'], level_data=end['level_data'])

    @staticmethod
    def get_level_name(id):
        return IastVulLevel.objects.get(id=id).name_value
