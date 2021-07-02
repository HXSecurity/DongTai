#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import base64
import logging
import time

from dongtai_models.models.replay_queue import IastReplayQueue
from rest_framework.request import Request

from base import R
from iast import const
from iast.base.user import UserEndPoint
from dongtai_models.models.project import IastProject
from dongtai_models.models.strategy import IastStrategyModel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel
from iast.serializers.vul import VulSerializer

logger = logging.getLogger('dongtai-webapi')


class VulReCheck(UserEndPoint):
    def post(self, request):
        """
        :param request:
        :return:
        """
        try:
            vul_ids = request.data.get('ids')
            vul_ids = vul_ids.split(',')
            auth_agents = self.get_auth_agents_with_user(user=request.user)
            vul_queryset = IastVulnerabilityModel.objects.filter(id__in=vul_ids, agent__in=auth_agents)
            timestamp = int(time.time())
            waiting_count = 0
            success_count = 0
            re_success_count = 0
            for vul in vul_queryset:
                history_replay_queryset = IastReplayQueue.objects.filter(relation_id=vul.id,
                                                                         replay_type=const.VUL_REPLAY).first()
                if history_replay_queryset:
                    if history_replay_queryset.state in [const.PENDING, const.WAITING, const.SOLVING]:
                        waiting_count = waiting_count + 1
                        continue
                    else:
                        history_replay_queryset.state = const.PENDING
                        history_replay_queryset.count = history_replay_queryset.count + 1
                        history_replay_queryset.update_time = timestamp
                        history_replay_queryset.save(update_fields=['state', 'count', 'update_time', ])
                        re_success_count = re_success_count + 1
                else:
                    IastReplayQueue.objects.create(
                        agent=vul.agent,
                        relation_id=vul.id,
                        state=const.PENDING,
                        count=1,
                        create_time=timestamp,
                        update_time=timestamp,
                        uri=vul.uri,
                        method=vul.http_method,
                        scheme=vul.http_scheme,
                        header=vul.req_header,
                        params=vul.req_params,
                        body=vul.req_data,
                        replay_type=const.VUL_REPLAY
                    )
                    success_count = success_count + 1
            return R.success(
                msg=f'{waiting_count}条数据待重放，无需重复验证；{re_success_count}条数据重新下发验证请求；{success_count}条数据已下发验证请求')
        except Exception as e:
            return R.failure(msg=f'漏洞重放出错，错误原因：{e}')
