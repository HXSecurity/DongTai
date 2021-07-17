#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午9:56
# software: PyCharm
# project: lingzhi-webapi
import time
from base import R
from iast.base.user import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from iast.base.project_version import get_project_version


class ProjectSummary(UserEndPoint):
    """
    edit by song 项目详情概括
    """
    name = "api-v1-project-summary-<id>"
    description = "查看项目详情-概括"

    @staticmethod
    def weeks_ago(week=1):
        # 最近7天，每天漏洞数量统计
        weekend = 7 * week
        current_timestamp = int(time.time())
        weekend_ago_time = time.localtime(current_timestamp - 86400 * weekend)
        weekend_ago_time_str = str(weekend_ago_time.tm_year) + "-" + str(weekend_ago_time.tm_mon) + "-" + str(
            weekend_ago_time.tm_mday) + " 00:00:00"
        beginArray = time.strptime(weekend_ago_time_str, "%Y-%m-%d %H:%M:%S")
        # 最近第七天0点
        beginT = int(time.mktime(beginArray))
        return current_timestamp, beginT, weekend

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
        # 获取项目当前版本信息
        current_project_version = get_project_version(project.id, auth_users)
        data['versionData'] = current_project_version
        relations = IastAgent.objects.filter(
            user__in=auth_users,
            bind_project_id=project.id,
            online=1,
            project_version_id=current_project_version.get("version_id", 0)
        ).values("id")
        # 通过agent获取漏洞数量，类型
        agent_ids = [relation['id'] for relation in relations]
        queryset = IastVulnerabilityModel.objects.filter(
            agent_id__in=agent_ids,
            status='已确认'
        ).values("type", "level_id", "latest_time")
        typeArr = {}
        typeLevel = {}
        levelCount = {}
        if queryset:
            for one in queryset:
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
        current_timestamp, a_week_ago_timestamp, days = self.weeks_ago(week=1)
        vulInfo = queryset.filter(
            latest_time__gt=a_week_ago_timestamp,
            latest_time__lt=current_timestamp
        ).values("type", "latest_time")

        dayNum = {}
        while days >= 0:
            wDay = time.localtime(current_timestamp - 86400 * days)
            wkey = str(wDay.tm_mon) + "-" + str(wDay.tm_mday)
            dayNum[wkey] = 0
            days = days - 1

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
