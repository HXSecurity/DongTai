#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午7:17
# software: PyCharm
# project: lingzhi-agent-server
import uuid

from django.http import FileResponse, JsonResponse
from rest_framework.authtoken.models import Token

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint


class AgentDownload(OpenApiEndPoint):
    """
    当前用户详情
    """
    name = "download_iast_agent"
    description = "下载洞态Agent"

    def get(self, request):
        """
        IAST下载 agent接口s
        :param request:
        :return:
        """
        try:
            base_url = request.query_params.get('url', 'https://www.huoxian.cn')
            jdk_version = request.query_params.get('jdk.version', 'https://www.huoxian.cn')
            if jdk_version in ["Java 9", "Java 10", "Java 11", "Java 13"]:
                jdk_level = 2
            else:
                jdk_level = 1
            token, success = Token.objects.get_or_create(user=request.user)
            agent_token = ''.join(str(uuid.uuid4()).split('-'))
            if self.create_config_file(base_url, jdk_level, agent_token, token.key):
                self.replace_jar_config()
                filename = f"iast-package/iast-agent.jar"
                response = FileResponse(open(filename, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = "attachment; filename=agent.jar"
                return response
            else:
                return R.failure(msg="agent file not exit.")
        except:
            return R.failure(msg="agent file not exit.")

    @staticmethod
    def create_config_file(base_url, jdk_level, agent_token, auth_token):
        try:
            data = "iast.name=lingzhi-Enterprise 1.0.0\niast.version=1.0.0\niast.response.name=lingzhi\niast.response.value=1.0.0\niast.server.url={url}\niast.server.token={token}\niast.allhook.enable=false\niast.dump.class.enable=false\niast.dump.class.path=/tmp/iast-class-dump/\niast.service.heartbeat.interval=30000\niast.service.vulreport.interval=1000\napp.name=LingZhi\nengine.status=start\nengine.name={agent_token}\njdk.version={jdk_level}"
            with open('/tmp/iast.properties', 'w') as config_file:
                config_file.write(
                    data.format(url=base_url, token=auth_token, agent_token=agent_token, jdk_level=jdk_level))
            return True
        except Exception as e:
            return False

    @staticmethod
    def replace_jar_config():
        # 执行jar -uvf iast/upload/iast-package/iast-agent.jar /tmp/iast.properties更新jar包的文件
        import os
        os.system('cd /tmp;jar -uvf /opt/iast/apiserver/iast-package/iast-agent.jar iast.properties')
