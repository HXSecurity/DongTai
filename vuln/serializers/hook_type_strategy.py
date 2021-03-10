#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/10 下午12:26
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from vuln.models.hook_type import HookType


class HookTypeSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookType
        fields = ['id', 'name']
