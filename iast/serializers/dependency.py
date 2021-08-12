#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-engine
from dongtai.models.dependency import Dependency
from rest_framework import serializers


class DependencySerialize(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['package_name', 'vul_count', 'version']
