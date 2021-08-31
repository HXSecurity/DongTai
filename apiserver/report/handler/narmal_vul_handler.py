#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/27 下午2:48
# project: dongtai-openapi

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:55
# software: PyCharm
# project: webapi
import logging

import time

from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vul_level import IastVulLevel
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.utils import const

from AgentServer import settings
from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.handler.saas_method_pool_handler import SaasMethodPoolHandler
from apiserver.report.report_handler_factory import ReportHandler

logger = logging.getLogger('dongtai.openapi')


class BaseVulnHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.server_name = None
        self.server_port = None
        self.server_env = None
        self.hostname = None
        self.agent_version = None
        self.app_name = None
        self.app_path = None
        self.http_uri = None
        self.http_url = None
        self.http_query_string = None
        self.http_header = None
        self.http_method = None
        self.http_scheme = None
        self.http_secure = None
        self.http_protocol = None
        self.vuln_type = None
        self.app_caller = None
        self.taint_value = None
        self.taint_position = None
        self.client_ip = None
        self.param_name = None
        self.container = None
        self.container_path = None

    @staticmethod
    def create_top_stack(obj):
        stack = f'{obj["classname"]}.{obj["methodname"]}({obj["in"]})'
        return stack

    @staticmethod
    def create_bottom_stack(obj):
        stack = f'{obj["classname"]}.{obj["methodname"]}("{obj["in"]}")'
        return stack

    def get_vul_info(self):
        level_id = 0
        vul_type = self.vuln_type
        vul_type_enable = 'disable'
        hook_type_id = 0
        # 根据用户ID判断获取策略中的漏洞等级
        hook_type = HookType.objects.values('id', 'enable').filter(value=vul_type).first()
        if hook_type:
            hook_type_id = hook_type.get('id', 0)
            strategy = IastStrategyModel.objects.values('level_id').filter(hook_type_id=hook_type_id).first()
            level_id = strategy.get('level_id', 4)
            vul_type_enable = hook_type.get('enable', 0)

        return level_id, vul_type, vul_type_enable, hook_type_id

    @staticmethod
    def get_command(envs):
        for env in envs:
            if 'sun.java.command' in env.lower():
                return '='.join(env.split('=')[1:])
        return ''

    @staticmethod
    def get_runtime(envs):
        for env in envs:
            if 'java.runtime.name' in env.lower():
                return '='.join(env.split('=')[1:])
        return ''

    def parse(self):
        self.server_name = self.detail.get('server_name')
        self.server_port = self.detail.get('server_port')
        self.server_env = self.detail.get('server_env')
        self.hostname = self.detail.get('hostname')
        self.agent_version = self.detail.get('agent_version')
        self.app_name = self.detail.get('app_name')
        self.app_path = self.detail.get('app_path')
        self.http_uri = self.detail.get('http_uri')
        self.http_url = self.detail.get('http_url')
        self.http_query_string = self.detail.get('http_query_string')
        self.http_header = self.detail.get('http_req_header')
        self.http_req_data = self.detail.get('http_body')
        self.http_method = self.detail.get('http_method')
        self.http_scheme = self.detail.get('http_scheme')
        self.http_secure = self.detail.get('http_secure')
        self.http_protocol = self.detail.get('http_protocol')
        self.vuln_type = self.detail.get('vuln_type')
        self.app_caller = self.detail.get('app_caller')
        self.taint_value = self.detail.get('taint_value')
        self.taint_position = self.detail.get('taint_position')
        self.client_ip = self.detail.get('http_client_ip')
        self.param_name = self.detail.get('param_name')
        self.container = self.detail.get('container')
        self.container_path = self.detail.get('container_path')
        self.http_replay = self.detail.get('http_replay_request')
        self.http_res_header = self.detail.get('http_res_header')
        self.http_res_body = self.detail.get('http_res_body')


@ReportHandler.register(const.REPORT_VULN_NORNAL)
class NormalVulnHandler(BaseVulnHandler):
    def save(self):
        if self.http_replay:
            return

        level_id, vul_type, vul_type_enable, hook_type_id = self.get_vul_info()
        if vul_type_enable == 0:
            return
        iast_vul = IastVulnerabilityModel.objects.filter(
            hook_type_id=hook_type_id,
            url=self.http_url,
            http_method=self.http_method,
            agent=self.agent
        ).first()

        if iast_vul:
            iast_vul.req_header = self.http_header
            iast_vul.req_params = self.http_query_string
            iast_vul.counts = iast_vul.counts + 1
            iast_vul.latest_time = int(time.time())
            iast_vul.status_id = settings.CONFIRMED
            iast_vul.save()
        else:
            IastVulnerabilityModel.objects.create(
                hook_type_id=hook_type_id,
                level_id=level_id,
                url=self.http_url,
                uri=self.http_uri,
                http_method=self.http_method,
                http_scheme=self.http_scheme,
                http_protocol=self.http_protocol,
                req_header=self.http_header,
                req_params=self.http_query_string,
                req_data=self.http_req_data,
                res_header=self.http_res_header,
                res_body=self.http_res_body,
                agent=self.agent,
                context_path=self.app_name,
                counts=1,
                status_id=settings.CONFIRMED,
                first_time=int(time.time()),
                latest_time=int(time.time()),
                client_ip=self.client_ip
            )
