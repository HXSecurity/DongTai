#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi
import time

from rest_framework.request import Request

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint
from apiserver.decrypter import parse_data
from apiserver.models.agent import IastAgent
from apiserver.models.project import IastProject


class AgentRegisterEndPoint(OpenApiEndPoint):
    """
    引擎注册接口
    """
    name = "api-v1-agent-register"
    description = "引擎注册"

    def post(self, request: Request):
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
            self.user = request.user
            # todo ：
            #  1 分布式锁
            #  2.检查当前用户是否具有安装agent的权限
            #  3.减去一个license
            #  4.启动注册
            #  5.出现异常时，提供回滚功能，恢复license
            param = parse_data(request.read())
            token = param.get('name', '')
            version = param.get('version', '')
            project_name = param.get('project', 'Demo Project')
            if not token or not version or not project_name:
                return R.failure(msg="参数错误")
            exist_agent = IastAgent.objects.filter(token=token).exists()
            if exist_agent:
                return R.failure(msg="agent已注册")

            project_name = project_name.strip()
            project = IastProject.objects.filter(name=project_name, user=self.user).first()
            IastAgent.objects.create(
                token=token,
                version=version,
                latest_time=int(time.time()),
                user=self.user,
                is_running=1,
                bind_project_id=project.id if project else 0,
                project_name=project_name,
                control=0,
                is_control=0
            )
            return R.success()
        except Exception as e:
            return R.failure(msg="参数错误")
