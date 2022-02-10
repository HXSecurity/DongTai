#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from iast.base.project_version import get_project_version, get_project_version_by_id, ProjectsVersionDataSerializer
from django.utils.translation import gettext_lazy as _
from dongtai.models.vulnerablity import IastVulnerabilityStatus
from iast.serializers.project import ProjectSerializer
from dongtai.models.hook_type import HookType
from django.db.models import Q
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai.models.strategy import IastStrategyModel


class ProjectSummaryQuerySerializer(serializers.Serializer):
    version_id = serializers.CharField(
        help_text=_("The version id of the project"))


class ProjectSummaryDataTypeSummarySerializer(serializers.Serializer):
    type_name = serializers.CharField(help_text=_("Name of vulnerability"))
    type_count = serializers.IntegerField(
        help_text=_("Count of thi vulnerablity type"))
    type_level = serializers.IntegerField(
        help_text=_("Level of vulnerability"))


class ProjectSummaryDataDayNumSerializer(serializers.Serializer):
    day_label = serializers.CharField(help_text=_('Timestamp, format %M-%d'))
    day_num = serializers.IntegerField(
        help_text=_('The number of vulnerabilities corresponding to the time'))


class ProjectSummaryDataLevelCountSerializer(serializers.Serializer):
    level_name = serializers.CharField(
        help_text=_('Level name of vulnerability'))
    level_id = serializers.IntegerField(
        help_text=_('Level id of vulnerability'))
    num = serializers.IntegerField(help_text=_(
        'The number of vulnerabilities corresponding to the level'))


class _ProjectSummaryDataSerializer(serializers.Serializer):
    name = serializers.CharField(help_text=_('The name of project'))
    mode = serializers.ChoiceField(['插桩模式'],
                                   help_text=_('The mode of project'))
    id = serializers.IntegerField(help_text=_("The id of the project"))
    latest_time = serializers.IntegerField(help_text=_("The latest update time of the project"))
    versionData = ProjectsVersionDataSerializer(
        help_text=_('Version information about the project'))
    type_summary = ProjectSummaryDataTypeSummarySerializer(
        many=True,
        help_text=_('Statistics on the number of types of vulnerabilities'))
    agent_language = serializers.ListField(
        child=serializers.CharField(),
        help_text=_("Agent language currently included in the project"))
    level_count = ProjectSummaryDataLevelCountSerializer(
        many=True,
        help_text=_(
            "Statistics on the number of danger levels of vulnerabilities"))


_ProjectSummaryResponseSerializer = get_response_serializer(
    _ProjectSummaryDataSerializer())


class ProjectSummary(UserEndPoint):
    name = "api-v1-project-summary-<id>"
    description = _("Item details - Summary")

    @staticmethod
    def weeks_ago(week=1):

        weekend = 7 * week
        current_timestamp = int(time.time())
        weekend_ago_time = time.localtime(current_timestamp - 86400 * weekend)
        weekend_ago_time_str = str(weekend_ago_time.tm_year) + "-" + str(weekend_ago_time.tm_mon) + "-" + str(
            weekend_ago_time.tm_mday) + " 00:00:00"
        beginArray = time.strptime(weekend_ago_time_str, "%Y-%m-%d %H:%M:%S")

        beginT = int(time.mktime(beginArray))
        return current_timestamp, beginT, weekend

    @extend_schema_with_envcheck(
        tags=[_('Project')],
        summary=_('Projects Search'),
        description=
        _("Get the id and name of the item according to the search keyword matching the item name, in descending order of time."
          ),
        response_schema=_ProjectSummaryResponseSerializer,
    )
    def get(self, request, id):
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(user__in=auth_users,
                                             id=id).first()

        if not project:
            return R.failure(status=203, msg=_('no permission'))
        version_id = request.GET.get('version_id', None)
        data = dict()
        data['owner'] = project.user.get_username()
        data['name'] = project.name
        data['id'] = project.id
        data['mode'] = project.mode
        data['latest_time'] = project.latest_time
        data['type_summary'] = []
        data['day_num'] = []
        data['level_count'] = []

        if not version_id:
            current_project_version = get_project_version(
                project.id, auth_users)
        else:
            current_project_version = get_project_version_by_id(version_id)
        data['versionData'] = current_project_version
        relations = IastAgent.objects.filter(
            user__in=auth_users,
            bind_project_id=project.id,
            project_version_id=current_project_version.get("version_id", 0)
        ).values("id")

        agent_ids = [relation['id'] for relation in relations]
        queryset = IastVulnerabilityModel.objects.filter(
            agent_id__in=agent_ids).values("hook_type_id", 'strategy_id', "level_id",
                                "latest_time")
        q = ~Q(hook_type_id=0)
        queryset = queryset.filter(q)
        typeArr = {}
        typeLevel = {}
        levelCount = {}
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
        if queryset:
            for one in queryset:
                hook_type = hooktypes.get(one['hook_type_id'], None)
                hook_type_name = hook_type['name'] if hook_type else None
                strategy = strategys.get(one['strategy_id'], None)
                strategy_name = strategy['vul_name'] if strategy else None
                type_ = list(
                    filter(lambda x: x is not None, [strategy_name, hook_type_name]))
                one['type']= type_[0] if type_ else ''
                typeArr[one['type']] = typeArr.get(one['type'], 0) + 1
                typeLevel[one['type']] = one['level_id']
                levelCount[one['level_id']] = levelCount.get(
                    one['level_id'], 0) + 1
            typeArrKeys = typeArr.keys()
            for item_type in typeArrKeys:
                data['type_summary'].append({
                    'type_name': item_type,
                    'type_count': typeArr[item_type],
                    'type_level': typeLevel[item_type]
                })

        current_timestamp, a_week_ago_timestamp, days = self.weeks_ago(week=1)
        vulInfo = queryset.filter(latest_time__gt=a_week_ago_timestamp,
                                  latest_time__lt=current_timestamp).values(
                                      "hook_type_id", "latest_time")

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
        data['agent_language'] = ProjectSerializer(
            project).data['agent_language']
        return R.success(data=data)
