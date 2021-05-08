#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午12:23
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from django.db.models import Q
from rest_framework.request import Request

from base import R
from iast.base.agent import get_project_vul_count
from iast.base.user import UserEndPoint
from dongtai_models.models.project import IastProject
from dongtai_models.models.vul_level import IastVulLevel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel


class VulnSummary(UserEndPoint):
    name = "rest-api-vulnerability-summary"
    description = "应用漏洞概览"

    def get(self, request: Request):
        """
        应用漏洞总览接口
        - 语言
        - 漏洞等级
        - 漏洞类型
        - 应用程序
        :param request:
        :return: {
            "status": 201,
            "msg": "success",
            "data": {
                "language": {
                    "Java": 60,
                    ".NET": 60
                },
                "level": {
                    "critical": 10,
                    "high": 20,
                    "medium": 30,
                    "low": 10,
                    "note": 0
                },
                "type": {
                    "sql injection": 40,
                    "cmd injection": 40,
                    "xpath injection": 40,
                    "ldap injection": 40,
                    "ognl injection": 40,
                    "el injection": 40
                },

                "application": {
                    "struts2-test": 20
                }
            }
        }
        """
        DEFAULT_LANGUAGE = {"JAVA": 0, ".NET": 0}

        end = {
            "status": 201,
            "msg": "success",
            "level_data": [],
            "data": {}
        }

        # 提取过滤条件
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        queryset = IastVulnerabilityModel.objects.filter(agent__in=auth_agents)
        user = request.user

        # icontains
        url = request.query_params.get('url', None)
        levelInfo = IastVulLevel.objects.all()
        levelNameArr = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if levelInfo:
            for level_item in levelInfo:
                DEFAULT_LEVEL[level_item.name_value] = 0
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value
        # 动态创建
        condition = Q()

        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)

        level = request.query_params.get('level')
        if level:
            queryset = queryset.filter(level=level)

        vul_type = request.query_params.get('type')
        if vul_type:
            queryset = queryset.filter(type=vul_type)

        if url and url != '':
            queryset = queryset.filter(url__icontains=url)

        project_name = request.query_params.get('project_name')  # 项目名称， fixme 后续统一修改
        if project_name and project_name != '':
            projects = IastProject.objects.filter(user__in=auth_users, name__icontains=project_name).values("id")
            project_ids = [project["id"] for project in projects]
            auth_agents = auth_agents.filter(bind_project_id__in=project_ids)

        project_id = request.query_params.get('projectId')  # 项目名称， fixme 后续统一修改
        if project_id and project_id != '':
            auth_agents = auth_agents.filter(bind_project_id=project_id)

        datas = queryset.filter(agent__in=auth_agents).values('language', 'level', 'type', 'agent')

        language_summary = datas.values('language').order_by('language').annotate(total=Count('language'))
        level_summary = datas.values('level').order_by('level').annotate(total=Count('level'))
        type_summary = datas.values('type').order_by('type').annotate(total=Count('type'))

        _temp_data = {_['language']: _['total'] for _ in language_summary}

        DEFAULT_LANGUAGE.update(_temp_data)
        end['data']['language'] = [{'language': _key, 'count': _value} for _key, _value in DEFAULT_LANGUAGE.items()]

        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}

        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': levelNameArr[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]

        # result = sorted(result, key=lambda x: x['count'], reverse=True)
        vul_type_list = [{"type": _['type'], "count": _['total']} for _ in type_summary]
        end['data']['type'] = sorted(vul_type_list, key=lambda x: x['count'], reverse=True)
        end['data']['projects'] = get_project_vul_count(auth_users)

        return R.success(data=end['data'], level_data=end['level_data'])

    @staticmethod
    def get_level_name(id):
        return IastVulLevel.objects.get(id=id).name_value
