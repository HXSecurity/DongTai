import logging
from django.db.models import Prefetch

from dongtai_common.endpoint import UserEndPoint, R
from django.forms.models import model_to_dict
from dongtai_common.utils import const
from dongtai_web.serializers.agent import AgentSerializer
from dongtai_web.utils import get_model_field
from dongtai_common.models.agent import IastAgent
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
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.models.api_route import IastApiRoute, FromWhereChoices
from dongtai_common.models.asset import Asset
from dongtai_common.utils.user import get_auth_users__by_id
import json

logger = logging.getLogger('dongtai-webapi')


class StateType(IntEnum):
    ALL = 1
    RUNNING = 2
    STOP = 3
    UNINSTALL = 4


class AgentListv2(UserEndPoint, ViewSet):
    name = "api-v1-agents"
    description = _("Agent list")

    def pagenation_list(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 20))
            state = StateType(int(request.query_params.get('state', 1)))
            project_name = request.query_params.get('project_name', '')
            project_id = int(request.query_params.get('project_id', 0))
            filter_condiction = generate_filter(state) & Q(
                user__in=get_auth_users__by_id(request.user.id))
            if project_name:
                filter_condiction = filter_condiction & Q(
                    bind_project__name__icontains=project_name)
            if project_id:
                filter_condiction = filter_condiction & Q(
                    bind_project_id=project_id)
            page = page if page else 1
            page_size = page_size if page_size else 20

            summary, queryset = self.get_paginator(query_agent(filter_condiction),
                                                   page, page_size)
            queryset = list(queryset)
            for agent in queryset:
                agent['state'] = cal_state(agent)
                agent['memory_rate'] = get_memory(agent['heartbeat__memory'])
                agent['cpu_rate'] = get_cpu(agent['heartbeat__cpu'])
                agent['disk_rate'] = get_disk(agent['heartbeat__disk'])
            data = {'agents': queryset, "summary": summary}
        except Exception as e:
            logger.error("agents pagenation_list error:{}".format(e))
            data = dict()
        return R.success(data=data)

    def summary(self, request):
        res = {}
        for type_ in StateType:
            res[type_] = IastAgent.objects.filter(
                generate_filter(type_),
                user__in=get_auth_users__by_id(request.user.id)).count()
        return R.success(data=res)

    def agent_stat(self, request):
        try:
            agent_id = int(request.query_params.get('id', 0))
            res = get_agent_stat(agent_id, request.user.id)
        except Exception as e:
            logger.error("agent_stat error:{}".format(e))
            res = dict()
        return R.success(data=res)


def get_agent_stat(agent_id: int, user_id: int) -> dict:
    res = {}
    res['api_count'] = IastApiRoute.objects.filter(
        agent__id=agent_id,
        from_where=FromWhereChoices.FROM_AGENT,
        agent__user__in=get_auth_users__by_id(user_id)).count()
    res['sca_count'] = Asset.objects.filter(
        agent__id=agent_id,
        agent__user__in=get_auth_users__by_id(user_id)).count()
    res['vul_count'] = IastVulnerabilityModel.objects.filter(
        agent__id=agent_id,
        agent__user__in=get_auth_users__by_id(user_id)).count()
    return res


def generate_filter(state: StateType) -> Q:
    if state == StateType.ALL:
        return Q()
    elif state == StateType.RUNNING:
        return Q(online=1) & Q(is_core_running=1)
    elif state == StateType.STOP:
        return Q(online=1) & ~Q(is_core_running=1)
    elif state == StateType.UNINSTALL:
        return Q(online=0)


def get_disk(jsonstr: str) -> str:
    if not jsonstr:
        return ''
    dic = json.loads(jsonstr)
    print(dic)
    try:
        dic = json.loads(jsonstr)
        res = dic['info'][0]['rate']
        res.replace("%", '')
    except Exception as e:
        logger.info(e, exc_info=True)
        return 0
    return res


def get_cpu(jsonstr: str) -> str:
    if not jsonstr:
        return ''
    try:
        dic = json.loads(jsonstr)
        res = dic['rate']
    except Exception as e:
        logger.info(e, exc_info=True)
        return 0
    return res


def get_memory(jsonstr: str) -> str:
    if not jsonstr:
        return ''
    try:
        dic = json.loads(jsonstr)
        res = dic['rate']
    except Exception as e:
        logger.info(e, exc_info=True)
        return 0
    dic = json.loads(jsonstr)
    return res


def cal_state(agent: dict) -> StateType:
    if agent['online'] == 1 and agent['is_core_running'] == 1:
        return StateType.RUNNING
    elif agent['online'] == 1 and agent['is_core_running'] != 1:
        return StateType.STOP
    elif agent['online'] == 0 and agent['is_core_running'] != 1:
        return StateType.UNINSTALL
    return StateType.UNINSTALL


def query_agent(filter_condiction=Q()) -> QuerySet:
    return IastAgent.objects.filter(filter_condiction).values(
        'alias', 'token', 'bind_project__name', 'bind_project__user__username',
        'language', 'server__ip', 'server__port', 'server__path',
        'server__hostname', 'heartbeat__memory', 'heartbeat__cpu',
        'heartbeat__disk', 'register_time', 'is_core_running', 'is_control',
        'online', 'id', 'bind_project__id', 'version').order_by('-latest_time')
