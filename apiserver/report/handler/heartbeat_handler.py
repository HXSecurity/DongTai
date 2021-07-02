#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:56
# software: PyCharm
# project: webapi
import base64
import time

from dongtai_models.models.agent import IastAgent
from dongtai_models.models.heartbeat import Heartbeat
from dongtai_models.models.replay_queue import IastReplayQueue
from dongtai_models.models.server import IastServerModel

from apiserver import const
from apiserver.report.handler.report_handler_interface import IReportHandler


class HeartBeatHandler(IReportHandler):

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
        self.agent_name = self.detail.get('agent_name')
        self.project_name = self.detail.get('project_name', 'Demo Project')

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
        env = ""
        envs = []
        self.command = ""
        if self.server_env:
            env = base64.b64decode(self.server_env).decode('utf-8')
            env = env.replace('{', '').replace('}', '')
            envs = env.split(',')
            self.command = self.get_command(envs)

        iast_servers = IastServerModel.objects.filter(
            name=self.web_server_name,
            hostname=self.hostname,
            ip=self.web_server_ip,
            port=self.web_server_port,
            command=self.command
        )

        if len(iast_servers) > 0:
            iast_server = iast_servers[0]
            iast_server.status = 'online'
            iast_server.update_time = int(time.time())
            iast_server.save()
            return iast_server
        else:
            iast_server = IastServerModel(
                name=self.web_server_name,
                hostname=self.hostname,
                ip=self.web_server_ip,
                port=self.web_server_port,
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
            iast_server.save()
            return iast_server

    def get_result(self):
        if self.agent:
            # 根据agent查找项目
            try:
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
                        failure_ids = []
                        replay_requests = list()
                        for replay_request in replay_queryset:
                            if replay_request['uri']:
                                replay_requests.append(replay_request)
                                success_ids.append(replay_request['id'])
                            else:
                                failure_ids.append(replay_request['id'])

                        IastReplayQueue.objects.filter(id__in=success_ids).update(update_time=int(time.time()),
                                                                                  state=const.SOLVING)
                        IastReplayQueue.objects.filter(id__in=failure_ids).update(update_time=int(time.time()),
                                                                                  state=const.SOLVED)
                        return replay_requests
                else:
                    return list()
            except Exception as e:
                return list()
        return list()

    def save(self):
        self.agent = self.get_agent(project_name=self.project_name, agent_name=self.agent_name)
        if self.agent:
            self.agent.is_running = 1
            self.agent.is_core_running = 1
            self.agent.latest_time = int(time.time())
            self.agent.save()
            self.save_heartbeat()
            self.agent.server = self.save_server()
            self.agent.save()
