#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/30 10:31
# software: PyCharm
# project: webapi
import logging

from django.db.models import Q
from dongtai_models.models.agent import IastAgent

logger = logging.getLogger('dongtai.openapi')


class IReportHandler:
    def __init__(self):
        self._report = None
        self._detail = None
        self._user_id = None
        self.agent_name = None
        self.project_name = None
        self.language = None
        self.agent = None

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, reports):
        self._report = reports

    @property
    def detail(self):
        return self._detail

    @detail.setter
    def detail(self, detail):
        self._detail = detail

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    def common_header(self):
        self.detail = self.report.get('detail')
        self.agent_name = self.detail.get('agent_name')
        self.project_name = self.detail.get('project_name', 'Demo Project')
        self.language = self.detail.get('language', 'JAVA')

    def has_permission(self):
        self.agent = self.get_agent(project_name=self.project_name, agent_name=self.agent_name)
        return self.agent

    def parse(self):
        pass

    def save(self):
        pass

    def get_result(self, msg=None):
        return msg if msg else ''

    def handle(self, report, user):
        logger.info('报告解析开始')
        self.report = report
        self.user_id = user
        self.common_header()
        if self.has_permission():
            self.parse()
            self.save()
            logger.info('报告解析完成')
            return self.get_result()
        else:
            logger.info('报告解析失败，Agent不存在或无权访问')
            return self.get_result(msg='no permission')

    def get_project_agents(self, agent):
        if agent.bind_project_id != 0:
            agents = IastAgent.objects.filter(
                Q(project_name=self.project_name) | Q(bind_project_id=agent.bind_project_id), online=1,
                user=self.user_id)
        else:
            agents = IastAgent.objects.filter(project_name=self.project_name, user=self.user_id)
        return agents

    def get_agent(self, agent_name, project_name):
        return IastAgent.objects.filter(token=agent_name, project_name=project_name, online=1,
                                        user=self.user_id).first()
