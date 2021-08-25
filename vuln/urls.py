#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午7:01
# software: PyCharm
# project: lingzhi-engine

from django.urls import path

from vuln.views.health import HealthEndPoint
from vuln.views.strategy_run import StrategyRunEndPoint

urlpatterns = [
    path('run', StrategyRunEndPoint.as_view()),
    path('health', HealthEndPoint.as_view()),
]
