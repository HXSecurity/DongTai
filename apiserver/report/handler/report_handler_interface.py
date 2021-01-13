#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/30 10:31
# software: PyCharm
# project: webapi

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
