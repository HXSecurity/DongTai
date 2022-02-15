#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午7:01
# software: PyCharm
# project: lingzhi-engine

from django.urls import path

from vuln.views.health import HealthEndPoint
from vuln.views.proxy import ProxyEndPoint
from vuln.views.strategy_run import StrategyRunEndPoint
from vuln.views.sca import ScaEndPoint

urlpatterns = [
    path('run', StrategyRunEndPoint.as_view()),
    path('health', HealthEndPoint.as_view()),
    path('sca', ScaEndPoint.as_view()),
    path('proxy', ProxyEndPoint.as_view()),
]
