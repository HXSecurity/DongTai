#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:56
# software: PyCharm
# project: webapi

import logging
import os

from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request

from dongtai.endpoint import OpenApiEndPoint, R

from apiserver.api_schema import DongTaiParameter
from apiserver.utils import OssDownloader

logger = logging.getLogger("dongtai.openapi")

PACKAGE_NAME_LIST = ('iast-core', 'iast-inject', 'dongtai-servlet-api',
                     'dongtai-jakarta-api')


class EngineDownloadEndPoint(OpenApiEndPoint):
    name = "download_core_jar_package"
    description = "iast agent-下载IAST依赖的core、inject jar包"
    LOCAL_AGENT_PATH = '/tmp/iast_cache/package'
    LOCAL_AGENT_FILE = '/tmp/iast_cache/package/{package_name}.jar'
    REMOTE_AGENT_FILE = 'agent/java/{package_name}.jar'

    @extend_schema(
        description='Agent Engine Download',
        parameters=[
            DongTaiParameter.ENGINE_NAME,
        ],
        responses=R,
        methods=['GET']
    )
    def get(self, request: Request):
        package_name = request.query_params.get('engineName')
        try:
            jakarta = int(request.query_params.get('jakarta', 0))
        except:
            jakarta = 0
        if package_name not in ('iast-core', 'iast-inject', 'dongtai-api'):
            return R.failure({
                "status": -1,
                "msg": "bad gay."
            })
        if package_name == 'dongtai-api':
            if jakarta == 0:
                package_name = 'dongtai-servlet-api'
            elif jakarta == 1:
                package_name = 'dongtai-jakarta-api'
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
        if not os.path.exists(EngineDownloadEndPoint.LOCAL_AGENT_PATH):
            os.makedirs(EngineDownloadEndPoint.LOCAL_AGENT_PATH)
        if os.path.exists(local_agent_file):
            return True
        else:
            return OssDownloader.download_file(object_name=remote_agent_file,
                                               local_file=local_agent_file)
