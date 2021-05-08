#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/4 下午3:53
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_models.models.strategy import IastStrategyModel


class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = IastStrategyModel
        fields = ['id', 'vul_type', 'level', 'state', 'vul_name', 'vul_desc', 'dt']
