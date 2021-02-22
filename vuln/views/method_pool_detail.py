#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午10:12
# software: PyCharm
# project: lingzhi-engine
import json

from account.models import User
from core.engine import VulEngine
from lingzhi_engine import const
from lingzhi_engine.base import R
from vuln.base.method_pool import AnonymousAndUserEndPoint
from vuln.models.agent_method_pool import MethodPool
from vuln.serializers.method_pool import MethodPoolSerialize


class MethodPoolDetailEndPoint(AnonymousAndUserEndPoint):

    def post(self, request):
        try:
            method_pool_id = request.query_params.get('id')
            rule_id, rule_msg, rule_level, source_set, sink_set, propagator_set = \
                self.parse_search_condition(request)

            if method_pool_id:
                if request.user.is_active:
                    method_pool = MethodPool.objects.filter(agent__in=self.get_auth_agents_with_user(request.user),
                                                            id=method_pool_id).first()
                else:
                    # fixme 使用更加优雅的方法，开放靶场的agent数据给每一个用户
                    dt_range_user = User.objects.filter(username=const.USER_BUGENV).first()
                    if dt_range_user:
                        method_pool = MethodPool.objects.filter(agent__in=self.get_auth_agents_with_user(dt_range_user),
                                                                id=method_pool_id).first()
                    else:
                        R.failure(msg='no permission')
                if method_pool:
                    engine = VulEngine()
                    engine.prepare(method_pool=json.loads(method_pool.method_pool), vul_method_signature='')
                    engine.search_all_link()
                    data, link_count, method_count = engine.get_taint_links()
                    # taint_link = self.search_taint_link(method_pool=method_pool, sources=source_set, sinks=sink_set,
                    #                                     propagators=propagator_set)
                    return R.success(data={
                        'vul': MethodPoolSerialize(method_pool).data,
                        'graphData': data,
                        'link_count': link_count,
                        'method_count': method_count
                    })
                else:
                    R.failure(msg='数据不存在')
            return R.failure(msg='方法池ID为空')
        except ValueError as e:
            return R.failure(msg='page和pageSize只能为数字')

    def search_taint_link(self, method_pool, sources, sinks, propagators):
        """
        根据策略搜索满足条件的污点链
          1.如果存在sink点，根据sink点搜索污点链，
            1.1 如果存在污点链
                1.1.1 如果存在source节点或propagator节点，检查污点链中是否存在source节点或propagator节点
                1.1.2 如果不存在，则直接返回污点链
            1.2 如果不存在污点链，返回空
          2.如果不存在sink节点，直接进入2.1
            2.1 如果存在source节点或propagator节点，检查方法池中是否存在source节点或propagator节点
            2.2 如果不存在，返回空
        :param method_pool: 原始方法池
        :param sources: 污点源方法集合
        :param sinks: 危险函数方法集合
        :param propagators: 传播方法集合
        :return: 满足条件的污点链
        """
        engine = VulEngine()
        if sinks:
            for sink in sinks:
                engine.search(
                    method_pool=json.loads(method_pool.method_pool),
                    vul_method_signature=sink
                )
                status, stack, source, sink = engine.result()
                if status:
                    method_caller_set = self.convert_to_set(stack)
                    if self.check_match(method_caller_set, source_set=sources, propagator_set=propagators,
                                        sink_set=sinks):
                        return stack
        else:
            method_caller_set = self.convert_method_pool_to_set(method_pool.method_pool)
            if self.check_match(method_caller_set, source_set=sources, propagator_set=propagators):
                return json.loads(method_pool.method_pool)

    def parse_search_condition(self, request):
        """
        从request对象中解析搜索条件
        :param request:
        :return: 规则ID、规则信息、规则等级、source方法、sink方法、propagator方法
        """
        rule_id = request.data.get('name')
        rule_msg = request.data.get('msg')
        rule_level = request.data.get('level')
        rule_sources = request.data.get('sources')
        rule_sinks = request.data.get('sinks')
        rule_propagators = request.data.get('propagators')

        sink_set = set(rule_sinks) if rule_sinks else set()
        source_set = set(rule_sources) if rule_sources else set()
        propagator_set = set(rule_propagators) if rule_propagators else set()

        return rule_id, rule_msg, rule_level, source_set, sink_set, propagator_set

    def convert_method_pool_to_set(self, method_pool):
        method_callers = json.loads(method_pool)
        return self.convert_to_set(method_callers)

    def convert_to_set(self, method_callers):
        method_caller_set = set()
        for method_caller in method_callers:
            method_caller_set.add(
                f'{method_caller.get("className").replace("/", ".")}.{method_caller.get("methodName")}')
        return method_caller_set

    def check_match(self, method_caller_set, sink_set=None, source_set=None, propagator_set=None):
        """
        根据方法调用栈、source方法调用栈、传播方法调用栈、sink方法调用栈综合判断是否满足条件
        :param method_caller_set:
        :param sink_set:
        :param source_set:
        :param propagator_set:
        :return:
        """
        status = True
        if sink_set:
            result = method_caller_set & sink_set
            status = status and result is not None and len(result) > 0
        if source_set:
            result = method_caller_set & source_set
            status = status and result is not None and len(result) > 0
        if propagator_set:
            result = method_caller_set & propagator_set
            status = status and result is not None and len(result) > 0
        return status
