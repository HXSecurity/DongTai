#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import base64
import logging
import time
from dongtai_models.models.agent import IastAgent

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
    @staticmethod
    def recheck(vul_queryset):
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
                    replay_type=const.VUL_REPLAY
                )
                success_count = success_count + 1
        return waiting_count, success_count, re_success_count

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
            waiting_count, success_count, re_success_count = self.recheck(vul_queryset)
            return R.success(
                msg=f'{waiting_count}条数据待重放，无需重复验证；{re_success_count}条数据重新下发验证请求；{success_count}条数据已下发验证请求')
        except Exception as e:
            return R.failure(msg=f'漏洞重放出错，错误原因：{e}')

    def get(self, request):
        # 处理批量重放，例如，项目名称
        try:
            project_id = request.query_params.get('projectId')
            project_exist = IastProject.objects.values("id").filter(id=project_id,
                                                                    user__in=self.get_auth_users(request.user)).exists()
            if project_exist:
                agent_queryset = IastAgent.objects.values("id").filter(bind_project_id=project_id).first()
                if agent_queryset:
                    agent_ids = agent_queryset.values()
                    vul_queryset = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids)
                    waiting_count, success_count, re_success_count = self.recheck(vul_queryset)
                    return R.success(
                        msg=f'{waiting_count}条数据待重放，无需重复验证；{re_success_count}条数据重新下发验证请求；{success_count}条数据已下发验证请求')
                else:
                    return R.failure(msg='当前项目尚未发现漏洞，无法重放')
            else:
                return R.failure(msg=f'无权访问项目[{project_id}]')
        except Exception as e:
            return R.failure(msg=f'批量重放出错，错误详情：{e}')
