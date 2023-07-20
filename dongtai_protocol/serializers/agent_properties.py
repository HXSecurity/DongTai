#!/usr/bin/env python
# datetime:2021/1/14 下午2:59
from dongtai_common.models.agent_properties import IastAgentProperties
from rest_framework import serializers


class AgentPropertiesSerialize(serializers.ModelSerializer):
    class Meta:
        model = IastAgentProperties
        fields = ["hook_type", "dump_class"]
