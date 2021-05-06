#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:10
# software: PyCharm
# project: lingzhi-engine
from dongtai_models.models.agent_method_pool import MethodPool
from dongtai_models.models.dependency import Dependency
from rest_framework import serializers

from vuln.serializers.dependency import DependencySerialize
from vuln.utils import reduction_req_headers


class MethodPoolSerialize(serializers.ModelSerializer):
    DEPENDENCIES = dict()
    AGENTS = dict()
    req_header = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()

    class Meta:
        model = MethodPool
        fields = ['url', 'req_header', 'res_header', 'res_body', 'language', 'method_pool', 'dependencies']

    def get_req_header(self, obj):
        return reduction_req_headers(obj.http_method, obj.req_header, obj.uri, obj.req_params, obj.req_data,
                                     obj.http_protocol)

    def get_dependencies(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.DEPENDENCIES:
            dependencies = obj.agent.dependencies.all()
            self.DEPENDENCIES[obj.agent_id] = DependencySerialize(dependencies, many=True).data
        return self.DEPENDENCIES[obj.agent_id]


class MethodPoolListSerialize(serializers.ModelSerializer):
    DEPENDENCIES = dict()
    AGENTS = dict()
    rule = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()

    def __init__(self, rule, level, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule
        self.level = level

    class Meta:
        model = MethodPool
        fields = ['id', 'url', 'req_params', 'language', 'update_time', 'rule', 'level', 'agent_name']

    def get_rule(self, obj):
        return self.rule

    def get_level(self, obj):
        return self.level

    def get_agent_name(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.AGENTS:
            self.AGENTS[obj.agent_id] = obj.agent.token
        return self.AGENTS[obj.agent_id]


if __name__ == '__main__':
    d = Dependency()
