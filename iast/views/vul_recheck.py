#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import logging

import time
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils.validate import Validate

from base import R
from dongtai.utils import const
from iast.base.user import UserEndPoint

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

            vul.status = const.VUL_WAITING
            vul.latest_time = timestamp
            vul.save(update_fields=['status', 'latest_time'])
        return waiting_count, success_count, re_success_count

    @staticmethod
    def vul_check_for_queryset(vul_queryset):
        no_agent, checked_vuls = 0, list()
        for vul_model in vul_queryset:
            project_id = vul_model.agent.bind_project_id
            if project_id and IastAgent.objects.values("id").filter(bind_project_id=project_id,
                                                                    is_running=const.RUNNING,
                                                                    is_core_running=const.CORE_IS_RUNNING).exists():
                checked_vuls.append(vul_model)
            else:
                no_agent = no_agent + 1
        waiting_count, success_count, re_success_count = VulReCheck.recheck(vul_queryset)
        return no_agent, waiting_count, success_count, re_success_count

    def post(self, request):
        """
        查找项目中存在活跃探针的数量
        :param request:
        :return:
        """
        try:
            vul_ids = request.data.get('ids')
            if vul_ids is None or vul_ids == '':
                return R.failure('ids不能为空')

            vul_ids = vul_ids.split(',')
            if Validate.is_number(vul_ids) is False:
                return R.failure('ids必须为：漏洞ID,漏洞ID 格式')

            auth_agents = self.get_auth_agents_with_user(user=request.user)
            vul_queryset = IastVulnerabilityModel.objects.filter(id__in=vul_ids, agent__in=auth_agents)
            no_agent, waiting_count, success_count, re_success_count = self.vul_check_for_queryset(vul_queryset)

            return R.success(
                data={
                    "no_agent": no_agent,
                    "pending": waiting_count,
                    "recheck": re_success_count,
                    "checking": success_count
                },
                msg=f'处理成功')

        except Exception as e:
            return R.failure(msg=f'漏洞重放出错，错误原因：{e}')

    def vul_check_for_project(self, project_id, auth_users):
        try:
            project_exist = IastProject.objects.values("id").filter(id=project_id, user__in=auth_users).exists()
            if project_exist:
                agent_queryset = IastAgent.objects.values("id").filter(bind_project_id=project_id)
                if agent_queryset:
                    agent_ids = agent_queryset.values()
                    vul_queryset = IastVulnerabilityModel.objects.filter(agent_id__in=agent_ids)
                    waiting_count, success_count, re_success_count = self.recheck(vul_queryset)
                    return True, waiting_count, re_success_count, success_count, None
                else:
                    return False, 0, 0, 0, '当前项目尚未关联探针，无法进行漏洞重放'
            else:
                return False, 0, 0, 0, f'无权访问项目[{project_id}]'
        except Exception as e:
            return False, 0, 0, 0, f'批量重放出错，错误详情：{e}'

    def get(self, request):
        # 处理批量重放，例如，项目名称
        try:
            check_type = request.query_params.get('type')

            if check_type == 'all':
                vul_queryset = IastVulnerabilityModel.objects.filter(
                    agent__in=self.get_auth_agents_with_user(request.user))
                no_agent, pending, recheck, checking = self.vul_check_for_queryset(vul_queryset)

                return R.success(
                    data={
                        "no_agent": no_agent,
                        "pending": pending,
                        "recheck": recheck,
                        "checking": checking
                    },
                    msg=f'处理成功')
            elif check_type == 'project':
                project_id = request.query_params.get('projectId')
                auth_users = self.get_auth_users(request.user)
                if project_id:
                    status, pending, recheck, checking, msg = self.vul_check_for_project(project_id,
                                                                                         auth_users=auth_users)
                    return R.success(
                        data={
                            "no_agent": 0,
                            "pending": pending,
                            "recheck": recheck,
                            "checking": checking
                        },
                        msg=msg)
                return R.failure(msg=f'项目ID不能为空')
            return R.failure(msg="参数格式不正确")

        except Exception as e:
            return R.failure(msg=f'批量重放出错，错误详情：{e}')
