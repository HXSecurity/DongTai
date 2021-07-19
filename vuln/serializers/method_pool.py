#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:10
# software: PyCharm
# project: lingzhi-engine

from rest_framework import serializers

from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.dependency import Dependency
from vuln import utils
from vuln.serializers.dependency import DependencySerialize


class MethodPoolSerialize(serializers.ModelSerializer):
    DEPENDENCIES = dict()
    AGENTS = dict()
    request = serializers.SerializerMethodField()
    response = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()

    class Meta:
        model = MethodPool
        fields = ['url', 'request', 'response', 'language', 'dependencies']

    def get_request(self, obj):
        return utils.build_request(obj.http_method, obj.req_header, obj.uri, obj.req_params, obj.req_data,
                                   obj.http_protocol)

    def get_response(self, obj):
        return utils.build_response(obj.res_header, obj.res_body)

    def get_dependencies(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.DEPENDENCIES:
            dependencies = obj.agent.dependencies.values('package_name', 'vul_count', 'version').all()
            self.DEPENDENCIES[obj.agent_id] = DependencySerialize(dependencies, many=True).data
        return self.DEPENDENCIES[obj.agent_id]

    def get_language(self, obj):
        return obj.agent.language


class MethodPoolListSerialize(serializers.ModelSerializer):
    DEPENDENCIES = dict()
    AGENTS = dict()
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
        fields = ['id', 'url', 'req_params', 'language', 'update_time', 'rule', 'level', 'agent_name']

    def get_rule(self, obj):
        return self._rule

    def get_level(self, obj):
        return self._level

    def get_agent_name(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.AGENTS:
            self.AGENTS[obj.agent_id] = obj.agent.token
        return self.AGENTS[obj.agent_id]

    def get_language(self, obj):
        return obj.agent.language


if __name__ == '__main__':
    d = Dependency()
