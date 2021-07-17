#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from base import R
from iast.base.user import UserEndPoint
from dongtai.models.project_version import IastProjectVersion
from iast.base.project_version import version_modify

logger = logging.getLogger("django")


class ProjectVersionAdd(UserEndPoint):
    """
    新增项目版本
    """
    name = "api-v1-project-version-add"
    description = "新增项目版本信息"

    def post(self, request):
        try:
            result = version_modify(request.user, request.data)
            if result.get("status", "202") == "202":
                return R.failure(status=202, msg=result.get("msg", "参数错误"))
            else:
                return R.success(msg='创建成功', data=result.get("data", {}))

            # version = IastProjectVersion.objects.filter(project_id=project_id, version_name=version_name, user=request.user, status=1).first()
            # if version:
            #     return R.failure(status=202, msg='版本名称重复')
            # else:
            #     IastProjectVersion.objects.create(
            #         project_id=project_id,
            #         version_name=version_name,
            #         description=description,
            #         status=1,
            #         user=request.user
            #     )
            #     return R.success(msg='创建成功')
        except Exception as e:
            return R.failure(status=202, msg=e)
