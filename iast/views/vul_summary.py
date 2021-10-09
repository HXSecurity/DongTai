#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel

from iast.base.agent import get_project_vul_count
from iast.base.project_version import get_project_version, get_project_version_by_id
from django.utils.translation import gettext_lazy as _
from dongtai.models.hook_type import HookType
from django.db.models import Q
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework import serializers
from iast.serializers.vul import VulSummaryTypeSerializer, VulSummaryProjectSerializer, VulSummaryLevelSerializer, VulSummaryLanguageSerializer


class VulSummaryResponseDataSerializer(serializers.Serializer):
    language = VulSummaryLanguageSerializer(many=True)
    level = VulSummaryLevelSerializer(many=True)
    type = VulSummaryTypeSerializer(many=True)
    projects = VulSummaryProjectSerializer(many=True)


_ResponseSerializer = get_response_serializer(
    VulSummaryResponseDataSerializer())


class VulSummary(UserEndPoint):
    name = "rest-api-vulnerability-summary"
    description = _("Applied vulnerability overview")

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
        language_items = IastAgent.objects.filter(
            id__in=agent_ids.keys()).values('id', 'language')
        for language_item in language_items:
            language_agents[language_item['id']] = language_item['language']

        for agent_id, count in agent_ids.items():
            default_language[
                language_agents[agent_id]] = count + default_language[
                    language_agents[agent_id]]
        return [{
            'language': _key,
            'count': _value
        } for _key, _value in default_language.items()]

    @extend_schema_with_envcheck(
        [
            {
                'name': "language",
                'type': str,
                'description': _("programming language")
            },
            {
                'name': "type",
                'type': str,
                'description': _('Type of vulnerability'),
            },
            {
                'name': "project_name",
                'type': str,
                'deprecated': True,
                'description': _('Name of Project'),
            },
            {
                'name':
                "level",
                'type':
                int,
                'description':
                format_lazy("{} : {}", _('Level of vulnerability'), "1,2,3,4")
            },
            {
                'name': "project_id",
                'type': int,
                'description': _('Id of Project'),
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
                'name': "status",
                'type': str,
                'deprecated': True,
                'description': _('Name of status'),
            },
            {
                'name': "status_id",
                'type': int,
                'description': _('Id of status'),
            },
            {
                'name': "url",
                'type': str,
                'description': _('The URL corresponding to the vulnerability'),
            },
            {
                'name':
                "order",
                'type':
                str,
                'description':
                format_lazy(
                    "{} : {}", _('Sorted index'), ",".join(
                        ['type', 'type', 'first_time', 'latest_time', 'url']))
            },
        ],
        [],
        [{
            'name':
            _('Get data sample'),
            'description':
            _("The aggregation results are programming language, risk level, vulnerability type, project"
              ),
            'value': {
                "status": 201,
                "msg": "success",
                "data": {
                    "language": [{
                        "language": "JAVA",
                        "count": 136
                    }, {
                        "language": "PYTHON",
                        "count": 0
                    }],
                    "level": [{
                        "level": "HIGH",
                        "count": 116,
                        "level_id": 1
                    }, {
                        "level": "MEDIUM",
                        "count": 16,
                        "level_id": 2
                    }, {
                        "level": "LOW",
                        "count": 4,
                        "level_id": 3
                    }, {
                        "level": "INFO",
                        "count": 0,
                        "level_id": 4
                    }],
                    "type": [{
                        "type": "Path Traversal",
                        "count": 79
                    }, {
                        "type": "OS Command Injection",
                        "count": 26
                    }, {
                        "type": "Cross-Site Scripting",
                        "count": 16
                    }, {
                        "type": "SQL Injection",
                        "count": 9
                    }, {
                        "type": "Weak Random Number Generation",
                        "count": 2
                    }, {
                        "type": "Hibernate Injection",
                        "count": 2
                    }, {
                        "type": "Insecure Hash Algorithms",
                        "count": 1
                    }, {
                        "type": "Arbitrary Server Side Forwards",
                        "count": 1
                    }],
                    "projects": [{
                        "project_name": "demo1",
                        "count": 23,
                        "id": 58
                    }, {
                        "project_name": "demo3",
                        "count": 4,
                        "id": 63
                    }, {
                        "project_name": "demo",
                        "count": 2,
                        "id": 67
                    }, {
                        "project_name": "demo4",
                        "count": 2,
                        "id": 69
                    }, {
                        "project_name": "demo5",
                        "count": 1,
                        "id": 71
                    }]
                },
                "level_data": []
            }
        }],
        tags=[_('Vulnerability')],
        summary=_('Vulnerability Summary'),
        description=
        _('Use the following conditions to view the statistics of the number of vulnerabilities in the project.'
          ),
        response_schema=_ResponseSerializer
    )
    def get(self, request):
        """
        :param request:
        :return:
        """

        end = {
            "status": 201,
            "msg": "success",
            "level_data": [],
            "data": {}
        }


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

        queryset = queryset.filter(agent__in=auth_agents)

        status = request.query_params.get('status')
        if status:
            queryset = queryset.filter(status__name=status)
        status_id = request.query_params.get('status_id')
        if status_id:
            queryset = queryset.filter(status_id=status_id)

        level = request.query_params.get('level')
        if level:
            try:
                level = int(level)
            except:
                return R.failure(_("Parameter error")) 
            queryset = queryset.filter(level=level)

        vul_type = request.query_params.get('type')
        if vul_type:
            hook_type = HookType.objects.filter(name=vul_type).first()
            vul_type_id = hook_type.id if hook_type else 0
            queryset = queryset.filter(hook_type_id=vul_type_id)

        url = request.query_params.get('url')
        if url and url != '':
            queryset = queryset.filter(url__icontains=url)

        q = ~Q(hook_type_id=0)
        queryset = queryset.filter(q)

        level_summary = queryset.values('level').order_by('level').annotate(total=Count('level'))
        type_summary = queryset.values('hook_type_id').order_by(
            'hook_type_id').annotate(total=Count('hook_type_id'))

        end['data']['language'] = self.get_languages(queryset.values('agent_id'))

        _temp_data = {levelIdArr[_['level']]: _['total'] for _ in level_summary}

        DEFAULT_LEVEL.update(_temp_data)
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': vul_level_metadata[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]

        vul_type_list = [{
            "type": get_hook_type_name(_),
            "count": _['total']
        } for _ in type_summary]
        end['data']['type'] = sorted(vul_type_list,
                                     key=lambda x: x['count'],
                                     reverse=True)
        end['data']['projects'] = get_project_vul_count(
            users=auth_users,
            queryset=queryset,
            auth_agents=auth_agents,
            project_id=project_id)

        return R.success(data=end['data'], level_data=end['level_data'])

    @staticmethod
    def get_level_name(id):
        return IastVulLevel.objects.get(id=id).name_value


def get_hook_type_name(obj):
    hook_type = HookType.objects.filter(pk=obj['hook_type_id']).first()
    return  hook_type.name if hook_type else ''
