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
import time

from dongtai_models.models.strategy import IastStrategyModel
from dongtai_models.models.vul_level import IastVulLevel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from apiserver.report.handler.report_handler_interface import IReportHandler


class BaseVulnHandler(IReportHandler):
    @staticmethod
    def create_top_stack(obj):
        stack = f'{obj["classname"]}.{obj["methodname"]}({obj["in"]})'
        return stack

    @staticmethod
    def create_bottom_stack(obj):
        stack = f'{obj["classname"]}.{obj["methodname"]}("{obj["in"]}")'
        return stack

    def get_vul_info(self, agent):
        vul_level = '待定'
        vul_type = self.vuln_type
        vul_type_enable = 'disable'
        # 根据用户ID判断获取策略中的漏洞等级
        strategy = IastStrategyModel.objects.values('vul_type', 'level', 'state').filter(vul_type=vul_type).first()
        if strategy:
            vul_level = strategy.get('level', 4)
            vul_type = strategy.get('vul_type', None)
            vul_type_enable = strategy.get('state', 'disable')
        return vul_level, vul_type, vul_type_enable

    def get_command(self, envs):
        for env in envs:
            if 'sun.java.command' in env.lower():
                return '='.join(env.split('=')[1:])
        return ''

    def get_runtime(self, envs):
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
        self.http_header = self.detail.get('http_header')
        self.http_method = self.detail.get('http_method')
        self.http_scheme = self.detail.get('http_scheme')
        self.http_secure = self.detail.get('http_secure')
        self.http_protocol = self.detail.get('http_protocol')
        self.vuln_type = self.detail.get('vuln_type')
        self.app_caller = self.detail.get('app_caller')
        self.language = self.detail.get('language')
        self.agent_name = self.detail.get('agent_name')
        self.taint_value = self.detail.get('taint_value')
        self.taint_position = self.detail.get('taint_position')
        self.client_ip = self.detail.get('http_client_ip')
        self.param_name = self.detail.get('param_name')
        self.container = self.detail.get('container')
        self.container_path = self.detail.get('container_path')
        self.project_name = self.detail.get('project_name', 'Demo Project')


class NormalVulnHandler(BaseVulnHandler):
    def save(self):
        #  查漏洞名称对应的漏洞等级，狗咋熬漏洞等级表
        agent = self.get_agent(project_name=self.project_name, agent_name=self.agent_name)
        if agent:
            vul_level, vul_type, vul_type_enable = self.get_vul_info(agent)
            if vul_type_enable == 'enable':
                level = IastVulLevel.objects.filter(id=vul_level).first()
                strategy = IastStrategyModel.objects.filter(vul_type=vul_type).first()
                if level and strategy:
                    iast_vul = IastVulnerabilityModel.objects.filter(
                        type=strategy.vul_name,
                        url=self.http_url,
                        http_method=self.http_method,
                        agent=agent
                    ).first()
                    if iast_vul:
                        iast_vul.req_header = self.http_header
                        iast_vul.req_params = self.http_query_string
                        iast_vul.counts = iast_vul.counts + 1
                        iast_vul.latest_time = int(time.time())
                        iast_vul.status = '已上报'
                        iast_vul.save()
                    else:
                        vul = IastVulnerabilityModel(
                            type=strategy.vul_name,
                            level=level,
                            url=self.http_url,
                            uri=self.http_uri,
                            http_method=self.http_method,
                            http_scheme=self.http_scheme,
                            http_protocol=self.http_protocol,
                            req_header=self.http_header,
                            req_params=self.http_query_string,
                            req_data='',  # fixme 请求体 数据保存
                            res_header='',  # fixme 响应头，暂时没有，后续补充
                            res_body='',  # fixme 响应体数据
                            agent=agent,
                            context_path=self.app_name,
                            counts=1,
                            status='已上报',
                            language=self.language,
                            first_time=int(time.time()),
                            latest_time=int(time.time()),
                            client_ip=self.client_ip
                        )
                        vul.save()
