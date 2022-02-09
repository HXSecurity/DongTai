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
from dongtai.models.strategy import IastStrategyModel

from iast.base.agent import get_project_vul_count
from iast.base.project_version import get_project_version, get_project_version_by_id
from django.utils.translation import gettext_lazy as _
from dongtai.models.hook_type import HookType
from django.db.models import Q
import copy,time


class VulSummaryType(UserEndPoint):
    name = "rest-api-vulnerability-summary-type"
    description = _("Applied vulnerability overview")

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
        queryset = IastVulnerabilityModel.objects.filter()

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
            hook_types = HookType.objects.filter(name=vul_type).all()
            strategys = IastStrategyModel.objects.filter(vul_name=vul_type).all()
            q = Q(hook_type__in=hook_types,strategy_id=0) | Q(strategy__in=strategys)
            queryset = queryset.filter(q)

        url = request.query_params.get('url')
        if url and url != '':
            queryset = queryset.filter(url__icontains=url)

        q = ~Q(hook_type_id=0)
        queryset = queryset.filter(q)

        # 汇总 level
        vul_level = IastVulLevel.objects.all()
        vul_level_metadata = {}
        levelIdArr = {}
        DEFAULT_LEVEL = {}
        if vul_level:
            for level_item in vul_level:
                DEFAULT_LEVEL[level_item.name_value] = 0
                vul_level_metadata[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value
        level_summary = queryset.values('level').order_by('level').annotate(total=Count('level'))
        for temp in level_summary:
            DEFAULT_LEVEL[levelIdArr[temp['level']]] = temp['total']
        end['data']['level'] = [{
            'level': _key, 'count': _value, 'level_id': vul_level_metadata[_key]
        } for _key, _value in DEFAULT_LEVEL.items()]

        # 汇总 type
        type_summary = queryset.values(
            'hook_type_id', 'strategy_id', 'hook_type__name',
            'strategy__vul_name').order_by('hook_type_id').annotate(
            total=Count('hook_type_id'))
        type_summary = list(type_summary)

        vul_type_list = [{
            "type": get_hook_type_name(_).lower().strip(),
            "count": _['total']
        } for _ in type_summary]

        tempdic = {}
        for vul_type in vul_type_list:
            if tempdic.get(vul_type['type'], None):
                tempdic[vul_type['type']]['count'] += vul_type['count']
            else:
                tempdic[vul_type['type']] = vul_type
        vul_type_list = tempdic.values()
        end['data']['type'] = sorted(vul_type_list, key=lambda x: x['count'], reverse=True)

        return R.success(data=end['data'], level_data=end['level_data'])


def get_hook_type_name(obj):
    #hook_type = HookType.objects.filter(pk=obj['hook_type_id']).first()
    #hook_type_name = hook_type.name if hook_type else None
    #strategy = IastStrategyModel.objects.filter(pk=obj['strategy_id']).first()
    #strategy_name = strategy.vul_name if strategy else None
    #type_ = list(
    #    filter(lambda x: x is not None, [strategy_name, hook_type_name]))
    type_ = list(
        filter(lambda x: x is not None, [
            obj.get('strategy__vul_name', None),
            obj.get('hook_type__name', None)
        ]))
    return type_[0] if type_ else ''