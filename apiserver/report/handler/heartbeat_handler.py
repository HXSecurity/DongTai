#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:56
# software: PyCharm
# project: webapi
import time

from apiserver.models.agent import IastAgent
from apiserver.models.heartbeat import IastHeartbeat
from apiserver.report.handler.report_handler_interface import IReportHandler


class HeartBeatHandler(IReportHandler):

    def parse(self):
        self.web_server_name = self.detail.get('web_server_name')
        self.web_server_port = self.detail.get('web_server_port')
        self.web_server_version = self.detail.get('web_server_version')
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

    def save(self):
        self.agent = IastAgent.objects.get(token=self.agent_name, user=self.user_id)
        self.agent.is_running = 1
        self.agent.save()
        heartbeat = IastHeartbeat(
            user=self.user_id,
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
        heartbeat.save()
