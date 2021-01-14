#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:56
# software: PyCharm
# project: webapi

import logging

from django.http import FileResponse, JsonResponse
from rest_framework import status
from rest_framework.request import Request

from AgentServer.base import R
from apiserver.base.openapi import OpenApiEndPoint

logger = logging.getLogger("django")


class EngineDownloadEndPoint(OpenApiEndPoint):
    name = "download_core_jar_package"
    description = "iast agent-下载IAST依赖的core、inject jar包"

    def get(self, request: Request):
        """
        IAST下载 agent接口
        :param request:
        :return:
        """
        package_name = request.query_params.get('package_name')
        if package_name in ['iast-core', 'iast-inject']:
            logger.debug(f'即将下载{package_name}文件')
            filename = f"iast/upload/iast-package/{package_name}.jar"
            try:
                response = FileResponse(open(filename, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = f"attachment; filename={package_name}.jar"
                return response
            except:
                return JsonResponse(R.failure(msg="file not exit."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse(R.failure(msg="file not exit."), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
