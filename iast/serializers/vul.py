#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:29
# software: PyCharm
# project: webapi
from dongtai.models.agent import IastAgent
from rest_framework import serializers

from dongtai.models.vulnerablity import IastVulnerabilityModel


class VulSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    AGENT_LANGUAGE_MAP = {}

    class Meta:
        model = IastVulnerabilityModel
        fields = ['id', 'type', 'url', 'uri', 'agent_id', 'level_id', 'http_method', 'top_stack', 'bottom_stack',
                  'taint_position', 'latest_time', 'first_time', 'language', 'status']

    @staticmethod
    def split_container_name(name):
        result = ""
        if '/' in name:
            result = name.split('/')[0].lower().strip()
        elif ' ' in name:
            names = name.split(' ')[:-1]
            result = ' '.join(names).lower().strip()
        return result

    def get_language(self, obj):
        if obj['agent_id'] not in self.AGENT_LANGUAGE_MAP:
            agent_model = IastAgent.objects.filter(id=obj['agent_id']).first()
            if agent_model:
                self.AGENT_LANGUAGE_MAP[obj['agent_id']] = agent_model.language
        return self.AGENT_LANGUAGE_MAP[obj['agent_id']]


class VulForPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastVulnerabilityModel
        fields = ['id', 'type', 'level', 'url', 'http_method', 'top_stack', 'bottom_stack']
