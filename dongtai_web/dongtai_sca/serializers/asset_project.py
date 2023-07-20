# !usr/bin/env python
# coding:utf-8
# @author:zhaoyanwei
# @file: asset_project.py
# @time: 2022/5/7  上午7:39
from rest_framework import serializers

from dongtai_common.models.asset import Asset


class AssetProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ["project_id", "project_name", "dependency_level", "package_name"]
