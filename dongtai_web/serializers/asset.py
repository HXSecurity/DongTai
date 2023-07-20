#!/usr/bin/env python
# -*- coding:utf-8 -*-
from dongtai_common.models.asset import Asset
from rest_framework import serializers


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["package_name", "vul_count", "version"]
