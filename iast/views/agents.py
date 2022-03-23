#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging
from django.db.models import Prefetch

from dongtai.endpoint import UserEndPoint, R
from django.forms.models import model_to_dict
from dongtai.utils import const
from iast.serializers.agent import AgentSerializer
from iast.utils import get_model_field
from dongtai.models.agent import IastAgent
from collections import defaultdict
from functools import reduce
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger('dongtai-webapi')

_ResponseSerializer = get_response_serializer(
    data_serializer=AgentSerializer(many=True), )


class AgentList(UserEndPoint):
    name = "api-v1-agents"
    description = _("Agent list")
    SERVER_MAP = dict()
    @extend_schema_with_envcheck(
        [
            {
                'name': "page",
                'type': int,
                'default': 1,
                'required': False,
            },
            {
                'name': "pageSize",
                'type': int,
                'default': 1,
                'required': False,
            },
            {
                'name': "state",
                'type': int,
                'default': 1,
                'required': False,
            },
            {
                'name': "token",
                'type': str,
                'required': False,
            },
            {
                'name': "project_name",
                'type': str,
                'required': False,
            },
        ],
        tags=[_('Agent')],
        summary=_('Agent List'),
        description=_(
            "Get a list containing Agent information according to conditions."
        ),
        response_schema=_ResponseSerializer,
    )
    def get_running_status(self, obj):
        mapping = defaultdict(str)
        mapping.update({1: _("Online"), 0: _("Offline")})
        return mapping[obj.online]

    def get_server(self, obj):
        def get_server_addr():
            if obj.server_id not in self.SERVER_MAP:
                if obj.server.ip and obj.server.port and obj.server.port != 0:
                    self.SERVER_MAP[
                        obj.server_id] = f'{obj.server.ip}:{obj.server.port}'
                else:
                    return _('No flow is detected by the probe')
            return self.SERVER_MAP[obj.server_id]

        if obj.server_id:
            return get_server_addr()
        return _('No flow is detected by the probe')

    def get(self, request):
        try:
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('pageSize', 20))
            running_state = int(request.query_params.get('state', const.RUNNING))

            fields = get_model_field(
                IastAgent,
                include=['token', 'project_name'],
            )
            searchfields = dict(
                filter(lambda k: k[0] in fields, request.query_params.items()))
            searchfields_ = {k: v for k, v in searchfields.items() if k in fields}
            q = reduce(
                lambda x, y: x | y,
                map(
                    lambda x: Q(**x),
                    map(
                        lambda kv_pair:
                        {'__'.join([kv_pair[0], 'icontains']): kv_pair[1]},
                        searchfields_.items())), Q())
            q = q & Q(online=running_state)
            if request.user.is_anonymous:
                q = q & Q(user_id=request.user.id)
            if request.user.is_system_admin() != 1:
                q = q & Q(user__in=self.get_auth_users(request.user))

            total = IastAgent.objects.filter(q).count()
            if page > 1:
                before_id = page * page_size
                q = q & Q(id__gt=before_id)

            queryset = IastAgent.objects.filter(q).order_by('-latest_time').select_related("server","user").prefetch_related(
                "heartbeats"
            )[:page_size]
            end = []
            for item in queryset:
                one = model_to_dict(item)
                server_data = model_to_dict(item.server)
                one['cluster_name'] = server_data.get("cluster_name", "")
                one['cluster_version'] = server_data.get("cluster_version", "")
                one['owner'] = item.user.username
                one['server'] = self.get_server(item)
                if not one.get("alias", ""):
                    one['alias'] = one['token']
                all = item.heartbeats.all()
                if all:
                    one['report_queue'] = all[0].report_queue
                    one['method_queue'] = all[0].method_queue
                    one['replay_queue'] = all[0].replay_queue
                    one['system_load'] = all[0].cpu
                    one['flow'] = all[0].req_count
                    one['latest_time'] = all[0].dt
                else:
                    one['report_queue'] = 0
                    one['method_queue'] = 0
                    one['replay_queue'] = 0
                    one['system_load'] = _("Load data is not uploaded")
                    one['flow'] = 0
                del one['online']
                one['running_status'] = self.get_running_status(item)
                end.append(one)

            # summery, queryset = self.get_paginator(queryset, page=page, page_size=page_size)
            # data = AgentSerializer(queryset, many=True).data
            # if not request.user.is_talent_admin():
            #     data = list(map(lambda x:removestartup(x),data))
            page_info = {
                "alltotal": total,
                "num_pages": page,
                "page_size": page_size
            }
            return R.success(
                msg="success",
                data=end,
                page=page_info
            )
        except ValueError as e:
            logger.error(e)
            return R.failure(msg=_('Incorrect format parameter, please check again'))
        except Exception as e:
            logger.error(e)
            return R.failure(msg=_('Program error'))


def removestartup(dic):
    del dic['startup_time']
    return dic
