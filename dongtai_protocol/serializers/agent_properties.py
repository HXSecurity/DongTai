#!/usr/bin/env python
# datetime:2021/1/14 下午2:59
from rest_framework import serializers

from dongtai_common.models.agent_properties import IastAgentProperties


class AgentPropertiesSerialize(serializers.ModelSerializer):
    class Meta:
        model = IastAgentProperties
        fields = ["hook_type", "dump_class"]
