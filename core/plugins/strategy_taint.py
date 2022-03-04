#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/10/22 下午2:28
# project: DongTai-engine

# def check_taint(method_pool_model):
#     strategies = load_sink_strategy(method_pool_model.agent.user)
#     engine = VulEngine()
#
#     method_pool = json.loads(method_pool_model.method_pool) if method_pool_model else []
#     engine.method_pool = method_pool
#     if method_pool:
#         for strategy in strategies:
#             if strategy.get('value') in engine.method_pool_signatures:
#                 search_and_save_vul(engine, method_pool_model, method_pool, strategy)
#
