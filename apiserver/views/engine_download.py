#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:56
# software: PyCharm
# project: webapi

import logging

from django.http import FileResponse
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
        jdk = request.query_params.get('jdk.version')
        if package_name not in ('iast-core', 'iast-inject') or jdk not in ('1', '2'):
            return R.failure({
                "status": -1,
                "msg": "bad gay."
            })
        logger.debug(f'即将下载{package_name}文件')
        if package_name in ('iast-core',) and jdk == '2':
            filename = f"iast-package/jdk-high/{package_name}.jar"
        else:
            filename = f"iast-package/{package_name}.jar"
        try:
            response = FileResponse(open(filename, "rb"))
            response['content_type'] = 'application/octet-stream'
            response['Content-Disposition'] = f"attachment; filename={package_name}.jar"
            return response
        except:
            return R.failure(msg="file not exit.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
