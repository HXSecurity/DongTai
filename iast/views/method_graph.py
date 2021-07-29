#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/29 下午3:02
# project: dongtai-webapi

import json
import logging

from dongtai.endpoint import R, AnonymousAndUserEndPoint
from dongtai.engine.vul_engine import VulEngine
from dongtai.engine.vul_engine_v2 import VulEngineV2
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai.utils.validate import Validate

logger = logging.getLogger('dongtai-webapi')


class MethodGraph(AnonymousAndUserEndPoint):
    def get(self, request):
        try:
            method_pool_id = request.query_params.get('method_pool_id')
            method_pool_type = request.query_params.get('method_pool_type')
            if Validate.is_empty(method_pool_id):
                return R.failure(msg='方法池ID为空')

            auth_agents = self.get_auth_and_anonymous_agents(request.user).values('id')
            auth_agent_ids = [agent['id'] for agent in auth_agents]
            if method_pool_type == 'normal':
                method_pool = MethodPool.objects.filter(
                    agent_id__in=auth_agent_ids,
                    id=method_pool_id
                ).first()
            elif method_pool_type == 'replay':
                method_pool = IastAgentMethodPoolReplay.objects.filter(
                    agent_id__in=auth_agent_ids,
                    id=method_pool_id
                ).first()
            else:
                return R.failure(msg='污点调用图类型不存在')

            if method_pool is None:
                return R.failure(msg='数据不存在或无权限访问')

            data, link_count, method_count = self.search_all_links(method_pool.method_pool)
            return R.success(data=data)

        except ValueError as e:
            return R.failure(msg='page和pageSize只能为数字')

    def get_method_pool(self, user, method_pool_id):
        """
        根据用户和方法池ID获取方法池对象
        :param user:
        :param method_pool_id:
        :return:
        """
        return MethodPool.objects.filter(
            agent__in=self.get_auth_and_anonymous_agents(user),
            id=method_pool_id
        ).first()

    def search_all_links(self, method_pool):
        engine = VulEngineV2()
        engine.prepare(method_pool=json.loads(method_pool), vul_method_signature='')
        engine.search_all_link()
        return engine.get_taint_links()

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
        links = list()
        if sinks:
            for sink in sinks:
                engine.search(
                    method_pool=json.loads(method_pool.method_pool),
                    vul_method_signature=sink
                )
                status, stack, source, sink = engine.result()
                if status is False:
                    continue

                method_caller_set = MethodGraph.convert_to_set(stack)
                if self.check_match(
                        method_caller_set=method_caller_set,
                        source_set=sources,
                        propagator_set=propagators,
                        sink_set=sinks
                ) is False:
                    continue

                links.append(stack)
        else:
            method_caller_set = self.convert_method_pool_to_set(method_pool.method_pool)
            if self.check_match(method_caller_set, source_set=sources, propagator_set=propagators):
                links.append([json.loads(method_pool.method_pool)])
        return links

    def add_taint_links_to_all_links(self, taint_links, all_links):
        if taint_links:
            for links in taint_links:
                for link in links:
                    left = None
                    edges = list()
                    for node in link:
                        if node['source']:
                            left = node['invokeId']
                        elif left is not None:
                            right = node['invokeId']
                            edges.append({
                                'source': str(left),
                                'target': str(right)
                            })
                            left = right
                    for edge in edges:
                        for _edge in all_links['edges']:
                            if 'selected' not in _edge and _edge['source'] == edge['source'] and _edge['target'] == \
                                    edge['target']:
                                _edge['selected'] = True

    def convert_method_pool_to_set(self, method_pool):
        method_callers = json.loads(method_pool)
        return MethodGraph.convert_to_set(method_callers)

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

    @staticmethod
    def convert_to_set(method_callers):
        def signature_concat(method_caller):
            return f'{method_caller.get("className").replace("/", ".")}.{method_caller.get("methodName")}'

        method_caller_set = set()
        for method_caller in method_callers:
            if isinstance(method_caller, list):
                for node in method_caller:
                    method_caller_set.add(signature_concat(node))
            elif isinstance(method_caller, dict):
                method_caller_set.add(signature_concat(method_caller))
        return method_caller_set
