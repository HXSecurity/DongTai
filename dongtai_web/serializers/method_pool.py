#!/usr/bin/env python
# -*- coding:utf-8 -*-

from rest_framework import serializers

from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.asset import Asset
from dongtai_common.utils import http

from dongtai_web.serializers.asset import AssetSerializer


class MethodPoolSerialize(serializers.ModelSerializer):
    DEPENDENCIES = {}
    AGENTS = {}
    request = serializers.SerializerMethodField()
    response = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = MethodPool
        fields = ["url", "request", "response", "language", "dependencies"]

    def get_request(self, obj):
        return http.build_request(
            obj.http_method,
            obj.req_header,
            obj.uri,
            obj.req_params,
            obj.req_data,
            obj.http_protocol,
        )

    def get_response(self, obj):
        return http.build_response(obj.res_header, obj.res_body)

    def get_dependencies(self, obj):
        if obj.agent_id not in self.DEPENDENCIES:
            dependencies = obj.agent.dependencies.values(
                "package_name", "vul_count", "version"
            ).all()
            self.DEPENDENCIES[obj.agent_id] = AssetSerializer(
                dependencies, many=True
            ).data
        return self.DEPENDENCIES[obj.agent_id]

    def get_language(self, obj):
        return obj.agent.language


class MethodPoolListSerialize(serializers.ModelSerializer):
    DEPENDENCIES = {}
    AGENTS = {}
    rule = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    def __init__(self, rule, level, **kwargs):
        super().__init__(**kwargs)
        self._rule = rule
        self._level = level

    class Meta:
        model = MethodPool
        fields = [
            "id",
            "url",
            "req_params",
            "language",
            "update_time",
            "rule",
            "level",
            "agent_name",
        ]

    def get_rule(self, obj):
        return self._rule

    def get_level(self, obj):
        return self._level

    def get_agent_name(self, obj):
        if obj.agent_id not in self.AGENTS:
            self.AGENTS[obj.agent_id] = obj.agent.token
        return self.AGENTS[obj.agent_id]

    def get_language(self, obj):
        return obj.agent.language


if __name__ == "__main__":
    d = Asset()
