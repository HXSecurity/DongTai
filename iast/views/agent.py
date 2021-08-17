#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad

# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R

from dongtai.utils import const
from iast.serializers.agent import AgentSerializer
from iast.utils import get_model_field
from dongtai.models.agent import IastAgent
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _


class Agent(UserEndPoint):
    def get(self, request, id_):
        agent = IastAgent.objects.filter(pk=id_).first()
        if agent:
            return R.success(data={'agent':model_to_dict(agent)})
        return R.failure(msg=_("Can't find relevant data"))
