#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午3:13
# software: PyCharm
# project: lingzhi-webapi
import base64
import logging
import time

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion
from dongtai_common.models.server import IastServer
from dongtai_common.models.profile import IastProfile
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from django.utils.translation import gettext_lazy as _
from django.db import transaction
import time
from dongtai_common.endpoint import OpenApiEndPoint, R

import json
from dongtai_protocol.api_schema import DongTaiAuth, DongTaiParameter
from dongtai_protocol.decrypter import parse_data

logger = logging.getLogger('dongtai.openapi')


class AgentRegisterEndPoint(OpenApiEndPoint):
    """
    引擎注册接口
    """
    name = "api-v1-agent-register"
    description = "引擎注册"

    @staticmethod
    def register_agent(token, version, language, project_name, user,
                       project_version):
        project = IastProject.objects.values('id').filter(name=project_name,
                                                          user=user).first()
        is_audit = AgentRegisterEndPoint.get_is_audit()
        if project:
            if project_version:
                project_current_version = project_version
            else:
                project_current_version = IastProjectVersion.objects.filter(
                    project_id=project['id'],
                    current_version=1,
                    status=1
                ).first()
            agent_id = AgentRegisterEndPoint.get_agent_id(
                token, project_name, user, project_current_version.id)
            if agent_id == -1:
                agent_id = AgentRegisterEndPoint.__register_agent(
                    exist_project=True,
                    token=token,
                    user=user,
                    version=version,
                    project_id=project['id'],
                    project_name=project_name,
                    project_version_id=project_current_version.id,
                    language=language,
                    is_audit=is_audit
                )
        else:
            agent_id = AgentRegisterEndPoint.get_agent_id(token=token, project_name=project_name, user=user,
                                                          current_project_version_id=0)
            if agent_id == -1:
                agent_id = AgentRegisterEndPoint.__register_agent(
                    exist_project=False,
                    token=token,
                    user=user,
                    version=version,
                    project_id=0,
                    project_name=project_name,
                    project_version_id=0,
                    language=language,
                    is_audit=is_audit
                )
        return agent_id

    @staticmethod
    def get_is_audit():
        return 1

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

    @staticmethod
    def register_server(agent_id, hostname, network, container_name, server_addr, server_port, cluster_name,cluster_version,
                        server_path, server_env, pid):
        """
        注册server，并关联server至agent
        :param agent_id:
        :param hostname:
        :param network:
        :param container_name:
        :param server_addr:
        :param server_port:
        :param server_path:
        :param server_env:
        :param pid:
        :return:
        """
        agent = IastAgent.objects.filter(id=agent_id).first()
        if agent is None:
            return
        # todo 需要根据不同的语言做兼容
        if server_env:
            env = base64.b64decode(server_env).decode('utf-8')
            env = env.replace('{', '').replace('}', '')
            envs = env.split(',')
            command = AgentRegisterEndPoint.get_command(envs)
        else:
            command = ''
            env = ''
            envs = []

        try:
            port = int(server_port)
        except Exception as e:
            logger.error(_('The server port does not exist, has been set to the default: 0'))
            port = 0

        server_id = agent.server_id

        server = IastServer.objects.filter(id=server_id).first() if server_id else None
        if server:
            server.hostname = hostname
            server.network = network
            server.command = command
            server.ip = server_addr
            server.port = port
            server.pid = pid
            server.env = env
            server.cluster_name = cluster_name
            server.cluster_version = cluster_version
            server.status = 'online'
            server.update_time = int(time.time())
            server.save(update_fields=['hostname', 'command', 'ip', 'port', 'env', 'status', 'update_time', 'cluster_name', 'cluster_version'])
        else:
            server = IastServer.objects.create(
                hostname=hostname,
                ip=server_addr,
                port=port,
                pid=pid,
                network=network,
                env=env,
                path=server_path,
                status='online',
                container=container_name,
                container_path=server_path,
                cluster_name=cluster_name,
                cluster_version=cluster_version,
                command=command,
                runtime=AgentRegisterEndPoint.get_runtime(envs),
                create_time=int(time.time()),
                update_time=int(time.time())
            )
            agent.server_id = server.id
            agent.save(update_fields=['server_id'])
            logger.info(_('Server record creation success'))

    @extend_schema(
        description='Agent Register, Data is Gzip',
        parameters=[
            DongTaiParameter.AGENT_NAME,
            DongTaiParameter.LANGUAGE,
            DongTaiParameter.VERSION,
            DongTaiParameter.PROJECT_NAME,
            DongTaiParameter.HOSTNAME,
            DongTaiParameter.NETWORK,
            DongTaiParameter.CONTAINER_NAME,
            DongTaiParameter.SERVER_ADDR,
            DongTaiParameter.SERVER_PORT,
            DongTaiParameter.SERVER_PATH,
            DongTaiParameter.SERVER_ENV,
            DongTaiParameter.PID,
            DongTaiParameter.AUTO_CREATE_PROJECT,
        ],
        responses=[
            {204: None}
        ],
        methods=['POST']
    )
    def post(self, request: Request):
        try:
            param = parse_data(request.read())
            # param = request.data
            token = param.get('name')
            language = param.get('language')
            version = param.get('version')
            project_name = param.get('projectName', 'Demo Project').strip()
            if not token or not version or not project_name:
                return R.failure(msg="参数错误")
            hostname = param.get('hostname')
            network = param.get('network')
            container_name = param.get('containerName')
            server_addr = param.get('serverAddr')
            server_port = param.get('serverPort')
            server_path = param.get('serverPath')
            server_env = param.get('serverEnv')
            # add by song
            cluster_name = param.get('clusterName', "")
            cluster_version = param.get('clusterVersion', "")
            # end by song
            pid = param.get('pid')
            auto_create_project = param.get('autoCreateProject', 0)
            user = request.user
            version_name = param.get('projectVersion', 'V1.0')
            version_name = version_name if version_name else 'V1.0'
            with transaction.atomic():
                obj, project_created = IastProject.objects.get_or_create(
                    name=project_name,
                    user=request.user,
                    defaults={
                        'scan_id': 5,
                        'agent_count': 0,
                        'mode': '插桩模式',
                        'latest_time': int(time.time())
                    })
                project_version, version_created = IastProjectVersion.objects.get_or_create(
                    project_id=obj.id,
                    version_name=version_name,
                    defaults={
                        'user': request.user,
                        'version_name': version_name,
                        'status': 1,
                        'description': '',
                        'current_version': 0,
                    })
                if version_created:
                    count = IastProjectVersion.objects.filter(
                        project_id=obj.id).count()
                    if count == 1:
                        project_version.current_version = 1
                        project_version.save()
            if project_created:
                logger.info(_('auto create project {}').format(obj.id))
            if version_created:
                logger.info(
                    _('auto create project version {}').format(
                        project_version.id))
            if param.get('projectName', None) and param.get(
                    'projectVersion', None):
                agent_id = self.register_agent(token=token,
                                               project_name=project_name,
                                               language=language,
                                               version=version,
                                               project_version=project_version,
                                               user=user)
            else:
                agent_id = self.register_agent(token=token,
                                               project_name=project_name,
                                               language=language,
                                               version=version,
                                               user=user,
                                               project_version=None)

            self.register_server(
                agent_id=agent_id,
                hostname=hostname,
                network=network,
                container_name=container_name,
                server_addr=get_ipaddress(network)
                if get_ipaddress(network) else server_addr,
                server_port=server_port,
                server_path=server_path,
                cluster_name=cluster_name,
                cluster_version=cluster_version,
                server_env=server_env,
                pid=pid,
            )

            core_auto_start = 0
            if agent_id != -1:
                agent = IastAgent.objects.filter(pk=agent_id).first()
                agent.register_time = int(time.time())
                IastAgent.objects.filter(pk=agent_id).update(
                    register_time=int(time.time()))
                agent.save()
                core_auto_start = agent.is_audit

            return R.success(data={'id': agent_id, 'coreAutoStart': core_auto_start})
        except Exception as e:
            logger.error(e)
            return R.failure(msg="探针注册失败，原因：{reason}".format(reason=e))

    @staticmethod
    def get_agent_id(token, project_name, user, current_project_version_id):
        queryset = IastAgent.objects.values('id').filter(
            token=token,
            project_name=project_name,
            user=user,
            project_version_id=current_project_version_id
        )
        agent = queryset.first()
        if agent:
            queryset.update(is_core_running=1, online=1, is_running=1)
            return agent['id']
        return -1

    @staticmethod
    def __register_agent(exist_project, token, user, version, project_id, project_name, project_version_id, language, is_audit):
        if exist_project:
            IastAgent.objects.filter(token=token, online=1, user=user).update(online=0)
        agent = IastAgent.objects.create(
            token=token,
            version=version,
            latest_time=int(time.time()),
            user=user,
            is_running=1,
            bind_project_id=project_id,
            project_name=project_name,
            control=0,
            is_control=0,
            is_core_running=1,
            online=1,
            project_version_id=project_version_id,
            language=language,
            is_audit=is_audit
        )
        return agent.id


def get_ipaddress(network: str):
    try:
        dic = json.loads(network)
        res = dic[0]['ip']
        for i in dic:
            if i['name'].startswith('en'):
                res = i['ip']
            if i.get("isAddress", 0):
                res = i['ip']
                break
        return res
    except KeyError as e:
        return ''
    except Exception as e:
        logger.error(e, exc_info=True)
        return ''
