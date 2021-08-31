#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:Bidaya0
# datetime:2021/7/27 11:36
# software: Vim8
# project: webapi

import time
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.deploy import IastDeployDesc
from dongtai.models.system import IastSystem
from rest_framework.authtoken.models import Token
from iast.utils import get_model_field
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck
from rest_framework.serializers import ValidationError

from rest_framework import serializers



class AgentDeployArgsSerializer(serializers.Serializer):
    middleware = serializers.CharField(required=False)
    language = serializers.CharField(required=False)


class AgentDeploy(UserEndPoint):
    @extend_schema_with_envcheck([AgentDeployArgsSerializer])
    def get(self, request):
        ser = AgentDeployArgsSerializer(data=request.GET)
        try:
            ser.is_valid(True)
        except ValidationError as e:
            return R.failure(data=e.detail)
        desc = IastDeployDesc.objects.filter(**ser.validated_data).first()
        if desc:
            return R.success(data=model_to_dict(desc))
        return R.failure(
            msg=_("Corresponding deployment document could not be found"))
