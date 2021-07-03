#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/11 下午6:47
# software: PyCharm
# project: lingzhi-webapi

import logging

from dongtai_models.models.asset import Asset
from dongtai_models.models.errorlog import IastErrorlog
from dongtai_models.models.heartbeat import Heartbeat
from dongtai_models.models.iast_overpower_user import IastOverpowerUserAuth
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from base import R
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.agent_method_pool import MethodPool

logger = logging.getLogger('dongtai-webapi')


class AgentDeleteEndPoint(UserEndPoint):
    name = "api-v1-agent-<pk>-delete"
    description = "删除agent"

    def get(self, request, pk=None):
        try:
            user = request.user
            queryset = IastAgent.objects.filter(user=user, id=pk).first()
            if queryset:
                self.agent = queryset
                # todo 删除agent
                self.delete_error_log()
                self.delete_heart_beat()
                # self.delete_vul_overpower()
                self.delete_sca()
                self.delete_vul()
                self.delete_method_pool()
                self.agent.delete()

                return R.success(msg="agent及相关数据删除成功")
            else:
                return R.failure(msg="agent不存在或无权限访问")
        except Exception as e:
            logger.error(f'user_id:{request.user.id} msg:{e}')
            return R.failure(msg="删除过程出错，请稍后重试")

    def delete_error_log(self):
        try:
            IastErrorlog.objects.filter(agent=self.agent).delete()
        except Exception as e:
            print(e)

    def delete_heart_beat(self):
        try:
            Heartbeat.objects.filter(agent=self.agent).delete()
        except Exception as e:
            logger.error(f'心跳数据删除失败，原因：{e}')

    def delete_vul_overpower(self):
        try:
            IastOverpowerUserAuth.objects.filter(agent=self.agent).delete()
        except Exception as e:
            logger.error(f'越权相关数据删除失败，原因：{e}')

    def delete_vul(self):
        try:
            IastVulnerabilityModel.objects.filter(agent=self.agent).delete()
        except Exception as e:
            logger.error(f'漏洞数据删除失败，原因：{e}')

    def delete_sca(self):
        try:
            Asset.objects.filter(agent=self.agent).delete()
        except Exception as e:
            logger.error(f'第三方组件数据删除失败，原因：{e}')

    def delete_method_pool(self):
        try:
            MethodPool.objects.filter(agent=self.agent).delete()
        except Exception as e:
            logger.error(f'方法池数据删除失败，原因：{e}')


if __name__ == '__main__':
    # 增加method_poll的引入，解决报错
    MethodPool.objects.count()
    IastErrorlog.objects.count()
    Heartbeat.objects.count()
    IastOverpowerUserAuth.objects.count()
    Asset.objects.count()
    IastVulnerabilityModel.objects.count()
    MethodPool.objects.count()
