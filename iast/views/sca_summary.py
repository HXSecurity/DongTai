#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from dongtai.models.vul_level import IastVulLevel

from iast.base.agent import get_project_vul_count
from iast.base.project_version import get_project_version, get_project_version_by_id
from iast.views.vul_summary import VulSummary
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck


class ScaSummary(UserEndPoint):
    name = "rest-api-sca-summary"
    description = _("Three-party components overview")

    @extend_schema_with_envcheck([
        {
            'name': "page",
            'type': int,
            'default': 1,
            'required': False,
        },
        {
            'name': "pageSize",
            'type': int,
            'default': 20,
            'required': False,
        },
        {
            'name': "language",
            'type': str,
        },
        {
            'name': "project_name",
            'type': str,
            'deprecated': True,
        },
        {
            'name': "level",
            'type': str,
        },
        {
            'name': "project_id",
            'type': int,
        },
        {
            'name': "version_id",
            'type': int,
            'description':
            "The default is the current version id of the project."
        },
        {
            'name': "keyword",
            'type': str,
        },
        {
            'name': "order",
            'type': str,
        },
    ])
    def get(self, request):
        """
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
            
            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
            auth_agents = auth_agents.filter(
                bind_project_id=project_id,
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
        end['data']['projects'] = get_project_vul_count(auth_users, queryset, auth_agents.values('id'), project_id)

        return R.success(data=end['data'])
