#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/26 下午12:41
# software: PyCharm
# project: lingzhi-webapi

import json
import re
import time

from base.endpoint import MixinAuthEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.asset import Asset
from dongtai_models.models.project import IastProject
from dongtai_models.models.server import IastServerModel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel
from iast.permissions import ScopedPermission


def get_agents_with_project(project_name, queryset, users):
    """
    根据项目名称和授权的用户列表查询有权限访问的agent列表
    :param project_name:项目名称
    :param queryset:无效字段，不传
    :param users:当前有权限的用户列表，如果是普通用户，该字段为[user]
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


def get_agentId_project_id(project_id, queryset, user):
    agents = IastAgent.objects.filter(bind_project_id=project_id).values("id")
    if user and user.is_talent_admin() is False:
        agents = agents.filter(user=user)
    agent_ids = [agent['id'] for agent in agents]
    return agent_ids


# 获取用户所有项目
def get_user_project_name(auth_users):
    project_models = IastProject.objects.filter(user__in=auth_users).values("id", "name")
    projects_info = {}
    if project_models:
        for item in project_models:
            projects_info[item['id']] = item['name']
    return projects_info


# 获取用户所有agent项目ID
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


# 根据server_id 获取所有 server_name
def get_all_server(ids):
    alls = IastServerModel.objects.filter(id__in=ids).values("id", "container")
    result = {}
    if alls:
        for item in alls:
            result[item['id']] = item['container']
    return result


# 获取项目漏洞数量
def get_project_vul_count(users):
    result = []
    projects = IastProject.objects.filter(user__in=users).values("name", "vul_count", "id")

    if projects:
        for project in projects:
            try:
                agents = IastAgent.objects.filter(bind_project_id=project['id'], user__in=users)
                vul_count = IastVulnerabilityModel.objects.filter(agent__in=agents).count()
            except Exception:
                vul_count = 0
            result.append({
                "project_name": project['name'],
                "count": vul_count
            })
    result = sorted(result, key=lambda x: x['count'], reverse=True)
    result = result[0:5]
    return result


def get_sca_count(users):
    result = []

    projects = IastProject.objects.filter(user__in=users).values("name", "vul_count", "id")
    if projects:
        for project in projects:
            try:
                agents = IastAgent.objects.filter(bind_project_id=project['id'])
                vul_count = Asset.objects.filter(agent__in=agents).count()
            except Exception:
                vul_count = 0
            result.append({
                "project_name": project['name'],
                "count": vul_count
            })
    result = sorted(result, key=lambda x: x['count'], reverse=True)
    result = result[0:5]
    return result


# 通过agent_id 获取 漏洞分类汇总 详情
# 漏洞类型 漏洞危害等级 首次发现时间 最近发现时间 漏洞地址  漏洞详情  编码语言
def get_vul_count_by_agent(agent_ids, vid, user):
    typeInfo = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids).values().order_by("level")
    if vid:
        typeInfo = typeInfo.filter(id=vid)
    type_summary = []
    levelCount = {}
    # 漏洞详情
    vulDetail = {}
    if typeInfo:
        typeArr = {}
        typeLevel = {}
        for one in typeInfo:
            typeArr[one['type']] = typeArr.get(one['type'], 0) + 1
            typeLevel[one['type']] = one['level_id']
            levelCount[one['level_id']] = levelCount.get(one['level_id'], 0) + 1
            if one['type'] not in vulDetail.keys():
                vulDetail[one['type']] = []
            detailStr1 = "我们发现在{0}页面中存在{1}，攻击者可以改变{2}的值进行攻击：".format(
                one['uri'], one['type'], one['taint_position'])

            try:
                one['req_params'] = str(one['req_params'])
            except Exception as e:
                one['req_params'] = ""
            detailStr2 = one['http_method'] + " " + one['uri'] + "?" + one['req_params'] + one['http_protocol']
            # 获取最新漏洞文件
            try:
                fileData = one['full_stack'][-1].get("stack", "")
                pattern = r'.*?\((.*?)\).*?'
                resMatch = re.match(pattern, fileData)
                uriArr = resMatch.group(1).split(":")
                fileName = uriArr[0]
                if len(uriArr) > 1:
                    rowStr = "的" + str(uriArr[1]) + "行"
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
            detailStr3 = "在" + str(fileName) + rowStr + "调用" + classname + "." + methodname + "(),传入参数" + str(
                one['taint_value'])
            cur_tile = one['type'] + "出现在" + str(one['uri']) + "的" + str(one['taint_position'])
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


class AgentPermission(ScopedPermission):
    def has_permission(self, request, view):
        user = request.user
        if user is not None and user.is_active:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class AgentEndPoint(MixinAuthEndPoint):
    permission_classes = (AgentPermission,)
