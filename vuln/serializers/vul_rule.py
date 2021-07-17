#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:05
# software: PyCharm
# project: lingzhi-engine
from dongtai.models.vul_rule import IastVulRule
from rest_framework import serializers


class VulRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastVulRule
        fields = ['id', 'rule_name', 'rule_msg']


class VulRuleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastVulRule
        fields = ['id', 'rule_name', 'rule_msg', 'rule_value']
