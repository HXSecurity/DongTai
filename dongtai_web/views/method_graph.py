#!/usr/bin/env python

import json
import logging

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

from dongtai_common.endpoint import AnonymousAndUserEndPoint, R
from dongtai_common.engine.vul_engine import VulEngine
from dongtai_common.engine.vul_engine_v2 import VulEngineV2
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.utils import const
from dongtai_common.utils.validate import Validate

logger = logging.getLogger("dongtai-webapi")


class MethodGraph(AnonymousAndUserEndPoint):
    @extend_schema(summary="调用链图", tags=["Method Pool"])
    def get(self, request):
        try:
            method_pool_id = int(request.query_params.get("method_pool_id"))
            method_pool_type = request.query_params.get("method_pool_type")
            replay_id = request.query_params.get("method_pool_replay_id", None)
            replay_type = request.query_params.get("replay_type", None)
            if replay_type is not None and int(replay_type) not in [
                const.API_REPLAY,
                const.REQUEST_REPLAY,
            ]:
                return R.failure(msg="replay_type error")
            replay_type = const.REQUEST_REPLAY if replay_type is None else int(replay_type)
            if Validate.is_empty(method_pool_id) and replay_id is None:
                return R.failure(msg=_("Method pool ID is empty"))

            auth_agents = self.get_auth_and_anonymous_agents(request.user).values("id")
            auth_agent_ids = auth_agents.values_list("id", flat=True)

            cur_ids = [int(item) for item in auth_agent_ids]

            if (
                method_pool_type == "normal"
                and MethodPool.objects.filter(agent_id__in=cur_ids, id=method_pool_id).exists()
            ):
                method_pool = MethodPool.objects.filter(id=method_pool_id).first()
            elif method_pool_type == "replay" and replay_id:
                method_pool = IastAgentMethodPoolReplay.objects.filter(id=replay_id, replay_type=replay_type).first()
            elif (
                method_pool_type == "replay"
                and MethodPool.objects.filter(agent_id__in=cur_ids, id=method_pool_id).exists()
            ):
                method_pool = IastAgentMethodPoolReplay.objects.filter(
                    relation_id=method_pool_id, replay_type=replay_type
                ).first()
            else:
                return R.failure(msg=_("Stain call map type does not exist"))

            if method_pool is None:
                return R.failure(msg=_("Data does not exist or no permission to access"))

            data, link_count, method_count = self.search_all_links(method_pool.method_pool)
            return R.success(data=data)

        except Exception as e:
            logger.error(e, exc_info=True)
            return R.failure(msg=_("Page and PageSize can only be numeric"))

    def get_method_pool(self, user, method_pool_id):
        """
        :param user:
        :param method_pool_id:
        :return:
        """
        return MethodPool.objects.filter(agent__in=self.get_auth_and_anonymous_agents(user), id=method_pool_id).first()

    def search_all_links(self, method_pool):
        engine = VulEngineV2()
        engine.prepare(method_pool=json.loads(method_pool), vul_method_signature="")
        engine.search_all_link()
        return engine.get_taint_links()

    def search_taint_link(self, method_pool, sources, sinks, propagators):
        """
        :param method_pool:
        :param sources:
        :param sinks:
        :param propagators:
        :return:
        """
        engine = VulEngine()
        links = []
        if sinks:
            for sink_ in sinks:
                sink = sink_
                engine.search(
                    method_pool=json.loads(method_pool.method_pool),
                    vul_method_signature=sink,
                )
                status, stack, source, sink = engine.result()
                if status is False:
                    continue

                method_caller_set = MethodGraph.convert_to_set(stack)
                if (
                    self.check_match(
                        method_caller_set=method_caller_set,
                        source_set=sources,
                        propagator_set=propagators,
                        sink_set=sinks,
                    )
                    is False
                ):
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
                    edges = []
                    for node in link:
                        if node["source"]:
                            left = node["invokeId"]
                        elif left is not None:
                            right = node["invokeId"]
                            edges.append({"source": str(left), "target": str(right)})
                            left = right
                    for edge in edges:
                        for _edge in all_links["edges"]:
                            if (
                                "selected" not in _edge
                                and _edge["source"] == edge["source"]
                                and _edge["target"] == edge["target"]
                            ):
                                _edge["selected"] = True

    def convert_method_pool_to_set(self, method_pool):
        method_callers = json.loads(method_pool)
        return MethodGraph.convert_to_set(method_callers)

    def check_match(self, method_caller_set, sink_set=None, source_set=None, propagator_set=None):
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
