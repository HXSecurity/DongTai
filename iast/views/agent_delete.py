#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi

import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.asset import Asset
from dongtai.models.errorlog import IastErrorlog
from dongtai.models.heartbeat import IastHeartbeat
from dongtai.models.iast_overpower_user import IastOverpowerUserAuth
from dongtai.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai.models.replay_queue import IastReplayQueue
from dongtai.models.vulnerablity import IastVulnerabilityModel

from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger('dongtai-webapi')


class AgentDeleteEndPoint(UserEndPoint):
    name = "api-v1-agent-<pk>-delete"
    description = _("Delete Agent")

    def get(self, request, pk=None):
        try:
            user = request.user
            queryset = IastAgent.objects.filter(user=user, id=pk).first()
            if queryset:
                self.agent = queryset
                self.delete_error_log()
                self.delete_heart_beat()
                # self.delete_vul_overpower()
                self.delete_sca()
                self.delete_vul()
                self.delete_method_pool()
                self.delete_method_pool_replay()
                self.delete_replay_queue()
                self.agent.delete()

                return R.success(msg=_("Agent and related data deletion success"))
            else:
                return R.failure(msg=_("Agent does not exist or have no right to access"))
        except Exception as e:
            logger.error('user_id:{request.user.id} msg:{e}')
            return R.failure(msg=_("Delete the process error, please try again later"))

    def delete_error_log(self):
        try:
            deleted, _rows_count = IastErrorlog.objects.filter(agent=self.agent).delete()
            logger.error(_('Error log deletion success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Error log deletion failed, probe ID: {}, reason: {}').format(self.agent.id,e))

    def delete_heart_beat(self):
        try:
            deleted, _rows_count = IastHeartbeat.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Heartbeat data deletion failed, reasons: {}').format(e))

    def delete_vul_overpower(self):
        try:
            deleted, _rows_count = IastOverpowerUserAuth.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Bypass Related Data Deletion Failure, Reason: {}').format(e))

    def delete_vul(self):
        try:
            deleted, _rows_count = IastVulnerabilityModel.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Vulnerability data deletion failed, reason: {}'.format(e)))

    def delete_sca(self):
        try:
            deleted, _rows_count = Asset.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Third-party component data deletion failed, reasons: {}').format(e))

    def delete_method_pool(self):
        try:
            deleted, _rows_count = MethodPool.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Method pool data deletion failed, reasons: {}').format(e))

    def delete_method_pool_replay(self):
        try:
            deleted, _rows_count = IastAgentMethodPoolReplay.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request method pool data delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Replay request method pool data deletion failed, reasons: {}'.format(e)))

    def delete_replay_queue(self):
        try:
            deleted, _rows_count = IastReplayQueue.objects.filter(agent=self.agent).delete()
            logger.error(_('Replay request queue delete success, copied: {}').format(deleted))
        except Exception as e:
            logger.error(_('Replay request queue delete failed, reason: {}').format(e))


if __name__ == '__main__':
    
    MethodPool.objects.count()
    IastErrorlog.objects.count()
    IastHeartbeat.objects.count()
    IastOverpowerUserAuth.objects.count()
    Asset.objects.count()
    IastVulnerabilityModel.objects.count()
    MethodPool.objects.count()
