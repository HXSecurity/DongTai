#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi

import logging

from core.tasks import search_vul_from_strategy, search_vul_from_method_pool, search_sink_from_method_pool, \
    search_sink_from_strategy, search_vul_from_replay_method_pool
from dongtai.endpoint import R, UserEndPoint

logger = logging.getLogger('dongtai-engine')


class StrategyRunEndPoint(UserEndPoint):
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
        """
        try:
            method_pool_id = request.query_params.get('method_pool_id')
            model = request.query_params.get('model')
            if method_pool_id:
                if model == 'replay':
                    self.handler_replay_request(method_pool_id)
                else:
                    self.handler_method_pool(method_pool_id)

            strategy_id = request.query_params.get('strategy_id')
            if strategy_id:
                self.handler_strategy(strategy_id)

            return R.success()
        except Exception as e:
            logger.info(f'[-] 方法池扫描任务下发失败，原因：{e}')
            return R.failure(msg=f"{e}")

    @staticmethod
    def handler_replay_request(replay_method_pool_id):
        logger.info(f'[+] 重放请求[{replay_method_pool_id}]正在下发扫描任务')
        search_vul_from_replay_method_pool.delay(replay_method_pool_id)
        logger.info(f'[+] 重放请求[{replay_method_pool_id}]扫描任务下发完成')

    @staticmethod
    def handler_method_pool(method_pool_id):
        logger.info(f'[+] 扫描任务 [{method_pool_id}]正在下发')
        search_vul_from_method_pool.delay(method_pool_id)
        search_sink_from_method_pool.delay(method_pool_id)
        logger.info(f'扫描任务 [{method_pool_id}] 下发完成')

    @staticmethod
    def handler_strategy(strategy_id):
        logger.info(f'[+] 策略[{strategy_id}]正在下发')
        search_vul_from_strategy.delay(strategy_id)
        search_sink_from_strategy.delay(strategy_id)
        logger.info(f'策略 [{strategy_id}] 下发完成')
