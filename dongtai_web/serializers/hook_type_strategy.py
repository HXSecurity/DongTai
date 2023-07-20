#!/usr/bin/env python
# -*- coding:utf-8 -*-
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from rest_framework import serializers


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
