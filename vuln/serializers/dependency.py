#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 上午11:31
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from vuln.models.dependency import Dependency


class DependencySerialize(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['package_name', 'vul_count', 'version']
