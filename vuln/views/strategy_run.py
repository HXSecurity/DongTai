#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi

from core.tasks import search_vul_from_strategy, search_vul_from_method_pool, search_sink_from_method_pool
from lingzhi_engine.base import R, EndPoint


class StrategyRunEndPoint(EndPoint):
    """
    引擎注册接口
    """
    authentication_classes = []
    permission_classes = []
    name = "api-v1-agent-register"
    description = "引擎注册"

    def get(self, request):
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
            method_pool_id = request.query_params.get('method_pool_id')
            if method_pool_id:
                search_vul_from_method_pool.delay(method_pool_id)
                # search_sink_from_method_pool.delay(method_pool_id)
                search_sink_from_method_pool(method_pool_id)

            strategy_id = request.query_params.get('strategy_id')
            if strategy_id:
                search_vul_from_strategy.delay(strategy_id)

            return R.success()
        except Exception as e:
            return R.failure(msg=f"{e}")
