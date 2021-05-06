#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 上午11:31
# software: PyCharm
# project: lingzhi-engine
from dongtai_models.models.dependency import Dependency
from rest_framework import serializers



class DependencySerialize(serializers.ModelSerializer):
    class Meta:
        model = Dependency
        fields = ['package_name', 'vul_count', 'version']
