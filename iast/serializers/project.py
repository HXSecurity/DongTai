#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午9:55
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from rest_framework import serializers

from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject
from dongtai_models.models.vul_level import IastVulLevel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel


class ProjectSerializer(serializers.ModelSerializer):
    vul_count = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    agent_count = serializers.SerializerMethodField()

    class Meta:
        model = IastProject
        fields = ['id', 'name', 'mode', 'vul_count', 'agent_count', 'owner', 'latest_time']

    def get_agents(self, obj):
        try:
            agents = getattr(obj, 'project_agents')
        except:
            agents = IastAgent.objects.filter(bind_project_id=obj.id).values('id')
            setattr(obj, 'project_agents', agents)
        return agents

    def get_vul_count(self, obj):
        agents = self.get_agents(obj)
        vul_levels = IastVulnerabilityModel.objects.values('level').filter(agent__in=agents).annotate(
            total=Count('level'))
        for vul_level in vul_levels:
            level = IastVulLevel.objects.get(id=vul_level['level'])
            vul_level['name'] = level.name_value
        return list(vul_levels) if vul_levels else list()

    def get_owner(self, obj):
        return obj.user.get_username()

    def get_agent_count(self, obj):
        return len(self.get_agents(obj))
