#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:23
# software: PyCharm
# project: lingzhi-webapi
import logging

from dongtai.endpoint import UserEndPoint, R

from dongtai.utils import const
from iast.serializers.agent import AgentSerializer
from iast.utils import get_model_field
from dongtai.models.agent import IastAgent
from django.forms.models import model_to_dict


class Agent(UserEndPoint):
    def get(self, request, id_): 
        agent = IastAgent.objects.filter(pk=id_).first()
        if agent:
            return R.success(data={'agent':model_to_dict(agent)})
        return R.failure(msg='找不到相关数据')
