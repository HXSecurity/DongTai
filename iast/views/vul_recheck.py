#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import logging

import time
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils.validate import Validate
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('dongtai-webapi')


class VulReCheckDataSerializer(serializers.Serializer):
    no_agent = serializers.BooleanField(
        help_text=_('Whether the project does not exist agent'))
    pending = serializers.IntegerField(
        help_text=_('Waiting queue length for replay'))
    recheck = serializers.IntegerField(
        help_text=_('Success queue length for replay'))
    checking = serializers.IntegerField(
        help_text=_('Checking queue length for replay'))


_ResponseGetSerializer = get_response_serializer(
    VulReCheckDataSerializer(),
    status_msg_keypair=(
        ((201, _('Handle success')), ''),
        ((202, _('Item ID should not be empty')), ''),
        ((202, _('Incorrect format parameter')), ''),
        ((202, _('Batch playback error')), ''),
        ((202, _('Current application has not been associated with probes and cannot be reproduced.')), ''),
        ((202, _('No permission to access')), ''),
    ))
_ResponsePostSerializer = get_response_serializer(
    VulReCheckDataSerializer(),
    status_msg_keypair=(
        ((201, _('Handle success')), ''),
        ((202, _('IDS should not be empty')), ''),
        ((202, _('IDS must be: Vulnerability ID, Vulnerability ID Format')), ''),
        ((202, _('Vulnerability replay error')), ''),
    ))


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
                if history_replay_queryset.state in [const.PENDING, const.WAITING]:
                    waiting_count = waiting_count + 1
                    continue
                else:
                    history_replay_queryset.state = const.WAITING
                    history_replay_queryset.count = history_replay_queryset.count + 1
                    history_replay_queryset.update_time = timestamp
                    history_replay_queryset.save(update_fields=['state', 'count', 'update_time', ])
                    re_success_count = re_success_count + 1
            else:
                IastReplayQueue.objects.create(
                    agent=vul.agent,
                    relation_id=vul.id,
                    state=const.WAITING,
                    count=1,
                    create_time=timestamp,
                    update_time=timestamp,
                    replay_type=const.VUL_REPLAY
                )
                success_count = success_count + 1
            vul.status_id = 1
            vul.latest_time = timestamp
            vul.save(update_fields=['status_id', 'latest_time'])
        return waiting_count, success_count, re_success_count

    @staticmethod
    def vul_check_for_queryset(vul_queryset):
        no_agent, checked_vuls = 0, list()
        for vul_model in vul_queryset:
            project_id = vul_model.agent.bind_project_id
            if project_id and IastAgent.objects.values("id").filter(bind_project_id=project_id,
                                                                    online=const.RUNNING,
                                                                    is_core_running=const.CORE_IS_RUNNING).exists():
                checked_vuls.append(vul_model)
            else:
                no_agent = no_agent + 1
        waiting_count, success_count, re_success_count = VulReCheck.recheck(vul_queryset)
        return no_agent, waiting_count, success_count, re_success_count

    @extend_schema_with_envcheck(
        [{
            'name':
            'type',
            'type':
            str,
            'description':
            _('''available options are ("all","project").
                Corresponding to all or specific project respectively.''')
        }, {
            'name':
            "projectId",
            'type':
            int,
            'description':
            _("""The corresponding id of the Project.
            Only If the type is project, the projectId here will be used.""")
        }],
        tags=[_('Vulnerability')],
        summary=_("Vulnerability verification"),
        description=_("""Verify the user's corresponding vulnerabilities.
            Need to specify the type"""),
        response_schema=_ResponsePostSerializer
    )
    def post(self, request):
        """
        :param request:
        :return:
        """
        try:
            vul_ids = request.data.get('ids')
            if vul_ids is None or vul_ids == '':
                return R.failure(_("IDS should not be empty"))

            vul_ids = vul_ids.split(',')
            if Validate.is_number(vul_ids) is False:
                return R.failure(_('IDS must be: Vulnerability ID, Vulnerability ID Format'))

            auth_agents = self.get_auth_agents_with_user(user=request.user)
            vul_queryset = IastVulnerabilityModel.objects.filter(
                id__in=vul_ids, agent__in=auth_agents)
            no_agent, waiting_count, success_count, re_success_count = self.vul_check_for_queryset(
                vul_queryset)

            return R.success(data={
                "no_agent": no_agent,
                "pending": waiting_count,
                "recheck": re_success_count,
                "checking": success_count
            },
                             msg=_('Handle success'))

        except Exception as e:
            logger.error(f' msg:{e}')
            return R.failure(msg=_('Vulnerability replay error'))

    def vul_check_for_project(self, project_id, auth_users):
        try:
            project_exist = IastProject.objects.values("id").filter(
                id=project_id, user__in=auth_users).exists()
            if project_exist:
                agent_queryset = IastAgent.objects.values("id").filter(
                    bind_project_id=project_id)
                if agent_queryset:
                    agent_ids = agent_queryset.values()
                    vul_queryset = IastVulnerabilityModel.objects.filter(
                        agent_id__in=agent_ids)
                    waiting_count, success_count, re_success_count = self.recheck(
                        vul_queryset)
                    return True, waiting_count, re_success_count, success_count, None
                else:
                    return False, 0, 0, 0, _(
                        'Current application has not been associated with probes and cannot be reproduced.'
                    )
            else:
                return False, 0, 0, 0, _('No permission to access')
        except Exception as e:
            logger.error(f' msg:{e}')
            return False, 0, 0, 0, _('Batch playback error')

    @extend_schema_with_envcheck(
        [{
            'name':
            'type',
            'type':
            str,
            'description':
            _('''available options are ("all","project").
                Corresponding to all or specific project respectively.''')
        }, {
            'name':
            "projectId",
            'type':
            int,
            'description':
            _("""The corresponding id of the Project.
            Only If the type is project, the projectId here will be used.""")
        }],
        tags=[_('Vulnerability')],
        summary=_("Vulnerability verification"),
        description=_("""Verify the user's corresponding vulnerabilities.
            Need to specify the type"""),
        response_schema=_ResponsePostSerializer
    )
    def get(self, request):

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
                    msg=_('Handle success'))
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
                        msg=_(msg))
                return R.failure(msg=_("Item ID should not be empty"))
            return R.failure(msg=_("Incorrect format parameter"))

        except Exception as e:
            logger.error(f'user_id:{request.user.id} msg:{e}')
            return R.failure(msg=_('Batch playback error'))
