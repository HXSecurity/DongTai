#!/usr/bin/env python
# datetime:2020/6/3 11:36

import time

from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.deploy import IastDeployDesc
from dongtai_common.models.system import IastSystem


class AgentDeploySave(UserEndPoint):
    name = "api-v1-iast-deploy-submit"
    description = _("Uploading Agent configuration")

    def get(self, request):
        end = {
            "status": 201,
            "msg": "success",
            "user_token": "",
            "desc": "",
            "data": {},
        }
        systemInfo = IastSystem.objects.filter(id__gt=0).order_by("-id").first()
        if not systemInfo:
            step = 1
        else:
            token, success = Token.objects.get_or_create(user=request.user)
            end["user_token"] = token.key
            if systemInfo.system:
                step = 3
                desInfo = IastDeployDesc.objects.filter(
                    middleware=systemInfo.middleware, os=systemInfo.system
                ).first()
                if desInfo:
                    end["desc"] = desInfo.desc
            else:
                step = 2
            end["data"] = {
                "agent_value": systemInfo.agent_value,
                "java_version": systemInfo.java_version,
                "middleware": systemInfo.middleware,
                "system": systemInfo.system,
            }
        end["step"] = step
        return R.success(
            step=step, data=end["data"], user_token=end["user_token"], desc=end["desc"]
        )

    def post(self, request):
        user = request.user
        token, success = Token.objects.get_or_create(user=user)
        agent_value = request.data.get("agent_value", 0)
        java_version = request.data.get("java_version", 0)
        middleware = request.data.get("middleware", 0)
        system = request.data.get("system", 0)
        result = {"user_token": "", "status": 201, "msg": "success", "desc": ""}
        systemInfo = IastSystem.objects.filter(id__gt=0).order_by("-id").first()
        if not systemInfo:
            systemInfo = IastSystem.objects.create()
        if agent_value:
            systemInfo.deploy_status = 1
            systemInfo.agent_value = agent_value
        if java_version:
            systemInfo.java_version = java_version
        if middleware:
            systemInfo.middleware = middleware
        if system:
            systemInfo.system = system
            systemInfo.deploy_status = 2
            result["user_token"] = token.key
            desInfo = IastDeployDesc.objects.filter(
                middleware=systemInfo.middleware, os=systemInfo.system
            ).first()
            if desInfo:
                result["desc"] = desInfo.desc
        systemInfo.user = user
        systemInfo.update_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        systemInfo.save()
        return R.success(user_token=result["user_token"], desc=result["desc"])
