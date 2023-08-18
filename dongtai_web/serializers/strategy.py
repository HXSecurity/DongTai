#!/usr/bin/env python
from rest_framework import serializers

from dongtai_common.models.strategy import IastStrategyModel


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = IastStrategyModel
        fields = [
            "id",
            "vul_type",
            "vul_fix",
            "level_id",
            "state",
            "vul_name",
            "vul_desc",
            "dt",
        ]
