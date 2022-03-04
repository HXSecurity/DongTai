#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import base64
import json
import logging

from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.vulnerablity import IastVulnerabilityStatus
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from iast.serializers.vul import VulSerializer
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers

logger = logging.getLogger('dongtai-webapi')


class _VulDetailResponseDataServerSerializer(serializers.Serializer):
    name = serializers.CharField()
    hostname = serializers.CharField()
    ip = serializers.CharField()
    port = serializers.CharField()
    container = serializers.CharField()
    server_type = serializers.CharField()
    container_path = serializers.CharField()
    runtime = serializers.CharField()
    environment = serializers.CharField()
    command = serializers.CharField()

class _VulDetailResponseDataStrategySerializer(serializers.Serializer):
    desc = serializers.CharField()
    sample_code = serializers.CharField()
    repair_suggestion = serializers.CharField()

class _VulDetailResponseDataVulSerializer(serializers.Serializer):
    url = serializers.CharField()
    uri = serializers.CharField()
    agent_name = serializers.CharField()
    http_method = serializers.CharField()
    type = serializers.CharField()
    taint_position = serializers.CharField()
    first_time = serializers.IntegerField()
    latest_time = serializers.IntegerField()
    project_name = serializers.CharField(help_text=_('The name of project'))
    project_version = serializers.CharField(
        help_text=_("The version name of the project"))
    language = serializers.CharField(
        default=None,
        help_text=_("programming language"))
    level = serializers.CharField(help_text=_("The name of vulnerablity level"))
    level_type = serializers.IntegerField(help_text=_("The id of vulnerablity level"))
    counts = serializers.IntegerField()
    request_header = serializers.CharField()
    response = serializers.CharField()
    graph = serializers.CharField()
    context_path = serializers.CharField()
    client_ip = serializers.CharField()
    status = serializers.CharField()
    taint_value = serializers.CharField()
    param_name = serializers.CharField()
    method_pool_id = serializers.IntegerField()
    project_id = serializers.IntegerField(help_text=_("The id of the project"))


class _VulDetailResponseDataSerializer(serializers.Serializer):
    vul = _VulDetailResponseDataVulSerializer()
    server = _VulDetailResponseDataServerSerializer()
    strategy = _VulDetailResponseDataStrategySerializer()

