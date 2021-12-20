#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi

import json
import re
import time

from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.server import IastServer
from dongtai.models.vulnerablity import IastVulnerabilityModel
from django.utils.translation import gettext_lazy as _
from dongtai.models.hook_type import HookType
from iast.base.project_version import get_project_version
from dongtai.models.strategy import IastStrategyModel

def get_agents_with_project(project_name, users):
    """
    :param project_name:
    :param users:
    :return:
    """
    agent_ids = []
    if project_name and project_name != '':
        project_queryset = IastProject.objects.filter(user__in=users, name__icontains=project_name).values("id")
        project_ids = []

        if project_queryset:
            for pro_item in project_queryset:
                project_ids.append(pro_item['id'])

            relations = IastAgent.objects.filter(bind_project_id__in=project_ids).values("id")
            agent_ids = [relation['id'] for relation in relations]

    return agent_ids


def get_user_project_name(auth_users):
    project_models = IastProject.objects.filter(user__in=auth_users).values("id", "name")
    projects_info = {}
    if project_models:
        for item in project_models:
            projects_info[item['id']] = item['name']
    return projects_info


def get_user_agent_pro(auth_users, bindId):
    agentInfo = IastAgent.objects.filter(
        user__in=auth_users,
        bind_project_id__in=bindId
    ).values("id", "bind_project_id", "server_id")
    result = {"pidArr": {}, "serverArr": {}, "server_ids": []}

    if agentInfo:
        for item in agentInfo:
            result["pidArr"][item['id']] = item['bind_project_id']
            result["serverArr"][item['id']] = item['server_id']
            result["server_ids"].append(item['server_id'])
    return result


def get_all_server(ids):
    alls = IastServer.objects.filter(id__in=ids).values("id", "container")
    result = {}
    if alls:
        for item in alls:
            result[item['id']] = item['container']
    return result


def get_project_vul_count(users, queryset, auth_agents, project_id=None):
    result = list()
    project_queryset = IastProject.objects.filter(user__in=users)
    if project_queryset.values('id').exists() is False:
        return result
    if project_id:
        project_queryset = project_queryset.filter(id=project_id)

    project_queryset = project_queryset.values('name', 'id')
    for project in project_queryset:
        project_id = project['id']
        current_version = get_project_version(project_id, users)
        version_id = current_version.get("version_id", 0)
        agent_queryset = auth_agents.filter(project_version_id=version_id,
                                            bind_project_id=project_id)
        if agent_queryset.values('id').exists() is False:
            result.append({
                "project_name": project['name'],
                "count": 0,
                "id": project_id
            })
        else:
            result.append({
                "project_name": project['name'],
                "count": queryset.filter(agent__in=agent_queryset).values('id').count(),
                "id": project_id
            })
    result = sorted(result, key=lambda item: item['count'], reverse=True)[:5]
    return result


def change_dict_key(dic, keypair):
    for k, v in keypair.items():
        dic[v] = dic.pop(k)
    return dic


def get_vul_count_by_agent(agent_ids, vid, user):
    queryset = IastVulnerabilityModel.objects.filter(
        agent_id__in=agent_ids)
    typeInfo = queryset.values().order_by("level")
    if vid:
        typeInfo = typeInfo.filter(id=vid)
    type_summary = []
    levelCount = {}
    vulDetail = {}
    strategy_ids = queryset.values_list('strategy_id',
                                        flat=True).distinct()
    strategys = {
        strategy['id']: strategy
        for strategy in IastStrategyModel.objects.filter(
            pk__in=strategy_ids).values('id', 'vul_name').all()
    }
    hook_type_ids = queryset.values_list('hook_type_id',
                                         flat=True).distinct()
    hooktypes = {
        hooktype['id']: hooktype
        for hooktype in HookType.objects.filter(
            pk__in=hook_type_ids).values('id', 'name').all()
    }
    if typeInfo:
        typeArr = {}
        typeLevel = {}
        for one in typeInfo:
            hook_type = hooktypes.get('hook_type_id', None)
            hook_type_name = hook_type['name'] if hook_type else None
            strategy = strategys.get('strategy_id', None)
            strategy_name = strategy['vul_name'] if strategy else None
            type_ = list(
                filter(lambda x: x is not None, [strategy_name, hook_type_name]))
            one['type']= type_[0] if type_ else ''
            typeArr[one['type']] = typeArr.get(one['type'], 0) + 1
            typeLevel[one['type']] = one['level_id']
            levelCount[one['level_id']] = levelCount.get(one['level_id'], 0) + 1
            language = IastAgent.objects.filter(
                pk=one['agent_id']).values_list('language', flat=True).first()
            one['language'] = language if language is not None else ''
            if one['type'] not in vulDetail.keys():
                vulDetail[one['type']] = []
            detailStr1 = _("We found that there is {1} in the {0} page, attacker can modify the value of {2} to attack:").format(
                one['uri'], one['type'], one['taint_position'])

            try:
                one['req_params'] = str(one['req_params'])
            except Exception as e:
                one['req_params'] = ""
            detailStr2 = one['http_method'] + " " + one['uri'] + "?" + one['req_params'] + one['http_protocol']
            try:
                fileData = one['full_stack'][-1].get("stack", "")
                pattern = r'.*?\((.*?)\).*?'
                resMatch = re.match(pattern, fileData)
                uriArr = resMatch.group(1).split(":")
                fileName = uriArr[0]
                if len(uriArr) > 1:
                    rowStr = _("{} Line").format(str(uriArr[1]))
                else:
                    rowStr = ""
            except Exception as e:
                fileName = ""
                rowStr = ""
            classname = ""
            methodname = ""
            if one['full_stack']:
                try:
                    full_stack_arr = json.loads(one['full_stack'])
                    full_stack = full_stack_arr[-1]
                    classname = str(full_stack.get("classname", ""))
                    methodname = str(full_stack.get("methodname", ""))
                except Exception as e:
                    print("======")
            detailStr3 = _("In {} {} call {}. {} (), Incoming parameters {}").format(
                str(fileName), rowStr, classname, methodname,
                str(one['taint_value']))
            cur_tile = _("{} Appears in {} {}").format(one['type'],str(one['uri']),str(one['taint_position']))
            if one['param_name']:
                cur_tile = cur_tile + "\"" + str(one['param_name']) + "\""
            vulDetail[one['type']].append({
                "title": cur_tile,
                "type_name": one['type'],
                "level_id": one['level_id'],
                "first_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(one['first_time'])),
                "latest_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(one['latest_time'])),
                "language": one['language'],
                "url": one['url'],
                "detail_data": [detailStr1, detailStr2, detailStr3],
            })
        typeArrKeys = typeArr.keys()
        for item_type in typeArrKeys:
            type_summary.append(
                {
                    'type_name': item_type,
                    'type_count': typeArr[item_type],
                    'type_level': typeLevel[item_type]
                }
            )
    return {
        'type_summary': type_summary,
        'levelCount': levelCount,
        'vulDetail': vulDetail
    }
