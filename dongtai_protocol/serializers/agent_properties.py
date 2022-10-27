#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午2:59
# software: PyCharm
# project: lingzhi-agent-server
from dongtai_common.models.agent_properties import IastAgentProperties
from rest_framework import serializers


from _typeshed import Incomplete
class AgentPropertiesSerialize(serializers.ModelSerializer):
    class Meta:
        model: Incomplete = IastAgentProperties
        fields: Incomplete = ['hook_type', 'dump_class']
