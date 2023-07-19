#!/usr/bin/env python
from rest_framework import serializers

from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel


class HookTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookType
        fields = ["id", "name"]


class StrategySerialize(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = IastStrategyModel
        fields = ["id", "vul_name", "name"]

    def get_name(self, obj):
        return obj.vul_name
