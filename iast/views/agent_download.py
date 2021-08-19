#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: lingzhi-webapi
import logging
import os

import requests
from django.http import FileResponse
from dongtai.endpoint import UserEndPoint, R
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from dongtai.models.profile import IastProfile



logger = logging.getLogger('dongtai-webapi')


class AgentDownload(UserEndPoint):
    name = "download_iast_agent"
    description = _("Downloading DongTai Agent")

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
        :param request:
        :return:
        """
        base_url = request.query_params.get('url', 'https://www.huoxian.cn')
        language = request.query_params.get('language', 'java')
        project_name = request.query_params.get('projectName', 'Demo Project')
        token, success = Token.objects.values('key').get_or_create(user=request.user)
        AGENT_SERVER_PROXY={'HOST':''}
        APISERVER = IastProfile.objects.filter(key='apiserver').values_list('value',
                                                            flat=True).first()       
        AGENT_SERVER_PROXY['HOST'] = APISERVER if APISERVER is not None else ''
        resp = requests.get(
            url=f'{AGENT_SERVER_PROXY["HOST"]}/api/v1/agent/download?url={base_url}&language={language}&projectName={project_name}',
            headers={
                'Authorization': f'Token {token["key"]}'
            })
        
        response = self.res_by_language(language, token, resp)

        return response
