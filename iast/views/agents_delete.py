#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/11 下午6:47
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

logger = logging.getLogger('dongtai-webapi')


class AgentsDeleteEndPoint(UserEndPoint):
    name = "api-v1-agent-<pk>-delete"
    description = "删除agent"

    def get(self, request):
        agent_ids = request.GET.get('ids')
        agent_ids = agent_ids.split(',')
        result = []
        for pk in agent_ids:
            try:
                user = request.user
                queryset = IastAgent.objects.filter(user=user, pk=pk).first()
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
                    result.append(True)
                else:
                    result.append(False)
                    pass
            except Exception as e:
                result.append(False)
                logger.error(f'user_id:{request.user.id} msg:{e}')
        success = list(filter(lambda x: x is True, result))
        failure = list(filter(lambda x: x is False, result))
        if len(success) == len(agent_ids):
            return R.success(msg='删除成功')
        if len(failure) == len(agent_ids):
            return R.success(msg='删除失败')
        return R.success(msg='成功删除{}条，删除失败{}条'.format(len(success), len(failure)))

    def delete_error_log(self):
        try:
            deleted, _rows_count = IastErrorlog.objects.filter(agent=self.agent).delete()
            logger.error(f'错误日志删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'错误日志删除失败，探针ID: {self.agent.id}，原因：{e}')

    def delete_heart_beat(self):
        try:
            deleted, _rows_count = IastHeartbeat.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'心跳数据删除失败，原因：{e}')

    def delete_vul_overpower(self):
        try:
            deleted, _rows_count = IastOverpowerUserAuth.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'越权相关数据删除失败，原因：{e}')

    def delete_vul(self):
        try:
            deleted, _rows_count = IastVulnerabilityModel.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'漏洞数据删除失败，原因：{e}')

    def delete_sca(self):
        try:
            deleted, _rows_count = Asset.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'第三方组件数据删除失败，原因：{e}')

    def delete_method_pool(self):
        try:
            deleted, _rows_count = MethodPool.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'方法池数据删除失败，原因：{e}')

    def delete_method_pool_replay(self):
        try:
            deleted, _rows_count = IastAgentMethodPoolReplay.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求方法池数据删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'重放请求方法池数据删除失败，原因：{e}')

    def delete_replay_queue(self):
        try:
            deleted, _rows_count = IastReplayQueue.objects.filter(agent=self.agent).delete()
            logger.error(f'重放请求队列删除成功，共删除：{deleted}条')
        except Exception as e:
            logger.error(f'重放请求队列删除失败，原因：{e}')


if __name__ == '__main__':
    # 增加method_poll的引入，解决报错
    MethodPool.objects.count()
    IastErrorlog.objects.count()
    IastHeartbeat.objects.count()
    IastOverpowerUserAuth.objects.count()
    Asset.objects.count()
    IastVulnerabilityModel.objects.count()
    MethodPool.objects.count()
