#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午12:23
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from rest_framework.request import Request

from base import R
from iast.base.agent import get_agents_with_project, get_sca_count
from iast.base.sca import ScaEndPoint
from dongtai_models.models.asset import Asset
from dongtai_models.models.vul_level import IastVulLevel


class ScaSummary(ScaEndPoint):
    name = "rest-api-sca-summary"
    description = "三方组件概览"

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
            "data": {}
        }
        auth_users = self.get_auth_users(request.user)
        agents = self.get_auth_agents(auth_users)
        queryset = Asset.objects.filter(agent__in=agents)

        language = request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language=language)

        level = request.query_params.get('level', None)
        if level:
            queryset = queryset.filter(level=level)

        project_id = request.query_params.get('project_id', None)
        if project_id and project_id != '':
            agents = self.get_auth_agents(auth_users).filter(bind_project_id=project_id)
            if agents:
                queryset = queryset.filter(agent__in=agents)

        project_name = request.query_params.get('project_name', None)
        if project_name and project_name != '':
            agent_ids = get_agents_with_project(project_name, queryset, auth_users)
            if agent_ids:
                queryset = queryset.filter(agent_id__in=agent_ids)
        package_kw = request.query_params.get('keyword', None)
        if package_kw and package_kw.strip() != '':
            queryset = queryset.filter(package_name__icontains=package_kw)

        datas = queryset.values('language', 'level', 'agent')

        language_summary = datas.values('language').order_by('language').annotate(total=Count('language'))
        level_summary = datas.values('level').order_by('level').annotate(total=Count('level'))
        levelInfo = IastVulLevel.objects.all()
        levelNameArr = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if levelInfo:
            for level_item in levelInfo:
                DEFAULT_LEVEL[level_item.name_value] = 0
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value
        _temp_data = {_['language']: _['total'] for _ in language_summary}
        # if language:
        #     end['data']['language'] = [{'language': _key, 'count': _value} for _key, _value in _temp_data.items()]
        # else:
        DEFAULT_LANGUAGE.update(_temp_data)
        end['data']['language'] = [{'language': _key, 'count': _value} for _key, _value in DEFAULT_LANGUAGE.items()]
        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}
        # if level:
        #     end['data']['level'] = [{
        #         'level': levelIdArr[_['level']], 'count': _['total'], 'level_id': _['level']
        #     } for _ in level_summary]
        # else:
        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': levelNameArr[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]
        end['data']['projects'] = get_sca_count(auth_users)
        return R.success(end['data'])
