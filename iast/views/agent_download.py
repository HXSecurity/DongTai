#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/19 下午2:44
# project: lingzhi-webapi
import os

import requests
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from rest_framework.authtoken.models import Token

from iast.base.user import UserEndPoint
from webapi.settings import AGENT_SERVER_PROXY
import logging

logger = logging.getLogger('dongtai-webapi')


class AgentDownload(UserEndPoint):
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
            project_name = request.query_params.get('projectName', 'Demo Project')
            token, success = Token.objects.values('key').get_or_create(user=request.user)
            resp = requests.get(
                url=f'{AGENT_SERVER_PROXY["HOST"]}/api/v1/agent/download?url={base_url}&jdk.version={jdk_version}&projectName={project_name}',
                headers={
                    'Authorization': f'Token {token["key"]}'
                })
            # 创建文件
            temp_filename = f'temp/agent-{token["key"]}.jar'
            with open(temp_filename, 'wb') as f:
                f.write(resp.content)

            response = FileResponse(open(temp_filename, 'rb'))
            response['content_type'] = 'application/octet-stream'
            response['Content-Disposition'] = "attachment; filename=agent.jar"
            os.remove(temp_filename)
            return response
        except Exception as e:
            logger.error(e)
            return JsonResponse({
                "status": '203',
                "msg": "agent file not exit."
            })
