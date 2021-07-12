#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi
import time

from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
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
            user = request.user
            param = parse_data(request.read())
            token = param.get('name', '')
            version = param.get('version', '')
            project_name = param.get('project', 'Demo Project').strip()
            if not token or not version or not project_name:
                return R.failure(msg="参数错误")

            project = self.get_project(project_name, user)
            if project:
                project_current_version = self.get_project_current_version(project['id'])
                if self.is_exist_agent(token, project_name, user, project_current_version['id']):
                    return R.failure(msg="agent已注册")
                else:
                    # 注册项目
                    self.register_agent(True, token, user, version, project['id'], project_name,
                                        project_current_version['id'])
            else:
                if self.is_exist_agent(token, project_name, user, 0):
                    return R.failure(msg="agent已注册")
                else:
                    self.register_agent(False, token, user, version, 0, project_name, 0)

            return R.success()
        except Exception as e:
            return R.failure(msg="参数错误")

    @staticmethod
    def get_project(project_name, user):
        return IastProject.objects.values("id").filter(name=project_name, user=user).first()

    @staticmethod
    def get_project_current_version(project_id):
        return IastProjectVersion.objects.filter(project_id=project_id, current_version=1, status=1).values(
            "id").first()

    @staticmethod
    def is_exist_agent(token, project_name, user, current_project_version_id):
        return IastAgent.objects.values("id").filter(token=token, project_name=project_name, user=user,
                                                     project_version_id=current_project_version_id).exists()

    @staticmethod
    def register_agent(exist_project, token, user, version, project_id, project_name, project_version_id):
        if exist_project:
            IastAgent.objects.filter(token=token, online=1, user=user).update(online=0)

        IastAgent.objects.create(
            token=token,
            version=version,
            latest_time=int(time.time()),
            user=user,
            is_running=1,
            bind_project_id=project_id,
            project_name=project_name,
            control=0,
            is_control=0,
            online=1,
            project_version_id=project_version_id
        )
