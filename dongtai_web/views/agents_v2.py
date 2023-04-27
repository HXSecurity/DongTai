import logging
from django.db.models import Prefetch

from dongtai_common.endpoint import UserEndPoint, R
from django.forms.models import model_to_dict

from dongtai_common.models.department import Department
from dongtai_common.utils import const
from dongtai_web.serializers.agent import AgentSerializer
from dongtai_web.utils import get_model_field
from dongtai_common.models.agent import IastAgent, IastAgentEvent
from collections import defaultdict
from functools import reduce
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.base.paginator import ListPageMaker
from django.core.cache import cache
from enum import IntEnum
from django.db.models.query import QuerySet
from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.api_route import IastApiRoute, FromWhereChoices
from dongtai_common.models.asset import Asset
from dongtai_common.utils.user import get_auth_users__by_id
import json
from typing import Optional
from time import time
from itertools import groupby

logger = logging.getLogger('dongtai-webapi')


class StateType(IntEnum):
    ALL = 1
    RUNNING = 2
    STOP = 3
    UNINSTALL = 4
    ONLINE = 5
    ALLOW_REPORT = 6


class AgentListv2ArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    state = serializers.ChoiceField(choices=StateType)
    last_days = serializers.IntegerField(default=None,
                                         required=False,
                                         help_text=_('Last days'))
    project_id = serializers.IntegerField(default=None,
                                          required=False,
                                          help_text=_('project_id'))
    project_name = serializers.CharField(default=None,
                                         help_text=_("project_name"))


class AgentListv2(UserEndPoint, ViewSet):
    name = "api-v1-agents"
    description = _("Agent list")

    @extend_schema_with_envcheck(
        [AgentListv2ArgsSerializer],
        tags=[_('Agent')],
        summary=_('Agent List v2'),
    )
    def pagenation_list(self, request):
        ser = AgentListv2ArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        department = request.user.get_relative_department()
        filter_condiction = generate_filter(
            ser.validated_data['state']) & Q(department__in=department)
        if ser.validated_data['project_name']:
            filter_condiction = filter_condiction & Q(
                bind_project__name__icontains=ser.
                validated_data['project_name'])
        if ser.validated_data['project_id'] is not None:
            filter_condiction = filter_condiction & Q(
                bind_project_id=ser.validated_data['project_id'])
        if ser.validated_data['last_days'] is not None:
            filter_condiction = filter_condiction & Q(
                heartbeat__dt__gte=int(time()) -
                60 * 60 * 24 * ser.validated_data['last_days'])

        summary, queryset = self.get_paginator(query_agent(filter_condiction),
                                               ser.validated_data['page'],
                                               ser.validated_data['page_size'])
        queryset = list(queryset)
        agent_dict = {}
        for agent in queryset:
            agent['state'] = cal_state(agent)
            agent['memory_rate'] = get_memory(agent['heartbeat__memory'])
            agent['cpu_rate'] = get_cpu(agent['heartbeat__cpu'])
            agent['disk_rate'] = get_disk(agent['heartbeat__disk'])
            agent['is_control'] = get_is_control(
                agent['actual_running_status'],
                agent['except_running_status'],
                agent['online'],
            )
            agent['ipaddresses'] = get_service_addrs(
                json.loads(agent['server__ipaddresslist']),
                agent['server__port'])
            if not agent['events']:
                agent['events'] = ['注册成功']
            agent_dict[agent['id']] = {}
        agent_events = IastAgentEvent.objects.filter(
            agent__id__in=agent_dict.keys()).values().all()
        agent_events_dict = {
            k: list(g)
            for k, g in groupby(agent_events, key=lambda x: x['agent_id'])
        }
        for agent in queryset:
            agent['new_events'] = agent_events_dict[
                agent['id']] if agent['id'] in agent_events_dict else {}
        data = {'agents': queryset, "summary": summary}
        return R.success(data=data)

    def summary(self, request):
        res = {}
        department = request.user.get_relative_department()
        last_days = int(request.query_params.get('last_days', 0))
        for type_ in StateType:
            filter_condiction = generate_filter(type_)
            if last_days:
                filter_condiction = filter_condiction & Q(
                    heartbeat__dt__gte=int(time()) - 60 * 60 * 24 * last_days)
            res[type_] = IastAgent.objects.filter(
                filter_condiction,
                department__in=department,
            ).count()
            # user__in=get_auth_users__by_id(request.user.id)).count()

        return R.success(data=res)

    def agent_stat(self, request):
        department = request.user.get_relative_department()
        try:
            agent_id = int(request.query_params.get('id', 0))
            res = get_agent_stat(agent_id, department)
        except Exception as e:
            logger.error("agent_stat error:{}".format(e))
            res = dict()
        return R.success(data=res)


