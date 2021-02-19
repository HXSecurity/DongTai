#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午7:01
# software: PyCharm
# project: lingzhi-engine

from django.urls import path

from vuln.views.method_pool import MethodPoolEndPoint
from vuln.views.search import SearchEndPoint
from vuln.views.signer import RunSigner
from vuln.views.strategy_run import StrategyRunEndPoint

urlpatterns = [
    # todo
    #   内置策略
    #   我的策略
    #   策略保存
    #   策略结果展示
    # fixme 增加搜素接口，根据输入的查询条件搜索数据
    path('search', SearchEndPoint.as_view()),
    path('run', StrategyRunEndPoint.as_view()),
    path('method_pools', MethodPoolEndPoint.as_view()),
    path('sign', RunSigner.as_view()),
]
