#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset

from iast.base.agent import get_agents_with_project
from iast.base.project_version import get_project_version, get_project_version_by_id
from iast.serializers.sca import ScaSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from iast.utils import get_model_order_options
from dongtai.models.sca_maven_db import ScaMavenDb

_ResponseSerializer = get_response_serializer(ScaSerializer(many=True))

class ScaList(UserEndPoint):
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
                'name': "level",
                'type': int,
                'description': _('The id of level of vulnerability'),
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
                    "status":
                    201,
                    "msg":
                    "success",
                    "data": [
                        {
                            "id": 13293,
                            "package_name": "message-business-7.1.0.Final.jar",
                            "version": "7.1.0.Final",
                            "project_name": "No application",
                            "project_id": 0,
                            "project_version": "No application version",
                            "language": "JAVA",
                            "agent_name":
                            "Mac OS X-bogon-v1.0.0-0c864ba2a60b48aaa1a8b49a53a6749b",
                            "signature_value":
                            "f744df92326c4bea7682fd16004bec184148db07",
                            "level": "INFO",
                            "level_type": 4,
                            "vul_count": 0,
                            "dt": 1631189450
                        }
                    ],
                    "page": {
                        "alltotal": 795,
                        "num_pages": 795,
                        "page_size": 1
                    }
                }
            }
        ],
        tags=[_('Component')],
        summary=_("Component List (with project)"),
        description=
        _("use the specified project information to obtain the corresponding component."
          ),
        response_schema=_ResponseSerializer)
    def get(self, request):
        """
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
        order_fields = [
            'level', 'package_name', 'vul_count', 'version', 'language', 'dt',
            'project_name'
        ]
        order = order if order in order_fields + list(
            map(lambda x: ''.join(['-', x]), order_fields)) else None

        package_kw = request.query_params.get('keyword', None)

        project_id = request.query_params.get('project_id', None)
        project_name = request.query_params.get('project_name')
        if project_id and project_id != '':

            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
            agents = self.get_auth_agents(auth_users).filter(
                bind_project_id=project_id,
                project_version_id=current_project_version.get(
                    "version_id", 0))
            queryset = queryset.filter(agent__in=agents)

        elif project_name and project_name != '':
            agent_ids = get_agents_with_project(project_name, auth_users)
            if agent_ids:
                queryset = queryset.filter(agent_id__in=agent_ids)

        level = request.query_params.get('level')
        if level:
            try:
                level = int(level)
            except:
                return R.failure(_("Parameter error")) 
            queryset = queryset.filter(level=level)

        if package_kw and package_kw.strip() != '':
            queryset = queryset.filter(package_name__icontains=package_kw)

        if order and order in get_model_order_options(Asset):
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-dt')
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get('pageSize', 20)
        page_summary, page_data = self.get_paginator(queryset.values('id','signature_value'), page, page_size)
        sca_ids = [i['id'] for i in  page_data]
        sca_sha1s = [i['signature_value'] for i in  page_data]
        license_dict = {
            i['sha_1']: i['license']
            for i in ScaMavenDb.objects.filter(sha_1__in=sca_sha1s).values('license', 'sha_1')
        }
        return R.success(data=ScaSerializer(Asset.objects.filter(pk__in=sca_ids).select_related('level', 'agent'),
                               context={
                                   'license_dict': license_dict
                               },many=True).data, page=page_summary)
