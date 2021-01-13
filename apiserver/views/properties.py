#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/21 15:56
# software: PyCharm
# project: webapi
import json
import logging

from django.http import JsonResponse
from rest_framework.request import Request

from apiserver.base.openapi import OpenApiEndPoint

logger = logging.getLogger("django")


class PropertiesEndPoint(OpenApiEndPoint):
    """
    当前用户详情
    """
    name = "download_agent_propreties"
    description = "iast agent-下载IAST 配置"

    def get(self, request: Request):
        """
        IAST下载 agent接口
        :param request:
        :return:
        """
        result = {
            "status": '202',
            "msg": "不存在自定义属性",
            "data": []
        }
        return JsonResponse(json.dumps(result))
