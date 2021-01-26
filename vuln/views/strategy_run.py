#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi
import time

from django.http import JsonResponse

from cron.test import demo_print
from lingzhi_engine.base import R, EndPoint
from vuln.models.agent import IastAgent


class StrategyRunEndPoint(EndPoint):
    """
    引擎注册接口
    """
    authentication_classes = []
    permission_classes = []
    name = "api-v1-agent-register"
    description = "引擎注册"

    def get(self, request):
        """
        IAST下载 agent接口s
        :param request:
        :return:
        服务器作为agent的唯一值绑定
        token: agent-ip-port-path
        """
        # 接受 token名称，version，校验token重复性，latest_time = now.time()
        # 生成agent的唯一token
        # 注册
        try:
            demo_print()
            self.user = request.user
            # todo ：
            #  1 分布式锁
            #  2.检查当前用户是否具有安装agent的权限
            #  3.减去一个license
            #  4.启动注册
            #  5.出现异常时，提供回滚功能，恢复license
            token = ''
            version = ''

            if not token or not version:
                return JsonResponse(R.failure(msg="参数错误"))
            have_token = IastAgent.objects.filter(token=token).exists()
            if have_token:
                return JsonResponse(R.failure(msg="agent已注册"))
            IastAgent.objects.create(
                token=token,
                version=version,
                latest_time=int(time.time()),
                user=self.user,
                is_running=1,
                bind_project_id=0,
                control=0,
                is_control=0
            )
            return JsonResponse(R.success())
        except Exception as e:
            return JsonResponse(R.failure(msg="参数错误"))
