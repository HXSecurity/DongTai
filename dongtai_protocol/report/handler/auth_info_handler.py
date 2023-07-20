#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi

import datetime

from dongtai_common.models.iast_overpower_user import IastOverpowerUserAuth
from dongtai_common.utils import const

from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler


@ReportHandler.register("auth-info-report")
class AuthInfoHandler:
    RECIVED_AUTH_INFO = set()

    @staticmethod
    def handler(reports):
        report_value = reports.get("report")
        AuthInfoHandler.RECIVED_AUTH_INFO.add(report_value["auth-value"])
        for authinfo in AuthInfoHandler.RECIVED_AUTH_INFO:
            print(f"==>> recived auth ifno: {authinfo}")

    @staticmethod
    def get_new_authinfo(authinfo):
        for _authinfo in AuthInfoHandler.RECIVED_AUTH_INFO:
            if _authinfo == authinfo:
                continue
            return _authinfo


@ReportHandler.register(const.REPORT_AUTH_ADD)
class AuthAddHandler(IReportHandler):
    def parse(self):
        # todo 增加appnem字段
        self.server_name = self.detail.get("server_name")
        self.server_port = self.detail.get("server_port")
        self.http_url = self.detail.get("http_url")
        self.http_query_string = self.detail.get("http_query_string")
        self.auth_sql = self.detail.get("auth_sql")
        self.jdbc_class = self.detail.get("jdbc_class")
        self.auth_value = self.detail.get("auth_value")
        self.app_name = ""

    def save(self):
        try:
            auth_model = IastOverpowerUserAuth.objects.filter(
                app_name=self.app_name,
                server_name=self.server_name,
                server_port=self.server_port,
                http_url=self.http_url,
                http_query_string=self.http_query_string,
                auth_sql=self.auth_sql,
                jdbc_class=self.jdbc_class,
                auth_value=self.auth_value,
            )
            if len(auth_model):
                print("权限已存在，忽略")
                pass
            else:
                print("新增权限")
                IastOverpowerUserAuth(
                    app_name=self.app_name,
                    server_name=self.server_name,
                    server_port=self.server_port,
                    http_url=self.http_url,
                    http_query_string=self.http_query_string,
                    auth_sql=self.auth_sql,
                    jdbc_class=self.jdbc_class,
                    auth_value=self.auth_value,
                    user_id=self.user_id,
                    created_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ).save()
        except Exception as e:
            pass


@ReportHandler.register(const.REPORT_AUTH_UPDATE)
class AuthUpdateHandler(IReportHandler):
    """
    {
        'server_name': '127.0.0.1',
        'auth_updated': 'csrftoken=A00l4Ok1bkiWiG1OWbPgneUiM5uFGnzVyfH4qllr1hTvw3QCmqjG0VqCnwfga8PF; _jspxcms=1b40610d1eb840498b9826c7b2809418; __utma=96992031.1435321630.1598931302.1598931302.1598931302.1; __utmz=96992031.1598931302.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_bdff1c1dcce971c3d986f9be0921a0ee=1598346920,1598434566,1599821526; JSESSIONID=B6CD0D586705E844E0B3DB4D840E0580',
        'server_port': 8080,
        'http_query_string': 'id=1',
        'auth_original': 'csrftoken=A00l4Ok1bkiWiG1OWbPgneUiM5uFGnzVyfH4qllr1hTvw3QCmqjG0VqCnwfga8PF; _jspxcms=1b40610d1eb840498b9826c7b2809418; __utma=96992031.1435321630.1598931302.1598931302.1598931302.1; __utmz=96992031.1598931302.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_bdff1c1dcce971c3d986f9be0921a0ee=1598346920,1598434566,1599821526; JSESSIONID=92766CDBD4888ACC278B7D88BAAAF352',
        'http_url': 'http://127.0.0.1:8080/overpower/read-03'
    }
    """

    def parse(self):
        self.app_name = self.detail.get("app_name")
        self.server_name = self.detail.get("server_name")
        self.server_port = self.detail.get("server_port")
        self.http_url = self.detail.get("http_url")
        self.http_query_string = self.detail.get("http_query_string")
        self.auth_original = self.detail.get("auth_original")
        self.auth_updated = self.detail.get("auth_updated")

    def save(self):
        try:
            print("存储权限变更报告")
            auth_model = IastOverpowerUserAuth.objects.filter(
                app_name=self.app_name,
                server_name=self.server_name,
                server_port=self.server_port,
                http_url=self.http_url,
                http_query_string=self.http_query_string,
                auth_value=self.auth_original,
            )
            if len(auth_model) > 0:
                print("处理权限变更")
            else:
                print("忽略权限变更")
        except Exception as e:
            raise e
            pass
