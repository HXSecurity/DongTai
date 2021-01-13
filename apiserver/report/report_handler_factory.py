#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 12:00
# software: PyCharm
# project: webapi
from apiserver import const


class ReportHandler:
    HANDLERS = {}

    # 注册handler到当前命名空间，后续进行异步处理数据
    @staticmethod
    def handler(reports):
        """
        处理上传的报告，如果报告的类型不存在，则忽略本次上传；
        检查用户与agent的权限
        :param reports:
        :return:
        """
        report_type = reports.get('type')
        if report_type is None:
            print(reports)
        else:
            if report_type == const.REPORT_HEART_BEAT:
                print(f"心跳报告：{reports}")
            elif report_type == const.REPORT_ERROR_LOG:
                print(f"错误日志报告：{reports}")
            elif report_type == const.REPORT_SCA:
                print(f"SCA报告：{reports}")
            elif report_type == const.REPORT_AUTH_ADD:
                print(f"新增权限报告：{reports}")
            elif report_type == const.REPORT_AUTH_UPDATE:
                print(f"更新权限报告：{reports}")
            elif report_type == const.REPORT_VULN_NORNAL:
                print(f"无调用栈漏洞报告：{reports}")
            elif report_type == const.REPORT_VULN_DYNAMIC:
                print(f"污点跟踪漏洞报告：{reports}")
            elif report_type == const.REPORT_VULN_OVER_POWER:
                print(f"越权检测数据报告：{reports}")
            elif report_type == const.REPORT_VULN_SAAS_POOL:
                print(f"SAAS版污点方法池数据报告：{reports}")
            else:
                print(report_type, type(report_type))

        try:
            ReportHandler.HANDLERS.get(report_type).handler(reports)
        except:
            pass

    @classmethod
    def register(cls, handler_name):
        def wrapper(handler):
            cls.HANDLERS.update({handler_name: handler})
            return handler

        return wrapper
