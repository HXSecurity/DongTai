#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:10
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from vuln.models.agent_method_pool import MethodPool
from vuln.models.dependency import Dependency
from vuln.serializers.dependency import DependencySerialize
from vuln.serializers.hook_strategy import SinkSerialize


class MethodPoolSerialize(serializers.ModelSerializer):
    class Meta:
        model = MethodPool
        fields = ['url', 'uri', 'http_method', 'req_header', 'req_params', 'req_data', 'res_header', 'res_body',
                  'context_path', 'language', 'method_pool', 'clent_ip', 'create_time', 'update_time']


class MethodPoolListSerialize(serializers.ModelSerializer):
    DEPENDENCIES = dict()
    AGENTS = dict()
    rule = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    dependencies = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    sink_rules = serializers.SerializerMethodField()

    def __init__(self, rule, level, **kwargs):
        super().__init__(**kwargs)
        self.rule = rule
        self.level = level

    class Meta:
        model = MethodPool
        fields = ['id', 'url', 'req_params', 'language', 'update_time', 'rule', 'level', 'dependencies', 'agent_name',
                  'sink_rules']

    def get_rule(self, obj):
        return self.rule

    def get_level(self, obj):
        return self.level

    def get_dependencies(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.DEPENDENCIES:
            dependencies = obj.agent.dependencies.all()
            self.DEPENDENCIES[obj.agent_id] = DependencySerialize(dependencies, many=True).data
        return self.DEPENDENCIES[obj.agent_id]

    def get_agent_name(self, obj):
        # fixme 内存溢出时，优先排查这里，临时使用类成员变量存储，后续考虑使用缓存来做
        if obj.agent_id not in self.AGENTS:
            self.AGENTS[obj.agent_id] = obj.agent.token
        return self.AGENTS[obj.agent_id]

    def get_sink_rules(self, obj):
        # fixme 查询效率过低时，优先排查这里，增加当前方法池命中的sink规则展示
        return SinkSerialize(obj.sinks.all(), many=True).data


if __name__ == '__main__':
    d = Dependency()