_ResponseSerializer = get_response_serializer(_VulDetailResponseDataSerializer())

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
                    data_type = _('Source method')
                elif i == method_counts - 1:
                    data_type = _('Hazardous method')
                else:
                    data_type = _('Propagation method')
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
                    'node': f'{class_name}.{method_name}()',
                    'tag': method.get('tag', None),
                    'code': htmlescape(method.get('code', None)),
                })
        except Exception as e:
            logger.error(_('Analysis of errovence analysis of stain call diagram: {}').format(__name__,e))
            results = None
        return results

    @staticmethod
    def parse_request(method, uri, query_param, protocol, header, data):
        _data = f"{method} {uri}?{query_param} {protocol}\n" if query_param else f"{method} {uri} {protocol}\n"
        try:
            _data = _data + (base64.b64decode(header.encode("utf-8")).decode("utf-8") if header else '')
        except Exception as e:
            logger.error(_('Error analysis of Header, error message: {}').format(e))
        if data:
            _data = _data + "\n" + data
        return _data

    @staticmethod
    def parse_response(header, body):
        return '{header}\n\n{body}'.format(header=header, body=body)

    def get_vul(self, auth_agents):
        vul = IastVulnerabilityModel.objects.filter(id=self.vul_id, agent__in=auth_agents).first()
        hook_type = HookType.objects.filter(pk=vul.hook_type_id).first() if vul is not None else None
        hook_type_name = hook_type.name if hook_type else None
        strategy = IastStrategyModel.objects.filter(pk=vul.strategy_id).first()
        strategy_name = strategy.vul_name if strategy else None
        type_ = list(
            filter(lambda x: x is not None, [strategy_name, hook_type_name]))
        vul.type = type_[0] if type_ else ''
        status = IastVulnerabilityStatus.objects.filter(pk=vul.status_id).first()
        vul.status_ = status.name if status else ''
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
            logger.error(_('[{}] Vulnerability information parsing error, error message: {}').format(__name__,e))
            self.server = {}
        self.vul_name = vul.type
        return {
            'url':
            vul.url,
            'uri':
            vul.uri,
            'agent_name':
            agent.token,
            'http_method':
            vul.http_method,
            'type':
            vul.type,
            'taint_position':
            vul.taint_position,
            'first_time':
            vul.first_time,
            'latest_time':
            vul.latest_time,
            'project_name':
            project['name']
            if project else _('The application has not been binded'),
            'project_version':
            project_version_name,
            'language':
            agent.language,
            'level':
            vul.level.name_value,
            'level_type':
            vul.level.id,
            'counts':
            vul.counts,
            'req_header':
            htmlescape(self.parse_request(vul.http_method, vul.uri, vul.req_params,
                               vul.http_protocol, vul.req_header,
                               vul.req_data)) if is_need_http_detail(strategy_name) else '',
            'response':
            htmlescape(self.parse_response(vul.res_header, vul.res_body)) if is_need_http_detail(strategy_name) else '',
            'graph':
            self.parse_graphy(vul.full_stack),
            'context_path':
            vul.context_path,
            'client_ip':
            vul.client_ip,
            'status':
            vul.status_,
            'taint_value':
            vul.taint_value,
            'param_name':
            parse_param_name(vul.param_name) if vul.param_name else {},
            'method_pool_id':
            vul.method_pool_id,
            'project_id':
            project_id,
            'is_need_http_detail': is_need_http_detail(strategy_name),
        }

    def get_strategy(self):

        strategy = IastStrategyModel.objects.filter(
            vul_name=self.vul_name).first()
        if strategy:
            return {
                'desc': strategy.vul_desc,
                'sample_code': '',
                'repair_suggestion': strategy.vul_fix
            }
        else:
            return {'desc': "", 'sample_code': '', 'repair_suggestion': ''}

    @extend_schema_with_envcheck(response_bodys=[{
        'name':
        _('Get data sample'),
        'description':
        _("The aggregation results are programming language, risk level, vulnerability type, project"
          ),
        'value': {
            "status": 201,
            "msg": "success",
            "data": {
                "vul": {
                    "url": "http://localhost:81/captcha/captchaImage",
                    "uri": "/captcha/captchaImage",
                    "agent_name":
                    "Mac OS X-localhost-v1.0.0-d24bf703ca62499ebdd12770708296f5",
                    "http_method": "GET",
                    "type": "Weak Random Number Generation",
                    "taint_position": None,
                    "first_time": 1631089870,
                    "latest_time": 1631089961,
                    "project_name": "demo-4.6.1",
                    "project_version": "V1.0",
                    "language": "JAVA",
                    "level": "LOW",
                    "level_type": 3,
                    "counts": 6,
                    "req_header":
                    "GET /captcha/captchaImage?type=math HTTP/1.1\nhost:localhost:81\nconnection:keep-alive\nsec-ch-ua:\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"\nsec-ch-ua-mobile:?0\nuser-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36\nsec-ch-ua-platform:\"macOS\"\naccept:image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8\nsec-fetch-site:same-origin\nsec-fetch-mode:no-cors\nsec-fetch-dest:image\nreferer:http://localhost:81/login\naccept-encoding:gzip, deflate, br\naccept-language:zh-CN,zh;q=0.9\ncookie:JSESSIONID=4bada2e5-d848-4218-8e24-3b28f765b986\n",
                    "response": "None\n\nNone",
                    "graph": None,
                    "context_path": "127.0.0.1",
                    "client_ip": "127.0.0.1",
                    "status": "Confirmed",
                    "taint_value": None,
                    "param_name": {},
                    "method_pool_id": None,
                    "project_id": 69
                },
                "server": {
                    "name": "server.name",
                    "hostname": "localhost",
                    "ip": "localhost",
                    "port": 81,
                    "container": "Apache Tomcat/9.0.41",
                    "server_type": "apache tomcat",
                    "container_path":
                    "/Users/erzhuangniu/workspace/vul/demo-4.6.1",
                    "runtime": "OpenJDK Runtime Environment",
                    "environment":
                    "java.runtime.name=OpenJDK Runtime Environment, spring.output.ansi.enabled=always, project.name=demo-4.6.1, sun.boot.library.path=/Users/erzhuangniu/Library/Java/JavaVirtualMachines/corretto-1.8.0_292/Contents/Home/jre/lib, java.vm.version=25.292-b10, gop",
                    "command": "com.ruoyi.demoApplication"
                },
                "strategy": {
                    "desc":
                    "Verifies that weak sources of entropy are not used.",
                    "sample_code": "",
                    "repair_suggestion": None
                }
            }
        }
    }],
                                 summary=_('Vulnerability details'),
                                 description=
                                 _('Use the corresponding id of the vulnerability to query the details of the vulnerability'
                                   ),
                                 tags=[_('Vulnerability')],
                                 response_schema=_ResponseSerializer)
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
            logger.error(_('[{}] Vulnerability information parsing error, error message: {}').format(__name__,e))
            return R.failure(msg=_('Vulnerability data query error'))


def htmlescape(string):
    return string.replace(
        '<em>', "6350be97a65823fc42ddd9dc78e17ddf13ff693b").replace(
            '</em>', "4d415116bf74985fbdb232cd954cd40392fbcd69").replace(
                '<',
                '&lt;').replace("4d415116bf74985fbdb232cd954cd40392fbcd69",
                                "</em>").replace(
                                    "6350be97a65823fc42ddd9dc78e17ddf13ff693b",
                                    "<em>")

def is_need_http_detail(name):
    return False if name in ['硬编码'] else True

def parse_param_name(param_name):
    try:
        res = json.loads(param_name)
        return res
    except:
        return {}

if __name__ == '__main__':
    vul = VulDetail()
    graphy = '[{"classname": "org.apache.struts2.dispatcher.StrutsRequestWrapper", "methodname": "getParameter", "in": ", "out": "desc", "stack": "javax.servlet.ServletRequestWrapper.getParameter(ServletRequestWrapper.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "append", "in": "desc", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.append(StringBuilder.java)"}, {"classname": "java.lang.StringBuilder", "methodname": "toString", "in": "select host,user from user where user=+desc order by host ", "out": "select host,user from user where user=+desc order by host ", "stack": "java.lang.StringBuilder.toString(StringBuilder.java)"}, {"classname": "com.mysql.jdbc.JDBC4Connection", "methodname": "prepareStatement", "in": "select host,user from user where user=+desc order by host ", "out": "NULL", "stack": "com.mysql.jdbc.ConnectionImpl.prepareStatement(ConnectionImpl.java)"}]'
    vul.parse_graphy(graphy)
