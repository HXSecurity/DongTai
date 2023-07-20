#!/usr/bin/env python
import logging
import os

import requests
from django.http import FileResponse
from dongtai_common.endpoint import UserEndPoint, R
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from dongtai_common.models.profile import IastProfile
from dongtai_web.utils import get_openapi
from requests.exceptions import ConnectionError

logger = logging.getLogger("dongtai-webapi")


class AgentDownload(UserEndPoint):
    name = "download_iast_agent"
    description = _("Downloading DongTai Agent")

    def __init__(self):
        super().__init__()
        self.common_info = {
            "java": {"extension": "jar", "filename": "agent.jar"},
            "python": {
                "extension": "tar.gz",
                "filename": "dongtai-agent-python.tar.gz",
            },
            "php": {"extension": "tar.gz", "filename": "php-agent.tar.gz"},
            "go": {"extension": ".yaml", "filename": "dongtai-go-agent-config.yaml"},
        }

    def res_by_language(self, language, token, resp):
        temp_filename = f'temp/dongtai-agent-{language}-{token["key"]}.{self.common_info[language]["extension"]}'
        with open(temp_filename, "wb") as f:
            f.write(resp.content)
        with open(temp_filename, "rb") as f:
            response = FileResponse(f)
            response["content_type"] = "application/octet-stream"

            response["Content-Disposition"] = "attachment; filename={}".format(
                self.common_info[language]["filename"]
            )
            os.remove(temp_filename)
            return response

    def get(self, request):
        """
        :param request:
        :return:
        """
        base_url = request.query_params.get("url", "https://www.huoxian.cn")
        language = request.query_params.get("language", "java")
        project_name = request.query_params.get("projectName", "Demo Project")
        token, success = Token.objects.values("key").get_or_create(user=request.user)
        AGENT_SERVER_PROXY = {"HOST": ""}
        AGENT_SERVER_PROXY["HOST"] = get_openapi()
        try:
            resp = requests.get(
                url=f'{AGENT_SERVER_PROXY["HOST"]}/api/v1/agent/download?url={base_url}&language={language}&projectName={project_name}',
                headers={"Authorization": f'Token {token["key"]}'},
            )
        except ConnectionError:
            return R.failure(msg="conncet error,please check config.ini")
        except Exception as e:
            logger.error(e)
            return R.failure(msg="download error,please check deployment")

        return self.res_by_language(language, token, resp)
