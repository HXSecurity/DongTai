#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午2:18
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_models.models.asset import Asset
from dongtai_models.models.project import IastProject


class ScaSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_type = serializers.SerializerMethodField()
    agent = serializers.SerializerMethodField()
    project_cache = dict()

    class Meta:
        model = Asset
        fields = ['id', 'package_name', 'version', 'project_name', 'language', 'agent', 'signature_value', 'level',
                  'level_type', 'vul_count', 'dt', 'agent']

    def get_project_name(self, obj):
        project_id = obj.agent.bind_project_id
        if project_id == 0:
            return "暂未绑定项目"
        else:
            if project_id in self.project_cache:
                return self.project_cache[project_id]
            else:
                self.project_cache[project_id] = IastProject.objects.filter(id=project_id).first().name
                return self.project_cache[project_id]

    def get_level_type(self, obj):
        return obj.level.id

    def get_level(self, obj):
        return obj.level.name_value

    def get_agent(self, obj):
        return obj.agent.token
