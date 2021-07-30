#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
import base64
import json
import logging

from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityModel

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from iast.serializers.vul import VulSerializer

"""
左侧边栏：
[x] server信息接口
漏洞信息接口
污点流图接口
修复建议接口
[x] 应用信息接口
[x] 运行时环境接口
[x] 环境变量接口

漏洞id -> 应用id -> 应用信息
漏洞ID -> 服务器ID -> 服务器信息接口

服务器信息接口：
- 入参：漏洞ID
- request对象：用户ID
- 漏洞表：服务器ID
- 服务器表：
    - name
    - hostname
    - ip
    - port
    - 中间件
    - 运行时环境
    - 环境变量

应用信息接口
- 入参：漏洞ID
- request对象：用户ID
- 漏洞表：应用ID
- 应用表：
    - name
    - path

漏洞信息接口：
- url
- http请求方法
- 漏洞类型
- 污点位置
- 首次出现时间
- 应用名称
- 语言
- 等级
- 出现次数
- http请求头
- 污点流图

策略接口：
- 漏洞描述
- 请求代码示例
- 修复建议

"""
logger = logging.getLogger('dongtai-webapi')


class VulDetail(UserEndPoint):

    def get_server(self):
        server = self.server
        if server:
            return {
                'name': 'server.name',
                'hostname': server.hostname,
                'ip': server.ip,
                'port': server.port,
                'container': server.container if server.container else 'JavaApplication',
                'server_type': VulSerializer.split_container_name(server.container),
                'container_path': server.container_path,
                'runtime': server.runtime,
                'environment': server.env,
                'command': server.command
            }
        else:
            return {
                'name': "",
                'hostname': "",
                'ip': "",
                'port': "",
                'container': "JavaApplication",
                'server_type': "",
                'container_path': "",
                'runtime': "",
                'environment': "",
                'command': ""
            }

    def parse_graphy(self, graphy):
        """

        :param graphy: [{"classname": "org.apache.struts2.dispatcher.StrutsRequestWrapper", "methodname": "getParameter", "in": ", "out": "desc", "stack": "javax.servlet.ServletRequestWrapper.getParameter(ServletRequestWrapper.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "append", "in": "desc", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.append(StringBuilder.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "toString", "in": "select host,user from user where user=+desc order by host ", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.toString(StringBuilder.java)"}, {"classname": "com.mysql.jdbc.JDBC4Connection", "methodname": "prepareStatement", "in": "select host,user from user where user=+desc order by host ", "out": "NULL", "stack": "com.mysql.jdbc.ConnectionImpl.prepareStatement(ConnectionImpl.java)"}]
        :return:
        """
        import json

        results = []
        try:
            method_note_pool = json.loads(graphy)[0]
            method_counts = len(method_note_pool)
            for i in range(method_counts):
                method = method_note_pool[i]
                class_name = method['originClassName'] if 'originClassName' in method else method['className']
                method_name = method['methodName']
                source = ', '.join([str(_hash) for _hash in method['sourceHash']])
                target = ', '.join([str(_hash) for _hash in method['targetHash']])
                _item = f"{method['callerClass']}.{method['callerMethod']}()"
                filename = method['callerClass']
                line_number = method['callerLineNumber']
                if i == 0:
                    data_type = '污点来源方法'
                elif i == method_counts - 1:
                    data_type = '危险方法'
                else:
                    data_type = '传播方法'
                results.append({
                    'type': data_type,
                    'file': filename,
                    'caller': _item,
                    'line_number': line_number,
                    'class': class_name,
                    'method': method_name,
                    'source': source,
                    'source_value': method.get('sourceValues', None),
                    'target': target,
                    'target_value': method.get('targetValues', None),
                    'node': f'{class_name}.{method_name}()'
                })
        except Exception as e:
            logger.error(f'[{__name__}] 污点调用图解析出错，原因：{e}')
            results = None
        return results

    @staticmethod
    def parse_request(method, uri, query_param, protocol, header, data):
        _data = f"{method} {uri}?{query_param} {protocol}\n" if query_param else f"{method} {uri} {protocol}\n"
        try:
            _data = _data + (base64.b64decode(header.encode("utf-8")).decode("utf-8") if header else '')
        except Exception as e:
            logger.error(f'header解析出错，错误原因：{e}')
        if data:
            _data = _data + "\n" + data
        return _data

    @staticmethod
    def parse_response(header, body):
        try:
            _data = base64.b64decode(header.encode("utf-8")).decode("utf-8")
        except Exception as e:
            _data = ''
            logger.error(f'Response Header解析出错，错误原因：{e}')
        return '{header}\n\n{body}'.format(header=_data, body=body)

    def get_vul(self, auth_agents):
        vul = IastVulnerabilityModel.objects.filter(id=self.vul_id, agent__in=auth_agents).first()

        agent = vul.agent
        project_id = agent.bind_project_id
        if project_id is None or project_id == 0:
            project = None
        else:
            project = IastProject.objects.values("name").filter(id=project_id).first()

        project_version_id = agent.project_version_id
        if project_version_id:
            project_version = IastProjectVersion.objects.values('version_name').filter(id=project_version_id).first()
            if project_version:
                project_version_name = project_version['version_name']
            else:
                project_version_name = ''
        else:
            project_version_name = ''
        try:
            self.server = agent.server
        except Exception as e:
            logger.error(f'[{__name__}] 漏洞信息解析出错，原因：{e}')
            self.server = {}
        self.vul_name = vul.type
        return {
            'url': vul.url,
            'uri': vul.uri,
            'agent_name': agent.token,
            'http_method': vul.http_method,
            'type': vul.type,
            'taint_position': vul.taint_position,
            'first_time': vul.first_time,
            'latest_time': vul.latest_time,
            'project_name': project['name'] if project else '暂未绑定项目',
            'project_version': project_version_name,
            'language': agent.language,
            'level': vul.level.name_value,
            'level_type': vul.level.id,
            'counts': vul.counts,
            'req_header': self.parse_request(vul.http_method, vul.uri, vul.req_params, vul.http_protocol,
                                             vul.req_header,
                                             vul.req_data),
            'response': self.parse_response(vul.res_header, vul.res_body),
            'graph': self.parse_graphy(vul.full_stack),
            'context_path': vul.context_path,
            'client_ip': vul.client_ip,
            'status': vul.status,
            'taint_value': vul.taint_value,
            'param_name': json.loads(vul.param_name) if vul.param_name else {},
            'method_pool_id': vul.method_pool_id,
        }

    def get_strategy(self):
        # todo 暂时策略不允许修改
        strategy = IastStrategyModel.objects.filter(vul_name=self.vul_name).first()
        if strategy:
            return {
                'desc': strategy.vul_desc,
                'sample_code': '',
                'repair_suggestion': strategy.vul_fix
            }
        else:
            return {
                'desc': "",
                'sample_code': '',
                'repair_suggestion': ''
            }

    def get(self, request, id):
        """
        :param request:
        :return:
        """
        self.vul_id = id
        auth_agents = self.get_auth_agents_with_user(request.user)
        try:
            return R.success(
                data={
                    'vul': self.get_vul(auth_agents),
                    'server': self.get_server(),
                    'strategy': self.get_strategy()
                }
            )
        except Exception as e:
            return R.failure(msg=f'漏洞数据查询出错，错误原因：{e}')


if __name__ == '__main__':
    vul = VulDetail()
    graphy = '[{"classname": "org.apache.struts2.dispatcher.StrutsRequestWrapper", "methodname": "getParameter", "in": ", "out": "desc", "stack": "javax.servlet.ServletRequestWrapper.getParameter(ServletRequestWrapper.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "append", "in": "desc", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.append(StringBuilder.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "toString", "in": "select host,user from user where user=+desc order by host ", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.toString(StringBuilder.java)"}, {"classname": "com.mysql.jdbc.JDBC4Connection", "methodname": "prepareStatement", "in": "select host,user from user where user=+desc order by host ", "out": "NULL", "stack": "com.mysql.jdbc.ConnectionImpl.prepareStatement(ConnectionImpl.java)"}]'
    vul.parse_graphy(graphy)
