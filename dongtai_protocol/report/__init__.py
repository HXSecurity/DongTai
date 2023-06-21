#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:54
# software: PyCharm
# project: webapi
from dongtai_protocol.report.handler.error_log_handler import ErrorLogHandler
from dongtai_protocol.report.handler.heartbeat_handler import HeartBeatHandler
from dongtai_protocol.report.handler.narmal_vul_handler import NormalVulnHandler
from dongtai_protocol.report.handler.saas_method_pool_handler import SaasMethodPoolHandler
from dongtai_protocol.report.handler.sca_handler import (ScaHandler,
                                                         ScaBulkHandler)
from dongtai_protocol.report.handler.api_route_handler import ApiRouteHandler
from dongtai_protocol.report.handler.api_route_v2_handler import ApiRouteV2Handler
from dongtai_protocol.report.handler.hardencode_vul_handler import HardEncodeVulHandler
from dongtai_protocol.report.handler.agent_third_service_handler import ThirdPartyServiceHandler
from dongtai_protocol.report.handler.agent_filepath_handler import FilePathHandler

if __name__ == '__main__':
    ErrorLogHandler()
    HeartBeatHandler()
    ScaHandler()
    NormalVulnHandler()
    SaasMethodPoolHandler()
    ApiRouteHandler()
    ApiRouteV2Handler()
    HardEncodeVulHandler()
    ScaBulkHandler()
    ThirdPartyServiceHandler()
    FilePathHandler()
