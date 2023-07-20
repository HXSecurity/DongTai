#!/usr/bin/env python
from rest_framework import serializers

from dongtai_common.models.asset import Asset


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["package_name", "vul_count", "version"]
