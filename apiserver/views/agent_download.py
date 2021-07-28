#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午7:17
# software: PyCharm
# project: lingzhi-agent-server
import json
import os
import uuid, logging

from django.http import FileResponse
from dongtai.endpoint import OpenApiEndPoint, R
from drf_yasg import openapi
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token

from apiserver.utils import OssDownloader

logger = logging.getLogger('dongtai.openapi')


class JavaAgentDownload():
    LOCAL_AGENT_FILE = '/tmp/iast-agent.jar'
    REMOTE_AGENT_FILE = 'agent/java/iast-agent.jar'

    @staticmethod
    def download_agent():
        if os.path.exists(JavaAgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(
                object_name=JavaAgentDownload.REMOTE_AGENT_FILE, local_file=JavaAgentDownload.LOCAL_AGENT_FILE
            )

    @staticmethod
    def create_config(base_url, agent_token, auth_token, project_name):
        try:
            data = "iast.name=DongTai-Enterprise 1.0.0\niast.version=1.0.0\niast.response.name=DongTai Iast\niast.response.value=1.0.0\niast.server.url={url}\niast.server.token={token}\niast.allhook.enable=false\niast.dump.class.enable=false\niast.dump.class.path=/tmp/iast-class-dump/\niast.service.heartbeat.interval=30000\niast.service.vulreport.interval=1000\napp.name=DongTai\nengine.status=start\nengine.name={agent_token}\njdk.version={jdk_level}\nproject.name={project_name}\niast.proxy.enable=false\niast.proxy.host=\niast.proxy.port=\n"
            with open('/tmp/iast.properties', 'w') as config_file:
                config_file.write(
                    data.format(url=base_url, token=auth_token, agent_token=agent_token, jdk_level=1,
                                project_name=project_name)
                )
            return True
        except Exception as e:
            logger.error(f'agent配置文件创建失败，原因：{e}')
            return False

    @staticmethod
    def replace_config():
        # 执行jar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties更新jar包的文件
        import os
        os.system(f'cd /tmp;jar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties')


class PythonAgentDownload():
    LOCAL_AGENT_FILE = '/tmp/dongtai_agent_python.tar.gz'
    REMOTE_AGENT_FILE = 'agent/python/dongtai_agent_python.tar.gz'

    @staticmethod
    def download_agent():
        if os.path.exists(PythonAgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(
                object_name=PythonAgentDownload.REMOTE_AGENT_FILE, local_file=PythonAgentDownload.LOCAL_AGENT_FILE
            )

    @staticmethod
    def create_config(base_url, agent_token, auth_token, project_name):
        raw_config = {
            "debug": False,
            "iast": {
                "proxy": {
                    "port": 80,
                    "host": "",
                    "enable": False
                },
                "server": {
                    "mode": "remote",
                    "token": auth_token,
                    "url": base_url
                },
                "service": {
                    "report": {
                        "interval": 60000
                    },
                    "replay": {
                        "interval": 300000
                    }
                },
                "dump": {
                    "class": {
                        "enable": False,
                        "path": "/tmp/iast-class-dump/"
                    }
                },
                "engine": {
                    "delay": {
                        "time": 10
                    }
                },
                "allhook": {
                    "enable": False
                },
                "name": "lingzhi-Enterprise 1.0.0",
                "mode": "normal"
            },
            "project": {
                "name": project_name
            },
            "engine": {
                "version": "v0.1",
                "name": agent_token
            },
            "app": {
                "name": "DongTai"
            },
            "log": {
                "log_path": "/tmp/dongtai_py_agent_log.txt"
            }
        }
        config_file = open("/tmp/config.json", "w")
        json.dump(raw_config, config_file)

    @staticmethod
    def replace_config():
        # todo 替换config文件
        import tarfile
        agent_file = tarfile.open(PythonAgentDownload.LOCAL_AGENT_FILE, "x:gz")
        os.system(f'cd /tmp;tar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties')


class AgentDownload(OpenApiEndPoint):
    """
    当前用户详情
    """
    name = "download_iast_agent"
    description = "下载洞态Agent"
    DOWNLOAD_HANDLER = {
        'python': PythonAgentDownload(),
        'java': JavaAgentDownload(),
    }

    @swagger_auto_schema(
        operation_description="下载Java探针",
        manual_parameters=(
                openapi.Parameter("url", openapi.IN_QUERY, required=True, description="OpenAPI服务器地址",
                                  type=openapi.TYPE_STRING),
                openapi.Parameter("projectName", openapi.IN_QUERY, required=True, description="项目名称",
                                  type=openapi.TYPE_STRING)
        ),
        responses={200: Response(description='修改成功', examples={'json': {'msg': '修改成功！', "data": []}})},
    )
    def get(self, request):
        try:
            base_url = request.query_params.get('url', 'https://www.huoxian.cn')
            project_name = request.query_params.get('projectName', 'Demo Project')
            language = request.query_params.get('langguage')

            handler = self.DOWNLOAD_HANDLER[language]

            if handler.download_agent() is False:
                return R.failure(msg="agent file download failure. please contact official staff for help.")

            token, success = Token.objects.get_or_create(user=request.user)
            agent_token = ''.join(str(uuid.uuid4()).split('-'))
            if handler.create_config(base_url=base_url, agent_token=agent_token, auth_token=token.key,
                                     project_name=project_name):
                handler.replace_config()
                response = FileResponse(open(handler.LOCAL_AGENT_FILE, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = "attachment; filename=agent.jar"
                return response
            else:
                return R.failure(msg="agent file not exit.")
        except Exception as e:
            logger.error(f'agent下载失败，用户: {request.user.get_username()}，错误详情：{e}')
            return R.failure(msg="agent file not exit.")
