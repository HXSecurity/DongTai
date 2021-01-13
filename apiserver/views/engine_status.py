#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/4 16:47
# software: PyCharm
# project: webapi
import logging

from django.http import JsonResponse
from rest_framework.request import Request

from apiserver.base.openapi import OpenApiEndPoint

logger = logging.getLogger("django")


class EngineUpdateEndPoint(OpenApiEndPoint):
    name = "iast_engine_update_status_edit"
    description = "IAST 检测引擎更新状态修改接口"

    def get(self, request: Request):
        """
        IAST 检测引擎 agent接口
        :param request:
        :return:
        """
        response_dict = {
            "status": '202',
            "msg": "更新状态修改失败"
        }
        status = request.query_params.get('status', None)
        if status:
            if '1' == status:
                # 标记更新状态为已完成
                response_dict['status'] = "201"
                response_dict['msg'] = "更新状态修改成功"

        return JsonResponse(response_dict)
