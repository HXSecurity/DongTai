#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:54
# software: PyCharm
# project: webapi
import time

from apiserver.models.agent import IastAgent
from apiserver.models.errorlog import IastErrorlog
from apiserver.report.handler.report_handler_interface import IReportHandler


class ErrorLogHandler(IReportHandler):

    def parse(self):
        self.app_name = self.detail.get('app_name')
        self.web_server_path = self.detail.get('web_server_path')
        self.log = self.detail.get('log')
        self.agent_name = self.detail.get('agent_name')
        self.project_name = self.detail.get('project_name', 'Demo Project')
        self.language = self.detail.get('language')

    def save(self):
        self.agent = IastAgent.objects.get(token=self.agent_name, project_name=self.project_name, user=self.user_id)

        IastErrorlog(
            errorlog=self.log,
            agent=self.agent,
            state='reported',
            dt=int(time.time())
        ).save()
