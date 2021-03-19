#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/18 下午4:46
# software: PyCharm
# project: lingzhi-engine
import json
import logging

from account.models import User
from core.engine import VulEngine
from lingzhi_engine import const
from lingzhi_engine.base import EndPoint, R
from vuln.models.agent_method_pool import MethodPool
from vuln.serializers.method_pool import MethodPoolListSerialize

logger = logging.getLogger("django")


class SearchEndPoint(EndPoint):
    """
    引擎注册接口
    """
    authentication_classes = []
    permission_classes = []
    name = "api-engine-search"
    description = "引擎-根据策略搜索数据"

    def post(self, request):
        """
        IAST下载 agent接口
        :param request:
        :return:
        服务器作为agent的唯一值绑定
        token: agent-ip-port-path
        """
        # 接受 token名称，version，校验token重复性，latest_time = now.time()
        # 生成agent的唯一token
        # 注册
        try:
            latest_id, page_size, rule_name, rule_msg, rule_level, source_set, sink_set, propagator_set = \
                self.parse_search_condition(request)
            # fixme 考虑入库时直接将数据拆分保存
            method_pool_ids = self.get_match_methods(
                agents=self.get_auth_and_anonymous_agents(request.user),
                source_set=source_set,
                propagator_set=propagator_set,
                sink_set=sink_set,
                latest_id=latest_id,
                match_times=page_size,
                size=page_size * 5)
            if method_pool_ids:
                return R.success(
                    data=self.get_result_data(method_pool_ids, rule_name, rule_level, source_set, sink_set,
                                              propagator_set),
                    latest=method_pool_ids[-1]
                )
            else:
                return R.success(msg='未查询到数据', data=list(), latest=0)
        except Exception as e:
            return R.failure(msg=f"{e}")

    def parse_search_condition(self, request):
        """
        从request对象中解析搜索条件
        :param request:
        :return: 规则ID、规则信息、规则等级、source方法、sink方法、propagator方法
        """
        latest_id = request.query_params.get('latest', 0)
        page_size = request.query_params.get('pageSize', 20)
        if page_size > 100:
            page_size = 100

        rule_id = request.data.get('name', '临时搜索')
        rule_msg = request.data.get('msg')
        rule_level = request.data.get('level')
        rule_sources = request.data.get('sources')
        rule_sinks = request.data.get('sinks')
        rule_propagators = request.data.get('propagators')

        sink_set = set(rule_sinks) if rule_sinks else set()
        source_set = set(rule_sources) if rule_sources else set()
        propagator_set = set(rule_propagators) if rule_propagators else set()

        return latest_id, page_size, rule_id, rule_msg, rule_level, source_set, sink_set, propagator_set

    def get_match_methods(self, agents, source_set, propagator_set, sink_set, latest_id=0, match_times=2, index=0,
                          size=20):
        queryset = MethodPool.objects.filter(id__gt=latest_id, agent__in=agents).order_by('id')
        matches = list()

        while True:
            logger.debug(f'正在搜索，当前第{index + 1}页')
            page = queryset[index * size:(index + 1) * size - 1]
            if page:
                for method_pool in page:
                    method_caller_set = self.convert_method_pool_to_set(method_pool.method_pool)
                    if self.check_match(method_caller_set, source_set, propagator_set, sink_set):
                        match_times = match_times - 1
                        matches.append(method_pool.id)
                    if match_times == 0:
                        break
                if match_times == 0:
                    break
            else:
                break
            index = index + 1
        return matches

    def convert_method_pool_to_set(self, method_pool):
        method_callers = json.loads(method_pool)
        return self.convert_to_set(method_callers)

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

    def get_result_data(self, method_pool_ids, rule_name, rule_level, source_set, sink_set, propagator_set):
        method_pools = MethodPool.objects.filter(id__in=method_pool_ids)
        data = list()
        if sink_set:
            engine = VulEngine()
            for method_pool in method_pools:
                for sink in sink_set:
                    engine.search(
                        method_pool=json.loads(method_pool.method_pool),
                        vul_method_signature=sink
                    )
                    status, links, source, sink = engine.result()
                    if status:
                        method_caller_set = self.convert_to_set(links)
                        if self.check_match(method_caller_set, source_set, propagator_set):
                            top_link = links[0]
                            data.append({
                                'id': method_pool.id,
                                'url': method_pool.url,
                                'req_params': method_pool.req_params,
                                'language': method_pool.language,
                                'update_time': method_pool.update_time,
                                'rule': rule_name,
                                'level': rule_level,
                                'agent_name': method_pool.agent.token,
                                'top_stack': f"{top_link[0]['className'].replace('/', '.')}.{top_link[0]['methodName']}",
                                'bottom_stack': f"{top_link[-1]['className'].replace('/', '.')}.{top_link[-1]['methodName']}",
                                'link_count': len(links)
                            })

        else:
            data = MethodPoolListSerialize(rule=rule_name, level=rule_level, instance=method_pools, many=True).data
        return data
