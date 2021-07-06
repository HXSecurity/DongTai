#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:56
# software: PyCharm
# project: webapi
import base64
import logging

import time

from dongtai_models.models.agent import IastAgent
from dongtai_models.models.heartbeat import Heartbeat
from dongtai_models.models.replay_queue import IastReplayQueue
from dongtai_models.models.server import IastServerModel
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from apiserver import const
from apiserver.report.handler.report_handler_interface import IReportHandler

logger = logging.getLogger('dongtai.openapi')


class HeartBeatHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.server_env = None
        self.app_name = None
        self.app_path = None
        self.web_server_name = None
        self.web_server_port = None
        self.web_server_version = None
        self.web_server_hostname = None
        self.web_server_ip = None
        self.web_server_path = None
        self.req_count = None
        self.pid = None
        self.hostname = None
        self.cpu = None
        self.memory = None
        self.network = None
        self.disk = None

    def parse(self):
        self.server_env = self.detail.get('server_env')
        self.app_name = self.detail.get('app_name')
        self.app_path = self.detail.get('app_path')
        self.web_server_name = self.detail.get('web_server_name')
        self.web_server_port = self.detail.get('web_server_port')
        self.web_server_version = self.detail.get('web_server_version')
        self.web_server_path = self.detail.get('web_server_path')
        self.web_server_hostname = self.detail.get('web_server_hostname')
        self.web_server_ip = self.detail.get('web_server_ip')
        self.req_count = self.detail.get('req_count')
        self.pid = self.detail.get('pid')
        self.hostname = self.detail.get('hostname')
        self.cpu = self.detail.get('cpu')
        self.memory = self.detail.get('memory')
        self.network = self.detail.get('network')
        self.disk = self.detail.get('disk')

    def save_heartbeat(self):
        Heartbeat.objects.create(
            hostname=self.hostname,
            network=self.network,
            memory=self.memory,
            cpu=self.cpu,
            disk=self.disk,
            pid=self.pid,
            env='',
            req_count=self.req_count,
            dt=int(time.time()),
            agent=self.agent
        )

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

    def save_server(self):
        # 根据服务器信息检查是否存在当前服务器，如果存在，标记为存活，否则，标记为失败
        logger.info(f'服务器信息更新开始')
        env = ""
        envs = []
        self.command = ""
        if self.server_env:
            env = base64.b64decode(self.server_env).decode('utf-8')
            env = env.replace('{', '').replace('}', '')
            envs = env.split(',')
            self.command = self.get_command(envs)

        try:
            port = int(self.web_server_port)
        except Exception as e:
            logger.error(f'服务器端口不存在，已设置为默认值：0')
            port = 0
        iast_server = IastServerModel.objects.filter(
            name=self.web_server_name,
            hostname=self.hostname,
            ip=self.web_server_ip,
            port=port,
            command=self.command
        ).first()

        if iast_server:
            iast_server.status = 'online'
            iast_server.update_time = int(time.time())
            iast_server.save(update_fields=['status', 'update_time'])
            logger.info(f'服务器记录更新成功')
            return iast_server
        else:
            iast_server = IastServerModel.objects.create(
                name=self.web_server_name,
                hostname=self.hostname,
                ip=self.web_server_ip,
                port=port,
                environment=env,
                path=self.web_server_path,
                status='online',
                container=self.web_server_name,
                container_path=self.web_server_path,
                command=self.command,
                runtime=self.get_runtime(envs),
                create_time=int(time.time()),
                update_time=int(time.time())
            )
            logger.info(f'服务器记录创建成功')
            return iast_server

    def get_result(self, msg=None):
        try:
            timestamp = int(time.time())
            project_agents = IastAgent.objects.values('id').filter(bind_project_id=self.agent.bind_project_id)
            if project_agents:
                replay_queryset = IastReplayQueue.objects.values('id', 'relation_id', 'uri', 'method', 'scheme',
                                                                 'header',
                                                                 'params', 'body', 'replay_type').filter(
                    agent_id__in=project_agents,
                    state=const.WAITING)[:10]
                # 读取，然后返回
                if replay_queryset:
                    success_ids = []
                    success_vul_ids = []
                    failure_ids = []
                    failure_vul_ids = []
                    replay_requests = list()
                    for replay_request in replay_queryset:
                        if replay_request['uri']:
                            replay_requests.append(replay_request)
                            success_ids.append(replay_request['id'])
                            if replay_request['replay_type'] == const.VUL_REPLAY:
                                success_vul_ids.append(replay_request['relation_id'])
                        else:
                            failure_ids.append(replay_request['id'])
                            if replay_request['replay_type'] == const.VUL_REPLAY:
                                failure_vul_ids.append(replay_request['relation_id'])

                    IastReplayQueue.objects.filter(id__in=success_ids).update(update_time=timestamp,
                                                                              state=const.SOLVING)
                    IastReplayQueue.objects.filter(id__in=failure_ids).update(update_time=timestamp, state=const.SOLVED)

                    IastVulnerabilityModel.objects.filter(id__in=success_vul_ids).update(
                        latest_time=timestamp,
                        status='验证中'
                    )
                    IastVulnerabilityModel.objects.filter(id__in=failure_vul_ids).update(
                        latest_time=timestamp,
                        status='验证失败'
                    )
                    logger.info(f'重放请求下发成功')
                    return replay_requests
                else:
                    logger.info(f'重放请求不存在')
            else:
                logger.info(f'项目下不存在探针')
        except Exception as e:
            logger.info(f'重放请求查询失败，原因：{e}')
        return list()

    def save(self):
        self.agent.is_running = 1
        self.agent.is_core_running = 1
        self.agent.latest_time = int(time.time())
        self.agent.save(update_fields=['is_running', 'is_core_running', 'latest_time'])
        self.save_heartbeat()
        self.agent.server = self.save_server()
        self.agent.save(update_fields=['server'])
