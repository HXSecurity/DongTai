#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/06/09 上午10:52
# software: PyCharm
# project: lingzhi-webapi
import logging, time
from base import R
from iast.base.user import UserEndPoint
from django.db.models import Q
from dongtai.models.project_version import IastProjectVersion
from iast.base.project_version import version_modify
logger = logging.getLogger("django")


class ProjectVersionUpdate(UserEndPoint):
    """
    更新项目版本名称，描述
    """
    name = "api-v1-project-version-update"
    description = "更新项目版本信息"

    def post(self, request):
        try:
            version_id = request.data.get("version_id", 0)
            result = version_modify(request.user, request.data)
            if not version_id or result.get("status", "202") == "202":
                return R.failure(status=202, msg=result.get("msg", "参数错误"))
            else:
                return R.success(msg='更新成功')


            # version = IastProjectVersion.objects.filter(id=version_id, user=request.user, status=1).first()
            # # 增加版本名称检测version_name
            # existVersion = IastProjectVersion.objects.filter(
            #     ~Q(id=version_id),
            #     project_id=project_id,
            #     version_name=version_name,
            #     status=1
            # ).first()
            # if existVersion:
            #     return R.failure(status=202, msg='版本名称重复')
            # if version:
            #     version.version_name = version_name
            #     version.description = description
            #     version.update_time = int(time.time())
            #     version.save(update_fields=['version_name', 'description', 'update_time'])
            #     return R.success(msg='更新成功')
            # else:
            #     return R.failure(status=202, msg='版本不存在')

        except Exception as e:
            return R.failure(status=202, msg=e)
