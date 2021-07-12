#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午10:12
# software: PyCharm
# project: lingzhi-engine
import json
import logging

from dongtai.models.agent_method_pool import MethodPool

from core.engine import VulEngine
from core.engine_v2 import VulEngineV2
from lingzhi_engine.base import R, AnonymousAndUserEndPoint
from vuln.serializers.method_pool import MethodPoolSerialize
from vuln.views.search import SearchEndPoint

logger = logging.getLogger('dongtai-engine')


class MethodPoolDetailEndPoint(AnonymousAndUserEndPoint):

    def post(self, request):
        try:
            method_pool_id = request.query_params.get('id')
            latest_id, page_size, rule_id, rule_msg, rule_level, source_set, sink_set, propagator_set = \
                SearchEndPoint.parse_search_condition(request)
            # todo 根据条件，处理对应的路径

            if method_pool_id:
                method_pool = MethodPool.objects.filter(
                    agent__in=self.get_auth_and_anonymous_agents(request.user),
                    id=method_pool_id
                ).first()
                if method_pool:
                    data, link_count, method_count = self.search_all_links(method_pool.method_pool)
                    taint_links = []
                    if source_set or sink_set or propagator_set:
                        taint_links = self.search_taint_link(method_pool=method_pool, sources=source_set,
                                                             sinks=sink_set, propagators=propagator_set)
                        self.add_taint_links_to_all_links(taint_links=taint_links, all_links=data)
                    return R.success(data={
                        'vul': MethodPoolSerialize(method_pool).data,
                        'graphData': data,
                        'link_count': link_count,
                        'method_count': method_count,
                        'taint_link': taint_links
                    })
                else:
                    return R.failure(msg='数据不存在或无权限访问')
            return R.failure(msg='方法池ID为空')
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
                if status:
                    method_caller_set = SearchEndPoint.convert_to_set(stack)
                    if self.check_match(method_caller_set, source_set=sources, propagator_set=propagators,
                                        sink_set=sinks):
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
        return SearchEndPoint.convert_to_set(method_callers)

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

    # fixme 删除无效边的功能存在bug
    def delete_invalid_edge(self, graph_data):
        # 寻边
        edge_count = len(graph_data['edges'])
        invalid_edges = list()
        for edge_index in range(edge_count):
            is_invalid_node = False
            has_children = False
            for _edge in graph_data['edges']:
                if graph_data['edges'][edge_index]['target'] == _edge['source']:
                    has_children = True
                    break
            if has_children is False:
                target_node = graph_data['edges'][edge_index]['target']
                source_node = graph_data['edges'][edge_index]['source']
                while True:
                    status, index = self.is_invalid(graph_data['nodes'], target_node)
                    if status:
                        del graph_data['nodes'][index]
                        invalid_edges.append(edge_index)
                        status, index = self.is_invalid(graph_data['nodes'], source_node)
                        if status:
                            del graph_data['nodes'][index]
                        else:
                            break
                    else:
                        break

    @staticmethod
    def is_invalid(nodes, target_node):
        node_count = len(nodes)
        for index in range(node_count):
            node = nodes[index]
            if node['id'] == target_node:
                if MethodPoolDetailEndPoint.is_invalid_node(node['nodeType']):
                    return True, index
        return False, 0

    @staticmethod
    def is_invalid_node(class_name):
        return class_name in (
            'String',
            'StringBuilder',
            'StringReader',
            'Map',
            'List',
            'Enumeration',
        )
