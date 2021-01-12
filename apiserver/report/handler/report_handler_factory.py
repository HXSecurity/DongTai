#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/30 10:29
# software: PyCharm
# project: webapi
from apiserver import const
from apiserver.report.handler.auth_info_handler import AuthAddHandler, AuthUpdateHandler
from apiserver.report.handler.error_log_handler import ErrorLogHandler
from apiserver.report.handler.heartbeat_handler import HeartBeatHandler
from apiserver.report.handler.over_power_handler import OverPowerHandler
from apiserver.report.handler.saas_method_pool_handler import SaasMethodPoolHandler
from apiserver.report.handler.sca_handler import ScaHandler


class ReportHandlerFactory:
    @staticmethod
    def get_handler(report_type):
        if report_type == const.REPORT_HEART_BEAT:
            return HeartBeatHandler()
        elif report_type == const.REPORT_ERROR_LOG:
            return ErrorLogHandler()
        elif report_type == const.REPORT_SCA:
            return ScaHandler()
        elif report_type == const.REPORT_AUTH_ADD:
            return AuthAddHandler()
        elif report_type == const.REPORT_AUTH_UPDATE:
            return AuthUpdateHandler()
        # elif report_type == const.REPORT_VULN_NORNAL:
        #     return NormalVulnHandler()
        # elif report_type == const.REPORT_VULN_DYNAMIC:
        #     return DynamicVulnHandler()
        elif report_type == const.REPORT_VULN_OVER_POWER:
            return OverPowerHandler()
        elif report_type == const.REPORT_VULN_SAAS_POOL:
            return SaasMethodPoolHandler()
        else:
            print(report_type, type(report_type))
