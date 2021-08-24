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


_fields = get_model_field(IastDeployDesc, include=['middleware', 'language'])

class AgentDeploy(UserEndPoint):
    @extend_schema_with_envcheck([{
        'name': field,
        'type': str
    } for field in _fields], [])
    def get(self, request):
        fields = get_model_field(IastDeployDesc,
                                 include=['middleware', 'language'])
        filters = {k: v for k, v in request.GET.items() if k in fields}
        desc = IastDeployDesc.objects.filter(**filters).first()
        if desc:
            return R.success(data= model_to_dict(desc))
        return R.failure(msg=_("Corresponding deployment document could not be found"))
