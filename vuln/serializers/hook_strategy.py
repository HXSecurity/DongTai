#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 上午11:56
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from vuln.models.hook_strategy import HookStrategy


class SinkSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookStrategy
        fields = ['value']
