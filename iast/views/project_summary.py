#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午9:56
# software: PyCharm
# project: lingzhi-webapi
import time

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject
from dongtai_models.models.vul_level import IastVulLevel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel


class ProjectSummary(UserEndPoint):
    """
    add by song 项目详情概括
    """
    name = "api-v1-project-summary-<id>"
    description = "查看项目详情-概括"

    def get(self, request, id):
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(user__in=auth_users, id=id).first()

        if not project:
            return R.failure(status=203, msg='no permission')
        data = dict()
        data['owner'] = project.user.get_username()
        data['name'] = project.name
        data['id'] = project.id
        data['mode'] = project.mode
        data['latest_time'] = project.latest_time
        data['type_summary'] = []
        data['day_num'] = []
        data['level_count'] = []
        relations = IastAgent.objects.filter(user__in=auth_users, bind_project_id=project.id).values("id")
        # 通过agent获取漏洞数量，类型
        agent_ids = [relation['id'] for relation in relations]
        typeInfo = IastVulnerabilityModel.objects.filter(
            agent_id__in=agent_ids).values("type", "level_id")
        typeArr = {}
        typeLevel = {}
        levelCount = {}
        if typeInfo:
            for one in typeInfo:
                typeArr[one['type']] = typeArr.get(one['type'], 0) + 1
                typeLevel[one['type']] = one['level_id']
                levelCount[one['level_id']] = levelCount.get(one['level_id'], 0) + 1
            typeArrKeys = typeArr.keys()
            for item_type in typeArrKeys:
                data['type_summary'].append(
                    {
                        'type_name': item_type,
                        'type_count': typeArr[item_type],
                        'type_level': typeLevel[item_type]
                    }
                )
        # 最近7天，每天漏洞数量统计
        weekend = 6
        nowTime = int(time.time())
        beginDay = time.localtime(nowTime - 86400 * weekend)
        beginStr = str(beginDay.tm_year) + "-" + str(beginDay.tm_mon) + "-" + str(beginDay.tm_mday) + " 00:00:00"
        beginArray = time.strptime(beginStr, "%Y-%m-%d %H:%M:%S")
        # 最近第七天0点
        beginT = int(time.mktime(beginArray))
        vulInfo = IastVulnerabilityModel.objects.filter(
            agent_id__in=agent_ids, latest_time__gt=beginT, latest_time__lt=nowTime
        ).values("type", "latest_time")

        dayNum = {}
        while weekend >= 0:
            wDay = time.localtime(nowTime - 86400 * weekend)
            wkey = str(wDay.tm_mon) + "-" + str(wDay.tm_mday)
            dayNum[wkey] = 0
            weekend = weekend - 1

        if vulInfo:
            for vul in vulInfo:
                timeArr = time.localtime(vul['latest_time'])
                timeKey = str(timeArr.tm_mon) + "-" + str(timeArr.tm_mday)
                dayNum[timeKey] = dayNum.get(timeKey, 0) + 1
        levelInfo = IastVulLevel.objects.all()
        levelIdArr = {}
        levelNum = []
        if levelInfo:
            for level_item in levelInfo:
                levelIdArr[level_item.id] = level_item.name_value
                levelNum.append({
                    "level_id": level_item.id,
                    "level_name": level_item.name_value,
                    "num": levelCount.get(level_item.id, 0)
                })
        data['level_count'] = levelNum
        if dayNum:
            for day_label in dayNum.keys():
                data['day_num'].append({
                    'day_label': day_label,
                    'day_num': dayNum[day_label]
                })

        return R.success(data=data)
