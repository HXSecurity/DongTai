#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from dongtai.models.agent import IastAgent
from dongtai.models.project_version import IastProjectVersion
from rest_framework import serializers

from dongtai.models.asset import Asset
from dongtai.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from dongtai.models.sca_maven_db import ScaMavenDb

class ScaSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    project_version = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_type = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    license = serializers.SerializerMethodField()
    project_cache = dict()
    project_version_cache = dict()
    AGENT_LANGUAGE_MAP = {}

    class Meta:
        model = Asset
        fields = [
            'id', 'package_name', 'version', 'project_name', 'project_id',
            'project_version', 'language', 'package_path', 'agent_name',
            'signature_value', 'level', 'level_type', 'vul_count', 'dt','license'
        ]

    def get_project_name(self, obj):
        project_id = obj.agent.bind_project_id
        if project_id == 0:
            return _("The application has not been binded")
        else:
            if project_id in self.project_cache:
                return self.project_cache[project_id]
            else:
                self.project_cache[project_id] = IastProject.objects.filter(id=project_id).first().name
                return self.project_cache[project_id]

    def get_project_id(self, obj):
        return obj.agent.bind_project_id

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
            return _('No application version has been created')

    def get_level_type(self, obj):
        return obj.level.id

    def get_level(self, obj):
        return obj.level.name_value

    def get_agent_name(self, obj):
        return obj.agent.token

    def get_language(self, obj):
        if obj.agent_id not in self.AGENT_LANGUAGE_MAP:
            agent_model = IastAgent.objects.filter(id=obj.agent_id).first()
            if agent_model:
                self.AGENT_LANGUAGE_MAP[obj.agent_id] = agent_model.language
        return self.AGENT_LANGUAGE_MAP[obj.agent_id]

    def get_license(self,obj):
        try:
            if not self.context.has_key('license_dict'):
                sca_maven = ScaMavenDb.objects.filter(sha_1=obj.signature_value).first()
                return sca_maven.license
            return self.context['license_dict'].get(obj.signature_value,'')
        except Exception as e:
            return ''
    def get_package_name(self,obj):
        if obj.package_name.startswith('maven:') and obj.package_name.endswith(':'):
            return obj.package_name.replace('maven:','',1)[:-1]
        return obj.package_name
