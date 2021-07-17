#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/10 下午12:26
# software: PyCharm
# project: lingzhi-engine
from dongtai.models.hook_type import HookType
from rest_framework import serializers


class HookTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookType
        fields = ['id', 'name']
