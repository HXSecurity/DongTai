#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi

from core.tasks import search_vul_from_strategy, search_vul_from_method_pool, search_sink_from_method_pool, \
    search_sink_from_strategy
from lingzhi_engine.base import R, EndPoint
import logging

logger = logging.getLogger('lingzhi.webapi')


class StrategyRunEndPoint(EndPoint):
    """
    引擎注册接口
    """
    authentication_classes = []
    permission_classes = []
    name = "api-engine-run"
    description = "引擎运行策略"

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
            logger.info(method_pool_id)
            if method_pool_id:
                logger.info(f'[+] 接收方法池 [{method_pool_id}]')
                search_vul_from_method_pool.delay(method_pool_id)
                search_sink_from_method_pool.delay(method_pool_id)
                logger.info(f'方法池扫描任务 [{method_pool_id}] 已下发')

            strategy_id = request.query_params.get('strategy_id')
            logger.info(strategy_id)
            if strategy_id:
                logger.info(f'[+] 接收策略 [{strategy_id}]')
                search_vul_from_strategy.delay(strategy_id)
                search_sink_from_strategy.delay(strategy_id)
                logger.info(f'策略扫描任务 [{strategy_id}] 已下发')

            return R.success()
        except Exception as e:
            logger.info(f'[-] 方法池扫描任务下发失败，原因：{e}')
            return R.failure(msg=f"{e}")
