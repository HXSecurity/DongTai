#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 18:13
# software: PyCharm
# project: webapi
import datetime
import json
import time

from dongtai_common.models.iast_overpower_user import IastOverpowerUserAuth
from dongtai_common.models.iast_vul_overpower import IastVulOverpower
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_common.utils import const

from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler


@ReportHandler.register(const.REPORT_VULN_OVER_POWER)
class OverPowerHandler(IReportHandler):
    def parse(self):
        """
        {
            'server_name': '127.0.0.1',
            'http_uri': '/overpower/read-02',
            'cookie': 'csrftoken=A00l4Ok1bkiWiG1OWbPgneUiM5uFGnzVyfH4qllr1hTvw3QCmqjG0VqCnwfga8PF; _jspxcms=1b40610d1eb840498b9826c7b2809418; __utma=96992031.1435321630.1598931302.1598931302.1598931302.1; __utmz=96992031.1598931302.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_bdff1c1dcce971c3d986f9be0921a0ee=1598346920,1598434566,1599821526; JSESSIONID=2F55FC8B6CBEC0E0F38018AD211AFDC8',
            'http_protocol': 'HTTP/1.1',
            'http_url': 'http://127.0.0.1:8080/overpower/read-02',
            'sql': 'SELECT * FROM article WHERE id=1',
            'app_name': '127.0.0.1',
            'x-trace-id': 'tomcat-docbase.14532572676169694122.8080-sql-3eea90fc-367c-47ab-9bb3-efa0683f58a3',
            'http_method': 'GET',
            'server_port': 8080,
            'http_scheme': 'http',
            'http_query_string': 'id=1',
            'http_header': 'host:127.0.0.1:8080\nconnection:keep-alive\nupgrade-insecure-requests:1\nuser-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36\naccept:text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\nsec-fetch-site:none\nsec-fetch-mode:navigate\nsec-fetch-user:?1\nsec-fetch-dest:document\naccept-encoding:gzip, deflate, br\naccept-language:zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6\ncookie:csrftoken=A00l4Ok1bkiWiG1OWbPgneUiM5uFGnzVyfH4qllr1hTvw3QCmqjG0VqCnwfga8PF; _jspxcms=1b40610d1eb840498b9826c7b2809418; __utma=96992031.1435321630.1598931302.1598931302.1598931302.1; __utmz=96992031.1598931302.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_bdff1c1dcce971c3d986f9be0921a0ee=1598346920,1598434566,1599821526; JSESSIONID=2F55FC8B6CBEC0E0F38018AD211AFDC8\n'
        }
        :return:
        """
        self.app_name = self.detail.get("app_name")
        self.app_path = self.detail.get("app_path")
        self.server_name = self.detail.get("server_name")
        self.server_port = self.detail.get("server_port")
        self.http_url = self.detail.get("http_url")
        self.http_uri = self.detail.get("http_uri")
        self.http_query_string = self.detail.get("http_query_string")
        self.http_method = self.detail.get("http_method")
        self.http_scheme = self.detail.get("http_scheme")
        self.http_protocol = self.detail.get("http_protocol")
        self.http_header = self.detail.get("http_header")
        self.x_trace_id = self.detail.get("x-trace-id")
        self.cookie = self.detail.get("cookie")
        self.sql = self.detail.get("sql")

    def save(self):
        # 检查trace_id是否存于数据库中
        vul_model = IastVulOverpower.objects.filter(
            app_name=self.app_name,
            server_name=self.server_name,
            server_port=self.server_port,
            http_url=self.http_url,
            http_query_string=self.http_query_string,
            http_method=self.http_method,
            x_trace_id=self.x_trace_id,
            sql=self.sql,
        )
        if len(vul_model):
            # 检查越权
            if vul_model[0].cookie != self.cookie:
                detail_report = {
                    "trace-id": self.x_trace_id,
                    "server-name": self.server_name,
                    "server-port": self.server_port,
                    "http-method": self.http_method,
                    "http-url": self.http_url,
                    "http-query-string": self.http_query_string,
                    "http-original-auth": vul_model[0].cookie,
                    "http-original-user": self.get_user_from_auth(vul_model[0].cookie),
                    "http-current-auth": self.cookie,
                    "http-current-user": self.get_user_from_auth(self.cookie),
                    "http-sql": self.server_name,
                }
                # 通过cookie查询原始的用户
                # 检查是否已存在漏洞，如果存在，则忽略，如果不存在则上报漏洞
                vuls = IastVulnerabilityModel.objects.filter(
                    vul_url=self.http_url,
                    vul_type="越权漏洞",
                    vul_req_method=self.http_method,
                    protocol=self.http_protocol,
                )
                if len(vuls) > 0:
                    vuls[0].vul_count = vuls[0].vul_count + 1
                    vuls[0].vul_last_time = int(time.time())
                    vuls[0].save()
                else:
                    IastVulnerabilityModel(
                        type="越权漏洞",
                        vul_level="中危",
                        url=self.http_url,
                        uri=self.http_uri,
                        http_method=self.http_method,
                        http_scheme=self.http_scheme,
                        http_protocol=self.http_protocol,
                        req_header=self.http_header,
                        req_params=self.http_query_string,
                        req_data="",  # fixme 请求体 数据保存
                        res_header="",  # fixme 响应头，暂时没有，后续补充
                        res_body="",  # fixme 响应体数据
                        full_stack=json.dumps(detail_report, ensure_ascii=False),
                        top_stack="",
                        bottom_stack="",
                        taint_value=None,
                        taint_position=None,
                        app_id=self.app_id,  # fixme app id 暂时不存该字段
                        app_name=self.app_name,
                        server_id=self.server_id,  # fixme app id 暂时不存该字段
                        server_name=self.server_name,
                        counts=1,
                        status="已上报",
                        first_time=int(time.time()),
                        latest_time=int(time.time()),
                    ).save()
        else:
            IastVulOverpower(
                app_name=self.app_name,
                server_name=self.server_name,
                server_port=self.server_port,
                http_url=self.http_url,
                http_uri=self.http_uri,
                http_query_string=self.http_query_string,
                http_method=self.http_method,
                http_scheme=self.http_scheme,
                http_protocol=self.http_protocol,
                http_header=self.http_header,
                x_trace_id=self.x_trace_id,
                cookie=self.cookie,
                sql=self.sql,
                user_id=self.user_id,
                created_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                updated_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ).save()

    def get_user_from_auth(self, auth_value):
        auths = IastOverpowerUserAuth.objects.filter(auth_value=auth_value)
        if len(auths) > 0:
            user_token = auths[0].http_query_string
            return user_token
