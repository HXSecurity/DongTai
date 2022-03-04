#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:54
# software: PyCharm
# project: webapi
from apiserver.report.handler.error_log_handler import ErrorLogHandler
from apiserver.report.handler.heartbeat_handler import HeartBeatHandler
from apiserver.report.handler.narmal_vul_handler import NormalVulnHandler
from apiserver.report.handler.saas_method_pool_handler import SaasMethodPoolHandler
from apiserver.report.handler.sca_handler import (ScaHandler, ScaBulkHandler)
from apiserver.report.handler.api_route_handler import ApiRouteHandler
from apiserver.report.handler.hardencode_vul_handler import HardEncodeVulHandler

if __name__ == '__main__':
    ErrorLogHandler()
    HeartBeatHandler()
    ScaHandler()
    NormalVulnHandler()
    SaasMethodPoolHandler()
    ApiRouteHandler()
    HardEncodeVulHandler()
    ScaBulkHandler()
