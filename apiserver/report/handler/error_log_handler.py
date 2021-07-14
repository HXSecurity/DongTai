#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:54
# software: PyCharm
# project: webapi
import logging

import time

from dongtai.models.errorlog import IastErrorlog
from dongtai.utils import const

from apiserver.report.handler.report_handler_interface import IReportHandler
from apiserver.report.report_handler_factory import ReportHandler

logger = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_ERROR_LOG)
class ErrorLogHandler(IReportHandler):
    def __init__(self):
        super().__init__()
        self.log = None

    def parse(self):
        self.log = self.detail.get('log')

    def save(self):
        try:
            IastErrorlog.objects.create(
                errorlog=self.log,
                agent=self.agent,
                state='已上报',
                dt=int(time.time())
            )
            logger.info('错误日志报告保存成功')
        except Exception as e:
            logger.info('错误日志报告保存失败，原因：%s', e)
