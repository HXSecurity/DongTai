#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/30 10:31
# software: PyCharm
# project: webapi
from django.db.models import Q
from dongtai_models.models.agent import IastAgent


class IReportHandler:
    def __init__(self):
        self._report = None
        self._detail = None
        self._user_id = None

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

    def parse(self):
        pass

    def save(self):
        pass

    def handle(self, report, user):
        self.report = report
        self.detail = self.report.get('detail')
        self.agent_token = self.detail.get('agent_name')
        self.user_id = user
        # todo 检查当前用户是否有操作该agent的权限
        self.parse()
        self.save()

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
