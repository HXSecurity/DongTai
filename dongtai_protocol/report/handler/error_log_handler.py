#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 11:54
# software: PyCharm
# project: webapi
import logging

import time

from dongtai_common.models.errorlog import IastErrorlog
from dongtai_common.utils import const

from dongtai_protocol.report.handler.report_handler_interface import IReportHandler
from dongtai_protocol.report.report_handler_factory import ReportHandler
from django.utils.translation import gettext_lazy as _

from _typeshed import Incomplete
logger: Incomplete = logging.getLogger('dongtai.openapi')


@ReportHandler.register(const.REPORT_ERROR_LOG)
class ErrorLogHandler(IReportHandler):
    log: Incomplete
    def __init__(self) -> None:
        super().__init__()
        self.log = None

    def parse(self) -> None:
        self.log = self.detail.get('log')

    def save(self) -> None:
        try:
            IastErrorlog.objects.create(
                errorlog=self.log,
                agent=self.agent,
                state='已上报',
                dt=int(time.time())
            )
            logger.info(_('Error log report saving success'))
        except Exception as e:
            logger.info(_('Error log report saves failed, why: {}').format(e))
