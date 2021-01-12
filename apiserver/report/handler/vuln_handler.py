# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # author:owefsad
# # datetime:2020/10/23 11:55
# # software: PyCharm
# # project: webapi
# import base64
# import json
# import time
#
# from apiserver.models.agent import IastAgent
# from apiserver.models.vul_level import IastVulLevel
# from apiserver.report.handler.report_handler_interface import IReportHandler
#
#
# class BaseVulnHandler(IReportHandler):
#     @staticmethod
#     def create_top_stack(obj):
#         stack = f'{obj["classname"]}.{obj["methodname"]}({obj["in"]})'
#         return stack
#
#     @staticmethod
#     def create_bottom_stack(obj):
#         stack = f'{obj["classname"]}.{obj["methodname"]}("{obj["in"]}")'
#         return stack
#
#     def get_vul_info(self):
#         # 判断 strategy.id 是否在 项目捆绑扫描策略中
#         vul_level = '待定'
#         vul_type = self.vuln_type
#         vul_type_enable = 'disable'
#         proBind = IastAgent.objects.filter(token=self.agent_name).values("bind_project_id").first()
#         if proBind and proBind['bind_project_id']:
#             proInfo = IastProject.objects.filter(id=proBind['bind_project_id']).first()
#             # 通过agent获取项目绑定扫描策略，策略ID
#             if proInfo and proInfo.scan.content:
#                 scan_ids = proInfo.scan.content.split(",")
#                 # 根据用户ID判断获取策略中的漏洞等级
#                 strategy = IastStrategyModel.objects.values('vul_type', 'level', 'state').filter(
#                     vul_type=self.vuln_type,
#                     id__in=scan_ids
#                 ).first()
#                 if strategy:
#                     vul_level = strategy.get('level', 4)
#                     vul_type = strategy.get('vul_type', None)
#                     vul_type_enable = strategy.get('state', 'disable')
#         return vul_level, vul_type, vul_type_enable
#
#     def get_command(self, envs):
#         for env in envs:
#             if 'sun.java.command' in env.lower():
#                 return '='.join(env.split('=')[1:])
#         return ''
#
#     def get_runtime(self, envs):
#         for env in envs:
#             if 'java.runtime.name' in env.lower():
#                 return '='.join(env.split('=')[1:])
#         return ''
#
#     def save_server(self):
#         # 根据服务器信息检查是否存在当前服务器，如果存在，标记为存活，否则，标记为失败
#         env = ""
#         envs = []
#         self.command = ""
#         if self.server_env:
#             env = base64.b64decode(self.server_env).decode('utf-8')
#             env = env.replace('{', '').replace('}', '')
#             envs = env.split(',')
#             self.command = self.get_command(envs)
#
#         iast_servers = IastServerModel.objects.filter(
#             user=self.user_id,
#             name=self.server_name,
#             hostname=self.hostname,
#             ip=self.server_name,
#             port=self.server_port,
#             agent_version=self.agent_version,
#             language=self.language,
#             command=self.command
#         )
#
#         if len(iast_servers) > 0:
#             iast_server = iast_servers[0]
#             iast_server.status = 'online'
#             iast_server.latest_time = int(time.time())
#             iast_server.save()
#             return iast_server
#         else:
#             iast_server = IastServerModel(
#                 user=self.user_id,
#                 name=self.server_name,
#                 hostname=self.hostname,
#                 ip=self.server_name,
#                 port=self.server_port,
#                 environment=env,
#                 agent_version=self.agent_version,
#                 latest_agent_version='',
#                 language=self.language,
#                 path=self.container_path,
#                 status='online',
#                 container=self.container,
#                 container_path=self.container_path,
#                 command=self.command,
#                 runtime=self.get_runtime(envs),
#                 first_time=int(time.time()),
#                 latest_time=int(time.time())
#             )
#             iast_server.save()
#             return iast_server
#
#     def parse(self):
#         self.server_name = self.detail.get('server_name')
#         self.server_port = self.detail.get('server_port')
#         self.server_env = self.detail.get('server_env')
#         self.hostname = self.detail.get('hostname')
#         self.agent_version = self.detail.get('agent_version')
#         self.app_name = self.detail.get('app_name')
#         self.app_path = self.detail.get('app_path')
#         self.http_uri = self.detail.get('http_uri')
#         self.http_url = self.detail.get('http_url')
#         self.http_query_string = self.detail.get('http_query_string')
#         self.http_header = self.detail.get('http_header')
#         self.http_method = self.detail.get('http_method')
#         self.http_scheme = self.detail.get('http_scheme')
#         self.http_secure = self.detail.get('http_secure')
#         self.http_protocol = self.detail.get('http_protocol')
#         self.vuln_type = self.detail.get('vuln_type')
#         self.app_caller = self.detail.get('app_caller')
#         self.language = self.detail.get('language')
#         self.agent_name = self.detail.get('agent_name')
#         self.taint_value = self.detail.get('taint_value')
#         self.taint_position = self.detail.get('taint_position')
#         self.client_ip = self.detail.get('http_client_ip')
#         self.param_name = self.detail.get('param_name')
#         self.container = self.detail.get('container')
#         self.container_path = self.detail.get('container_path')
#
#
# class NormalVulnHandler(BaseVulnHandler):
#     def save(self):
#         #  查漏洞名称对应的漏洞等级，狗咋熬漏洞等级表
#         server = self.save_server()
#         agent = IastAgent.objects.filter(token=self.agent_name).first()
#         if agent:
#             agent.server = server
#             agent.save()
#             vul_level, vul_type, vul_type_enable = self.get_vul_info()
#             # if vul_type_enable == 'enable':
#             #     level = IastVulLevel.objects.filter(id=vul_level).first()
#             #     strategy = IastStrategyModel.objects.filter(vul_type=vul_type).first()
#             #     if level and strategy:
#             #         iast_vuls = IastVulnerabilityModel.objects.filter(
#             #             user=self.user_id,
#             #             type=strategy.vul_name,
#             #             url=self.http_url,
#             #             http_method=self.http_method,
#             #             agent=agent
#             #         )
#             #         if iast_vuls:
#             #             vul = iast_vuls[0]
#             #             vul.req_header = self.http_header
#             #             vul.req_params = self.http_query_string
#             #             vul.counts = iast_vuls[0].counts + 1
#             #             vul.latest_time = int(time.time())
#             #             vul.status = 'reported'
#             #             vul.save()
#             #         else:
#             #             vul = IastVulnerabilityModel(
#             #                 user=self.user_id,
#             #                 type=strategy.vul_name,
#             #                 level=level,
#             #                 url=self.http_url,
#             #                 uri=self.http_uri,
#             #                 http_method=self.http_method,
#             #                 http_scheme=self.http_scheme,
#             #                 http_protocol=self.http_protocol,
#             #                 req_header=self.http_header,
#             #                 req_params=self.http_query_string,
#             #                 req_data='',  # fixme 请求体 数据保存
#             #                 res_header='',  # fixme 响应头，暂时没有，后续补充
#             #                 res_body='',  # fixme 响应体数据
#             #                 agent=agent,
#             #                 context_path=self.app_name,
#             #                 counts=1,
#             #                 status='reported',
#             #                 language=self.language,
#             #                 first_time=int(time.time()),
#             #                 latest_time=int(time.time()),
#             #                 client_ip=self.client_ip
#             #             )
#             #             vul.save()
#
#
# class DynamicVulnHandler(BaseVulnHandler):
#     def save(self):
#         server = self.save_server()
#         #  查漏洞名称对应的漏洞等级，漏洞等级表
#         agent = IastAgent.objects.get(token=self.agent_name)
#         # if agent:
#         #     agent.server = server
#         #     agent.save()
#         #     vul_level, vul_type, vul_type_enable = self.get_vul_info()
#         #     if vul_type_enable == 'enable':
#         #         level = IastVulLevel.objects.get(id=vul_level)
#         #         strategy = IastStrategyModel.objects.filter(vul_type=vul_type).first()
#         #         top_stack = DynamicVulnHandler.create_top_stack(self.app_caller[0])
#         #         bottom_stack = DynamicVulnHandler.create_bottom_stack(self.app_caller[-1])
#         #
#         #         iast_vuls = IastVulnerabilityModel.objects.filter(
#         #             user=self.user_id,
#         #             type=strategy.vul_name,
#         #             url=self.http_url,
#         #             http_method=self.http_method,
#         #             taint_position=self.taint_position,  # 或许补充相关数据
#         #             agent=agent
#         #         )
#         #         if iast_vuls:
#         #             vul = iast_vuls[0]
#         #             vul.req_header = self.http_header
#         #             vul.req_params = self.http_query_string
#         #             # vul.full_stack = json.dumps(self.app_caller, ensure_ascii=False),
#         #             # vul.top_stack = top_stack,
#         #             # vul.bottom_stack = bottom_stack,
#         #             vul.counts = iast_vuls[0].counts + 1
#         #             vul.latest_time = int(time.time())
#         #             vul.status = 'reported'
#         #             vul.save()
#         #         else:
#         #             vul = IastVulnerabilityModel(
#         #                 user=self.user_id,
#         #                 type=strategy.vul_name,
#         #                 level=level,
#         #                 url=self.http_url,
#         #                 uri=self.http_uri,
#         #                 http_method=self.http_method,
#         #                 http_scheme=self.http_scheme,
#         #                 http_protocol=self.http_protocol,
#         #                 req_header=self.http_header,
#         #                 req_params=self.http_query_string,
#         #                 req_data='',  # fixme 请求体 数据保存
#         #                 res_header='',  # fixme 响应头，暂时没有，后续补充
#         #                 res_body='',  # fixme 响应体数据
#         #                 full_stack=json.dumps(self.app_caller, ensure_ascii=False),
#         #                 top_stack=top_stack,
#         #                 bottom_stack=bottom_stack,
#         #                 taint_value=self.taint_value,  # fixme: 污点数据，后续补充
#         #                 taint_position=self.taint_position,  # fixme 增加污点位置
#         #                 agent=agent,
#         #                 context_path=self.app_name,
#         #                 counts=1,
#         #                 status='reported',
#         #                 language=self.language,
#         #                 first_time=int(time.time()),
#         #                 latest_time=int(time.time()),
#         #                 client_ip=self.client_ip,
#         #                 param_name=self.param_name
#         #             )
#         #             vul.save()
