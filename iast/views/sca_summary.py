#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from dongtai.models.vul_level import IastVulLevel

from iast.base.agent import get_project_vul_count,get_agent_languages
from iast.base.project_version import get_project_version, get_project_version_by_id
from iast.views.vul_summary import VulSummary
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from iast.serializers.vul import VulSummaryTypeSerializer, VulSummaryProjectSerializer, VulSummaryLevelSerializer, VulSummaryLanguageSerializer
from rest_framework import serializers

class _ScaSummaryResponseDataSerializer(serializers.Serializer):
    language = VulSummaryLanguageSerializer(many=True)
    level = VulSummaryLevelSerializer(many=True)
    projects = VulSummaryProjectSerializer(many=True)


_ResponseSerializer = get_response_serializer(
    _ScaSummaryResponseDataSerializer())

class ScaSummary(UserEndPoint):
    name = "rest-api-sca-summary"
    description = _("Three-party components overview")

    @extend_schema_with_envcheck(
        [
            {
                'name': "page",
                'type': int,
                'default': 1,
                'required': False,
                'description': _('Page index'),
            },
            {
                'name': "pageSize",
                'type': int,
                'default': 20,
                'required': False,
                'description': _('Number per page'),
            },
            {
                'name': "language",
                'type': str,
                'description': _("programming language"),
            },
            {
                'name': "project_name",
                'type': str,
                'deprecated': True,
                'description': _('Name of Project'),
            },
            {
                'name': "project_id",
                'type': int,
                'description': _('Id of Project'),
            },
            {
                'name': "level",
                'type': int,
                'description': _('The id level of vulnerability'),
            },
            {
                'name':
                "version_id",
                'type':
                int,
                'description':
                _("The default is the current version id of the project.")
            },
            {
                'name': "keyword",
                'type': str,
                'description':
                _("Fuzzy keyword search field for package_name.")
            },
            {
                'name':
                "order",
                'type':
                str,
                'description':
                format_lazy(
                    "{} : {}", _('Sorted index'), ",".join([
                        'version', 'level', 'vul_count', 'language',
                        'package_name'
                    ]))
            },
        ], [], [
            {
                'name':
                _('Get data sample'),
                'description':
                _("The aggregation results are programming language, risk level, vulnerability type, project"
                  ),
                'value': {
                    "status": 201,
                    "msg": "success",
                    "data": {
                        "language": [
                            {
                                "language": "JAVA",
                                "count": 17
                            }, {
                                "language": "PYTHON",
                                "count": 0
                            }
                        ],
                        "level": [
                            {
                                "level": "HIGH",
                                "count": 0,
                                "level_id": 1
                            }, {
                                "level": "MEDIUM",
                                "count": 0,
                                "level_id": 2
                            }, {
                                "level": "LOW",
                                "count": 0,
                                "level_id": 3
                            }, {
                                "level": "INFO",
                                "count": 17,
                                "level_id": 4
                            }
                        ],
                        "projects": [
                            {
                                "project_name": "demo",
                                "count": 17,
                                "id": 67
                            }
                        ]
                    }
                }
            }
        ],
        tags=[_('Component')],
        summary=_("Component Summary (with project)"),
        description=
        _("Use the specified project information to get the corresponding component summary"
          ),
        response_schema=_ResponseSerializer)
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
            try:
                level = int(level)
            except:
                return R.failure(_("Parameter error")) 
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
        agent_count = queryset.values('agent_id').annotate(count=Count('agent_id'))
        end['data']['language'] = get_agent_languages(agent_count)
        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}
        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': levelNameArr[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]

        end['data']['projects'] = get_project_vul_count(auth_users, agent_count, auth_agents.values('id'), project_id)

        return R.success(data=end['data'])