def get_service_addrs(ip_list: list, port: int) -> list:
    if not port:
        return ip_list
    return list(map(lambda x: x + ":" + str(port), ip_list))


def get_agent_stat(agent_id: int, department: Department) -> dict:
    res = {}
    res['api_count'] = IastApiRoute.objects.filter(
        agent__id=agent_id,
        from_where=FromWhereChoices.FROM_AGENT,
        project__department__in=department).count()
    # agent__user__in = get_auth_users__by_id(user_id)).count()
    res['sca_count'] = Asset.objects.filter(
        agent__id=agent_id,
        project__department__in=department).count()
    res['vul_count'] = IastVulnerabilityModel.objects.filter(
        agent__id=agent_id,
        project__department__in=department).count()
    return res


def generate_filter(state: StateType) -> Q:
    if state == StateType.ALL:
        return Q()
    elif state == StateType.RUNNING:
        return Q(online=1) & Q(actual_running_status=1)
    elif state == StateType.STOP:
        return Q(online=1) & ~Q(actual_running_status=1)
    elif state == StateType.UNINSTALL:
        return Q(online=0)
    elif state == StateType.ONLINE:
        return Q(online=1)
    elif state == StateType.ALLOW_REPORT:
        return Q(allow_report=1)
    return Q()


def get_is_control(actual_running_status: int, except_running_status: int,
                   online: int) -> int:
    if online and actual_running_status != except_running_status:
        return 1
    return 0


def get_disk(jsonstr: Optional[str]) -> str:
    if not jsonstr:
        return ''
    dic = json.loads(jsonstr)
    try:
        dic = json.loads(jsonstr)
        res = str(dic['info'][0]['rate'])
        res.replace("%", '')
    except Exception as e:
        logger.debug(e, exc_info=True)
        return '0'
    return res


def get_cpu(jsonstr: Optional[str]) -> str:
    if not jsonstr:
        return ''
    try:
        dic = json.loads(jsonstr)
        res = str(dic['rate'])
    except Exception as e:
        logger.debug(e, exc_info=True)
        return '0'
    return res


def get_memory(jsonstr: Optional[str]) -> str:
    if not jsonstr:
        return ''
    try:
        dic = json.loads(jsonstr)
        res = str(dic['rate'])
    except Exception as e:
        logger.debug(e, exc_info=True)
        return '0'
    dic = json.loads(jsonstr)
    return res


def cal_state(agent: dict) -> StateType:
    if agent['online'] == 1 and agent['actual_running_status'] == 1:
        return StateType.RUNNING
    elif agent['online'] == 1 and not agent['actual_running_status'] == 1:
        return StateType.STOP
    # elif agent['online'] == 0:
    #    return StateType.UNINSTALL
    return StateType.UNINSTALL


def query_agent(filter_condiction=Q()) -> QuerySet:
    return IastAgent.objects.filter(filter_condiction).values(
        'alias', 'token', 'bind_project__name', 'bind_project__user__username',
        'language', 'server__ip', 'server__port', 'server__path',
        'server__ipaddresslist', 'events', 'server__hostname',
        'heartbeat__memory', 'heartbeat__cpu', 'heartbeat__disk',
        'register_time', 'is_core_running', 'is_control', 'online', 'id',
        'bind_project__id', 'version', 'except_running_status',
        'actual_running_status', 'state_status',
        'allow_report').order_by('-latest_time')
