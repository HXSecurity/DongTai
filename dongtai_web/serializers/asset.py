#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-engine
from dongtai_common.models.asset import Asset
from rest_framework import serializers


from _typeshed import Incomplete
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model: Incomplete = Asset
        fields: Incomplete = ['package_name', 'vul_count', 'version']
