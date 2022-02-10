#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:29
# software: PyCharm
# project: webapi
from dongtai.models.agent import IastAgent
from rest_framework import serializers

from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.vulnerablity import IastVulnerabilityStatus
from dongtai.models.hook_type import HookType
from django.utils.translation import gettext_lazy as _
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vul_level import IastVulLevel


class VulSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    AGENT_LANGUAGE_MAP = {}
    status = serializers.SerializerMethodField()
    class Meta:
        model = IastVulnerabilityModel
        fields = [
            'id', 'type', 'hook_type_id', 'url', 'uri', 'agent_id', 'level_id',
            'http_method', 'top_stack', 'bottom_stack', 'taint_position',
                'latest_time', 'first_time', 'language', 'status'
        ]

    @staticmethod
    def split_container_name(name):
        if name is None:
            return ""
        if '/' in name:
            return name.split('/')[0].lower().strip()
        elif ' ' in name:
            names = name.split(' ')[:-1]
            return ' '.join(names).lower().strip()
        return name

    def get_language(self, obj):
        if obj['agent_id'] not in self.AGENT_LANGUAGE_MAP:
            agent_model = IastAgent.objects.filter(id=obj['agent_id']).first()
            if agent_model:
                self.AGENT_LANGUAGE_MAP[obj['agent_id']] = agent_model.language
        return self.AGENT_LANGUAGE_MAP[obj['agent_id']]

    def get_type(self, obj):
        hook_type = HookType.objects.filter(pk=obj['hook_type_id']).first()
        hook_type_name = hook_type.name if hook_type else None
        strategy = IastStrategyModel.objects.filter(pk=obj['strategy_id']).first()
        strategy_name = strategy.vul_name if strategy else None
        type_ = list(
            filter(lambda x: x is not None, [strategy_name, hook_type_name]))
        return type_[0] if type_ else ''

    def get_status(self, obj):
        status = IastVulnerabilityStatus.objects.filter(
            pk=obj['status_id']).first()
        return status.name if status else ''


class VulForPluginSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField(help_text=_("The level name of vulnerablity"))
    class Meta:
        model = IastVulnerabilityModel
        fields = [
            'id', 'type', 'level_id', 'url', 'http_method', 'top_stack',
            'bottom_stack', 'hook_type_id', 'level'
        ]

    def get_type(self, obj):
        hook_type = HookType.objects.filter(pk=obj['hook_type_id']).first()
        hook_type_name = hook_type.name if hook_type else None
        strategy = IastStrategyModel.objects.filter(pk=obj['strategy_id']).first()
        strategy_name = strategy.vul_name if strategy else None
        type_ = list(
            filter(lambda x: x is not None, [strategy_name, hook_type_name]))
        return type_[0] if type_ else ''

    def get_level(self, obj):
        level = IastVulLevel.objects.filter(pk=obj['level_id']).first()
        return level.name_value if level else ''


class VulSummaryLanguageSerializer(serializers.Serializer):
    language = serializers.CharField(help_text=_("programming language"))
    count = serializers.IntegerField(help_text=_(
        "The number of vulnerabilities corresponding to the programming language"
    ))


class VulSummaryLevelSerializer(serializers.Serializer):
    level = serializers.CharField(help_text=_("The name of vulnerablity level"))
    count = serializers.IntegerField(help_text=_("The number of vulnerabilities corresponding to the level"))
    level_id = serializers.IntegerField(help_text=_("The id of vulnerablity level"))


class VulSummaryTypeSerializer(serializers.Serializer):
    type = serializers.CharField(help_text=_("The name of vulnerablity type"))
    count = serializers.IntegerField(help_text=_(
        "The number of vulnerabilities corresponding to the vulnerablity type")
                                     )


class VulSummaryProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(
        help_text=_("The name of the project"))
    count = serializers.IntegerField(help_text=_(
        "The number of vulnerabilities corresponding to the project"))
    id = serializers.IntegerField(help_text=_("The id of the project"))


class VulSummaryResponseDataSerializer(serializers.Serializer):
    language = VulSummaryLanguageSerializer(many=True)
    level = VulSummaryLevelSerializer(many=True)
    type = VulSummaryTypeSerializer(many=True)
    projects = VulSummaryProjectSerializer(many=True)
