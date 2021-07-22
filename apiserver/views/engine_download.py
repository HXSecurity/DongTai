#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:56
# software: PyCharm
# project: webapi

import logging
import os

from django.http import FileResponse
from rest_framework import status
from rest_framework.request import Request

from dongtai.endpoint import OpenApiEndPoint, R
from apiserver.utils import OssDownloader

logger = logging.getLogger("dongtai.openapi")


class EngineDownloadEndPoint(OpenApiEndPoint):
    name = "download_core_jar_package"
    description = "iast agent-下载IAST依赖的core、inject jar包"
    LOCAL_AGENT_FILE = '/tmp/{package_name}.jar'
    REMOTE_AGENT_FILE = 'agent/java/{package_name}.jar'

    def get(self, request: Request):
        """
        IAST下载 agent接口
        :param request:
        :return:
        """
        package_name = request.query_params.get('package_name')
        jdk = request.query_params.get('jdk.version')
        if package_name not in ('iast-core', 'iast-inject', 'dongtai-servlet'):
            return R.failure({
                "status": -1,
                "msg": "bad gay."
            })

        local_file_name = EngineDownloadEndPoint.LOCAL_AGENT_FILE.format(package_name=package_name)
        remote_file_name = EngineDownloadEndPoint.REMOTE_AGENT_FILE.format(package_name=package_name)
        logger.debug(f'download file from oss or local cache, file: {local_file_name}')
        if self.download_agent_jar(remote_agent_file=remote_file_name, local_agent_file=local_file_name):
            try:
                response = FileResponse(open(local_file_name, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = f"attachment; filename={package_name}.jar"
                return response
            except:
                return R.failure(msg="file not exit.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return R.failure(msg="file not exit.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def download_agent_jar(remote_agent_file, local_agent_file):
        if os.path.exists(local_agent_file):
            return True
        else:
            return OssDownloader.download_file(object_name=remote_agent_file,
                                               local_file=local_agent_file)
