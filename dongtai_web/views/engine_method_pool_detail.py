#!/usr/bin/env python
import json
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.engine.vul_engine import VulEngine
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_web.serializers.method_pool import MethodPoolListSerialize

logger = logging.getLogger("dongtai-webapi")


class MethodPoolDetailProxy(AnonymousAndUserEndPoint):
    name = "api-engine-search"
    description = _("Engine - search data according to policy")

    @extend_schema(
        tags=[_("Method Pool")],
        summary="方法调用链详情",
    )
    def post(self, request):
        """
        :param request:
        :return:
        token: agent-ip-port-path
        """

        try:
            (
                latest_id,
                page_size,
                rule_name,
                rule_msg,
                rule_level,
                source_set,
                sink_set,
                propagator_set,
            ) = self.parse_search_condition(request)
            auth_agents = self.get_auth_and_anonymous_agents(request.user).values("id")

            auth_agent_ids = [agent["id"] for agent in auth_agents]
            method_pool_ids = self.get_match_methods(
                agents=auth_agent_ids,
                source_set=source_set,
                propagator_set=propagator_set,
                sink_set=sink_set,
                latest_id=latest_id,
                page_size=page_size,
                size=page_size * 5,
            )
            if method_pool_ids is None:
                return R.success(msg=_("Not queried"), data=[], latest=0)

            return R.success(
                data=self.get_result_data(
                    method_pool_ids,
                    rule_name,
                    rule_level,
                    source_set,
                    sink_set,
                    propagator_set,
                ),
                latest=method_pool_ids[-1],
            )
        except Exception:
            return R.failure(msg=_("Acquisition fail"))

    @staticmethod
    def parse_search_condition(request):
        """
        :param request:
        :return:
        """
        latest_id = int(request.query_params.get("latest", 0))
        page_size = int(request.query_params.get("pageSize", 20))
        if page_size > 100:
            page_size = 100

        rule_id = request.data.get("name", _("Temporary search"))
        rule_msg = request.data.get("msg")
        rule_level = request.data.get("level")
        rule_sources = request.data.get("sources")
        rule_sinks = request.data.get("sinks")
        rule_propagators = request.data.get("propagators")

        sink_set = set(rule_sinks) if rule_sinks else set()
        source_set = set(rule_sources) if rule_sources else set()
        propagator_set = set(rule_propagators) if rule_propagators else set()

        return (
            latest_id,
            page_size,
            rule_id,
            rule_msg,
            rule_level,
            source_set,
            sink_set,
            propagator_set,
        )

    def get_match_methods(
        self,
        agents,
        source_set,
        propagator_set,
        sink_set,
        latest_id=0,
        page_size=20,
        index=0,
        size=20,
    ):
        queryset = MethodPool.objects.order_by("id")
        if latest_id == 0:
            queryset = queryset.filter(agent_id__in=agents)
        else:
            queryset = queryset.filter(id__gt=latest_id, agent_id__in=agents)
        if queryset.values("id").exists() is False:
            return None

        matches = []
        while True:
            logger.debug(_("Searching, current {} page").format(index + 1))
            page = queryset.values("id", "method_pool")[
                index * size : (index + 1) * size - 1
            ]
            if page:
                if len(matches) == page_size:
                    break
                for method_pool in page:
                    if len(matches) == page_size:
                        break
                    method_caller_set = self.convert_method_pool_to_set(
                        method_pool["method_pool"]
                    )
                    if self.check_match(
                        method_caller_set, source_set, propagator_set, sink_set
                    ):
                        matches.append(method_pool["id"])
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

    def check_match(
        self, method_caller_set, sink_set=None, source_set=None, propagator_set=None
    ):
        """
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

    def get_result_data(
        self,
        method_pool_ids,
        rule_name,
        rule_level,
        source_set,
        sink_set,
        propagator_set,
    ):
        data = []

        method_pools = MethodPool.objects.filter(id__in=method_pool_ids)
        if method_pools.values("id").exists() is False:
            return data

        if len(sink_set) == 0:
            return MethodPoolListSerialize(
                rule=rule_name, level=rule_level, instance=method_pools, many=True
            ).data

        engine = VulEngine()
        for method_pool in method_pools:
            for sink_ in sink_set:
                engine.search(
                    method_pool=json.loads(method_pool.method_pool),
                    vul_method_signature=sink_,
                )
                status, links, source, sink = engine.result()
                if status is False:
                    continue

                method_caller_set = self.convert_to_set(links)
                if (
                    self.check_match(method_caller_set, source_set, propagator_set)
                    is False
                ):
                    continue

                top_link = links[0]
                data.append(
                    {
                        "id": method_pool.id,
                        "url": method_pool.url,
                        "req_params": method_pool.req_params,
                        "language": method_pool.agent.language,
                        "update_time": method_pool.update_time,
                        "rule": rule_name,
                        "level": rule_level,
                        "agent_name": method_pool.agent.token,
                        "top_stack": f"{top_link[0]['className'].replace('/', '.')}.{top_link[0]['methodName']}",
                        "bottom_stack": f"{top_link[-1]['className'].replace('/', '.')}.{top_link[-1]['methodName']}",
                        "link_count": len(links),
                    }
                )

        return data
