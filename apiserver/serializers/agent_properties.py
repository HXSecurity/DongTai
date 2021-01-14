#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午2:59
# software: PyCharm
# project: lingzhi-agent-server
from rest_framework import serializers

from apiserver.models.agent_properties import IastAgentProperties


class AgentPropertiesSerialize(serializers.ModelSerializer):
    class Meta:
        model = IastAgentProperties
        fields = ['hook_type', 'dump_class']
