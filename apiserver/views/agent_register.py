#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject
from dongtai_models.models.project_version import IastProjectVersion
from rest_framework.request import Request

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint
from apiserver.decrypter import parse_data


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
            param = parse_data(request.read())
            token = param.get('name', '')
            version = param.get('version', '')
            project_name = param.get('project', 'Demo Project')
            if not token or not version or not project_name:
                return R.failure(msg="参数错误")

            project_name = project_name.strip()
            # todo 增加其他字段， 版本为空
            exist_agent = IastAgent.objects.filter(token=token, project_name=project_name, user=self.user).exists()
            if exist_agent:
                return R.failure(msg="agent已注册")

            project = IastProject.objects.filter(name=project_name, user=self.user).first()
            project_version_id = 0
            online = 0
            project_id = 0
            if project:
                project_id = project.id
                versionInfo = IastProjectVersion.objects.filter(project_id=project_id, user=self.user, current_version=1, status=1).first()
                if versionInfo:
                    project_version_id = versionInfo.id
                    online = 1
                    # 下线同一台客户端其他版本
                    IastAgent.objects.filter(token=token, online=1, user=self.user).update(online=0)
            IastAgent.objects.create(
                token=token,
                version=version,
                latest_time=int(time.time()),
                user=self.user,
                is_running=1,
                bind_project_id=project_id,
                project_name=project_name,
                control=0,
                is_control=0,
                online=online,
                project_version_id=project_version_id
            )
            return R.success()
        except Exception as e:
            return R.failure(msg="参数错误")
