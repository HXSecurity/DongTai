#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午7:17
# software: PyCharm
# project: lingzhi-agent-server
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


class AgentDownload(OpenApiEndPoint):
    """
    当前用户详情
    """
    name = "download_iast_agent"
    description = "下载洞态Agent"
    LOCAL_AGENT_FILE = '/tmp/iast-agent.jar'
    REMOTE_AGENT_FILE = 'agent/java/iast-agent.jar'

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

            if self.download_agent_jar() is False:
                return R.failure(msg="agent file download failure. please contact official staff for help.")

            token, success = Token.objects.get_or_create(user=request.user)
            agent_token = ''.join(str(uuid.uuid4()).split('-'))
            if self.create_config_file(base_url=base_url, agent_token=agent_token,
                                       auth_token=token.key,
                                       project_name=project_name):
                self.replace_jar_config()
                response = FileResponse(open(AgentDownload.LOCAL_AGENT_FILE, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = "attachment; filename=agent.jar"
                return response
            else:
                return R.failure(msg="agent file not exit.")
        except Exception as e:
            logger.error(f'agent下载失败，用户: {request.user.get_username()}，错误详情：{e}')
            return R.failure(msg="agent file not exit.")

    @staticmethod
    def create_config_file(base_url, agent_token, auth_token, project_name):
        try:
            data = "iast.name=lingzhi-Enterprise 1.0.0\niast.version=1.0.0\niast.response.name=lingzhi\niast.response.value=1.0.0\niast.server.url={url}\niast.server.token={token}\niast.allhook.enable=false\niast.dump.class.enable=false\niast.dump.class.path=/tmp/iast-class-dump/\niast.service.heartbeat.interval=30000\niast.service.vulreport.interval=1000\napp.name=LingZhi\nengine.status=start\nengine.name={agent_token}\njdk.version={jdk_level}\nproject.name={project_name}\niast.proxy.enable=false\niast.proxy.host=\niast.proxy.port=\n"
            with open('/tmp/iast.properties', 'w') as config_file:
                config_file.write(
                    data.format(url=base_url, token=auth_token, agent_token=agent_token, jdk_level=1,
                                project_name=project_name))
            return True
        except Exception as e:
            logger.error(f'agent配置文件创建失败，原因：{e}')
            return False

    @staticmethod
    def replace_jar_config():
        # 执行jar -uvf {AgentDownload.LOCAL_AGENT_FILE} iast.properties更新jar包的文件
        import os
        os.system(f'cd /tmp;jar -uvf {AgentDownload.LOCAL_AGENT_FILE} iast.properties')

    @staticmethod
    def download_agent_jar():
        if os.path.exists(AgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(object_name=AgentDownload.REMOTE_AGENT_FILE,
                                               local_file=AgentDownload.LOCAL_AGENT_FILE)
