#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午2:18
# software: PyCharm
# project: lingzhi-webapi
from dongtai.models.project_version import IastProjectVersion
from rest_framework import serializers

from dongtai.models.asset import Asset
from dongtai.models.project import IastProject


class ScaSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    project_version = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_type = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    project_cache = dict()
    project_version_cache = dict()

    class Meta:
        model = Asset
        fields = ['id', 'package_name', 'version', 'project_name', 'project_version', 'language', 'agent_name',
                  'signature_value', 'level', 'level_type', 'vul_count', 'dt']

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

    def get_project_version(self, obj):
        project_version_id = obj.agent.project_version_id
        if project_version_id:
            if project_version_id in self.project_version_cache:
                return self.project_version_cache[project_version_id]
            else:
                project_version = IastProjectVersion.objects.values('version_name').filter(
                    id=project_version_id).first()
                self.project_version_cache[project_version_id] = project_version['version_name']

            return self.project_version_cache[project_version_id]
        else:
            return '暂未创建项目版本'

    def get_level_type(self, obj):
        return obj.level.id

    def get_level(self, obj):
        return obj.level.name_value

    def get_agent_name(self, obj):
        return obj.agent.token
