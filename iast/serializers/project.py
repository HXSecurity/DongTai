#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from django.db.models import Count
from rest_framework import serializers

from dongtai.models.agent import IastAgent
from dongtai.models.project import (IastProject, VulValidation)
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.vulnerablity import IastVulnerabilityStatus
from dongtai.utils import const
from dongtai.utils.systemsettings import get_vul_validate

class ProjectSerializer(serializers.ModelSerializer):
    vul_count = serializers.SerializerMethodField(
        help_text="Vulnerability Count")
    owner = serializers.SerializerMethodField(help_text="Project owner")
    agent_count = serializers.SerializerMethodField(
        help_text="Project current surviving agent")
    agent_language = serializers.SerializerMethodField(
        help_text="Agent language currently included in the project")
    USER_MAP = {}

    class Meta:
        model = IastProject
        fields = [
            'id', 'name', 'mode', 'vul_count', 'agent_count', 'owner',
            'latest_time', 'agent_language', 'vul_validation'
        ]

    def get_agents(self, obj):
        try:
            all_agents = getattr(obj, 'project_agents')
        except Exception as agent_not_founc:
            all_agents = IastAgent.objects.values('id').filter(bind_project_id=obj.id)
            setattr(obj, 'project_agents', all_agents)
        return all_agents

    def get_vul_count(self, obj):
        agents = self.get_agents(obj)
        vul_levels = IastVulnerabilityModel.objects.values('level').filter(
            agent__in=agents).annotate(total=Count('level'))
        for vul_level in vul_levels:
            level = IastVulLevel.objects.get(id=vul_level['level'])
            vul_level['name'] = level.name_value
        return list(vul_levels) if vul_levels else list()

    def get_owner(self, obj):
        if obj not in self.USER_MAP:
            self.USER_MAP[obj] = obj.user.get_username()
        return self.USER_MAP[obj]

    def get_agent_count(self, obj):
        return self.get_agents(obj).filter(online=const.RUNNING).count()

    def get_agent_language(self, obj):
        res = self.get_agents(obj).all().values_list(
            'language', flat=True).distinct()
        return list(res)

