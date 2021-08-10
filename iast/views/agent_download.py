#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/3/19 下午2:44
# project: lingzhi-webapi
import logging
import os

import requests
from django.http import FileResponse
from dongtai.endpoint import UserEndPoint, R
from rest_framework.authtoken.models import Token
from dongtai.models.profile import IastProfile

AGENT_SERVER_PROXY = {
    'HOST':
    IastProfile.objects.filter(key='apiserver').values_list('value',
                                                            flat=True).first()
}

logger = logging.getLogger('dongtai-webapi')


class AgentDownload(UserEndPoint):
    """
    当前用户详情
    """
    name = "download_iast_agent"
    description = "下载洞态Agent"

    def __init__(self):
        super().__init__()
        self.common_info = {
            "java": {
                "extension": "jar",
                "filename": "agent.jar"
            },
            "python": {
                "extension": "tar.gz",
                "filename": "dongtai-agent-python.tar.gz"
            }
        }

    def res_by_language(self,language, token, resp):
        temp_filename = f'temp/dongtai-agent-{language}-{token["key"]}.{self.common_info[language]["extension"]}'
        with open(temp_filename, 'wb') as f:
            f.write(resp.content)
        response = FileResponse(open(temp_filename, 'rb'))
        response['content_type'] = 'application/octet-stream'

        response['Content-Disposition'] = "attachment; filename={}".format(self.common_info[language]['filename'])
        os.remove(temp_filename)
        return response

    def get(self, request):
        """
        IAST下载 agent接口s
        :param request:
        :return:
        """
        # try:
        base_url = request.query_params.get('url', 'https://www.huoxian.cn')
        language = request.query_params.get('language', 'java')
        project_name = request.query_params.get('projectName', 'Demo Project')
        token, success = Token.objects.values('key').get_or_create(user=request.user)
        resp = requests.get(
            url=f'{AGENT_SERVER_PROXY["HOST"]}/api/v1/agent/download?url={base_url}&language={language}&projectName={project_name}',
            headers={
                'Authorization': f'Token {token["key"]}'
            })
        # 创建文件
        response = self.res_by_language(language, token, resp)

        return response
        # except Exception as e:
        #     logger.error(e)
        #     return R.failure(data={
        #         "status": '203',
        #         "msg": "agent file not exit."
        #     })
