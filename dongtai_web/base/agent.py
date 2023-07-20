#!/usr/bin/env python

import json
import re
import time

from django.utils.translation import gettext_lazy as _

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.program_language import IastProgramLanguage
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.server import IastServer
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel


def get_agents_with_project(project_name, users):
    """
    :param project_name:
    :param users:
    :return:
    """
    agent_ids = []
    if project_name and project_name != "":
        project_ids = (
            IastProject.objects.filter(user__in=users, name__icontains=project_name)
            .values_list("id", flat=True)
            .all()
        )

        if project_ids:
            agent_ids = (
                IastAgent.objects.filter(bind_project_id__in=project_ids)
                .values_list("id", flat=True)
                .all()
            )

    return agent_ids


def get_user_project_name(auth_users):
    project_models = IastProject.objects.filter(user__in=auth_users).values(
        "id", "name"
    )
    projects_info = {}
    if project_models:
        for item in project_models:
            projects_info[item["id"]] = item["name"]
    return projects_info


def get_user_agent_pro(auth_users, bindId):
    agentInfo = IastAgent.objects.filter(
        user__in=auth_users, bind_project_id__in=bindId
    ).values("id", "bind_project_id", "server_id")
    result = {"pidArr": {}, "serverArr": {}, "server_ids": []}

    if agentInfo:
        for item in agentInfo:
            result["pidArr"][item["id"]] = item["bind_project_id"]
            result["serverArr"][item["id"]] = item["server_id"]
            result["server_ids"].append(item["server_id"])
    return result


def get_all_server(ids):
    alls = IastServer.objects.filter(id__in=ids).values("id", "container")
    result = {}
    if alls:
        for item in alls:
            result[item["id"]] = item["container"]
    return result


# todo del edit by song
def get_project_vul_count_back(users, queryset, auth_agents, project_id=None):
    result = []
    project_queryset = IastProject.objects.filter(user__in=users)
    project_queryset = project_queryset.values("name", "id")
    if not project_queryset:
        return result
    if project_id:
        project_queryset = project_queryset.filter(id=project_id)

    versions = (
        IastProjectVersion.objects.filter(
            project_id__in=[project["id"] for project in project_queryset],
            status=1,
            current_version=1,
            user__in=users,
        )
        .values_list("id", "project_id")
        .all()
    )
    versions_map = {version[1]: version[0] for version in versions}
    # 需要 查询 指定项目 当前版本 绑定的agent 所对应的漏洞数量

    for project in project_queryset:
        project_id = project["id"]
        version_id = versions_map.get(project_id, 0)
        agent_queryset = auth_agents.filter(
            project_version_id=version_id, bind_project_id=project_id
        )

        count = queryset.filter(agent__in=agent_queryset).count()

        if count is False:
            result.append(
                {"project_name": project["name"], "count": 0, "id": project_id}
            )
        else:
            result.append(
                {"project_name": project["name"], "count": count, "id": project_id}
            )

    return sorted(result, key=lambda item: item["count"], reverse=True)[:5]


# add by song
def get_project_vul_count(users, queryset, auth_agents, project_id=None):
    result = []
    project_queryset = IastProject.objects.filter(user__in=users)
    project_queryset = project_queryset.values("name", "id")
    if not project_queryset:
        return result
    if project_id:
        project_queryset = project_queryset.filter(id=project_id)

    versions = (
        IastProjectVersion.objects.filter(
            project_id__in=[project["id"] for project in project_queryset],
            status=1,
            current_version=1,
            user__in=users,
        )
        .values_list("id", "project_id")
        .all()
    )
    versions_map = {version[1]: version[0] for version in versions}
    agentIdArr = {}
    for item in queryset:
        agentIdArr[item["agent_id"]] = item["count"]
    auth_agent_arr = auth_agents.values("project_version_id", "bind_project_id", "id")
    agent_list = {}
    for auth in auth_agent_arr:
        version_id = versions_map.get(auth["bind_project_id"], 0)
        if version_id == auth["project_version_id"]:
            if agent_list.get(auth["bind_project_id"], None) is None:
                agent_list[auth["bind_project_id"]] = []
            agent_list[auth["bind_project_id"]].append(auth["id"])

    # 需要 查询 指定项目 当前版本 绑定的agent 所对应的漏洞数量
    for project in project_queryset:
        project_id = project["id"]
        count = 0
        for agent_id in agent_list.get(project_id, []):
            count = count + int(agentIdArr.get(agent_id, 0))
        result.append(
            {"project_name": project["name"], "count": count, "id": project_id}
        )

    return sorted(result, key=lambda item: item["count"], reverse=True)[:5]


def change_dict_key(dic, keypair):
    for k, v in keypair.items():
        dic[v] = dic.pop(k)
    return dic


def get_vul_count_by_agent(agent_ids, vid, user):
    queryset = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids)
    typeInfo = queryset.values().order_by("level")
    if vid:
        typeInfo = typeInfo.filter(id=vid)
    type_summary = []
    levelCount = {}
    vulDetail = {}
    strategy_ids = queryset.values_list("strategy_id", flat=True).distinct()
    strategys = {
        strategy["id"]: strategy
        for strategy in IastStrategyModel.objects.filter(pk__in=strategy_ids)
        .values("id", "vul_name")
        .all()
    }
    hook_type_ids = queryset.values_list("hook_type_id", flat=True).distinct()
    hooktypes = {
        hooktype["id"]: hooktype
        for hooktype in HookType.objects.filter(pk__in=hook_type_ids)
        .values("id", "name")
        .all()
    }
    if typeInfo:
        typeArr = {}
        typeLevel = {}
        for one in typeInfo:
            hook_type = hooktypes.get(one["hook_type_id"], None)
            hook_type_name = hook_type["name"] if hook_type else None
            strategy = strategys.get(one["strategy_id"], None)
            strategy_name = strategy["vul_name"] if strategy else None
            type_ = list(
                filter(lambda x: x is not None, [strategy_name, hook_type_name])
            )
            one["type"] = type_[0] if type_ else ""
            typeArr[one["type"]] = typeArr.get(one["type"], 0) + 1
            typeLevel[one["type"]] = one["level_id"]
            levelCount[one["level_id"]] = levelCount.get(one["level_id"], 0) + 1
            language = (
                IastAgent.objects.filter(pk=one["agent_id"])
                .values_list("language", flat=True)
                .first()
            )
            one["language"] = language if language is not None else ""
            if one["type"] not in vulDetail.keys():
                vulDetail[one["type"]] = []
            detailStr1 = _(
                "We found that there is {1} in the {0} page, attacker can modify the value of {2} to attack:"
            ).format(one["uri"], one["type"], one["taint_position"])

            try:
                one["req_params"] = str(one["req_params"])
            except Exception:
                one["req_params"] = ""
            detailStr2 = (
                one["http_method"]
                + " "
                + one["uri"]
                + "?"
                + one["req_params"]
                + one["http_protocol"]
            )
            try:
                fileData = one["full_stack"][-1].get("stack", "")
                pattern = r".*?\((.*?)\).*?"
                resMatch = re.match(pattern, fileData)
                uriArr = resMatch.group(1).split(":")
                fileName = uriArr[0]
                rowStr = _("{} Line").format(str(uriArr[1])) if len(uriArr) > 1 else ""
            except Exception:
                fileName = ""
                rowStr = ""
            classname = ""
            methodname = ""
            if one["full_stack"]:
                try:
                    full_stack_arr = json.loads(one["full_stack"])
                    full_stack = full_stack_arr[-1]
                    classname = str(full_stack.get("classname", ""))
                    methodname = str(full_stack.get("methodname", ""))
                except Exception:
                    print("======")
            detailStr3 = _("In {} {} call {}. {} (), Incoming parameters {}").format(
                str(fileName), rowStr, classname, methodname, str(one["taint_value"])
            )
            cur_tile = _("{} Appears in {} {}").format(
                one["type"], str(one["uri"]), str(one["taint_position"])
            )
            if one["param_name"]:
                cur_tile = cur_tile + '"' + str(one["param_name"]) + '"'
            vulDetail[one["type"]].append(
                {
                    "title": cur_tile,
                    "type_name": one["type"],
                    "level_id": one["level_id"],
                    "first_time": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(one["first_time"])
                    ),
                    "latest_time": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(one["latest_time"])
                    ),
                    "language": one["language"],
                    "url": one["url"],
                    "detail_data": [detailStr1, detailStr2, detailStr3],
                }
            )
        typeArrKeys = typeArr.keys()
        type_summary.extend(
            {
                "type_name": item_type,
                "type_count": typeArr[item_type],
                "type_level": typeLevel[item_type],
            }
            for item_type in typeArrKeys
        )
    return {
        "type_summary": type_summary,
        "levelCount": levelCount,
        "vulDetail": vulDetail,
    }


def get_hook_type_name(obj):
    #    filter(lambda x: x is not None, [strategy_name, hook_type_name]))
    type_ = list(
        filter(
            lambda x: x is not None,
            [obj.get("strategy__vul_name", None), obj.get("hook_type__name", None)],
        )
    )
    return type_[0] if type_ else ""


def initlanguage():
    program_language_list = IastProgramLanguage.objects.values_list(
        "name", flat=True
    ).all()
    return {program_language.upper(): 0 for program_language in program_language_list}


# todo 默认开源许可证
# def init_license():
#         for license in license_list


def get_agent_languages(agent_items):
    default_language = initlanguage()
    language_agents = {}
    language_items = IastAgent.objects.filter().values("id", "language")
    for language_item in language_items:
        language_agents[language_item["id"]] = language_item["language"]

    for item in agent_items:
        agent_id = item["agent_id"]
        count = item["count"]
        if default_language.get(language_agents[agent_id], None):
            default_language[language_agents[agent_id]] = (
                count + default_language[language_agents[agent_id]]
            )
        else:
            default_language[language_agents[agent_id]] = count
    return [
        {"language": _key, "count": _value} for _key, _value in default_language.items()
    ]
