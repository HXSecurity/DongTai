#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/10/23 12:00
# software: PyCharm
# project: webapi
import logging
import requests
import json
import time
from django.utils.translation import gettext_lazy as _
from dongtai_conf import settings
from dongtai_protocol.report.log_service import LogService
from dongtai_common.models.agent import IastAgent

logger = logging.getLogger('dongtai.openapi')


class ReportHandler:
    HANDLERS = {}
    log_service = None
    log_service_disabled = False

    # 注册handler到当前命名空间，后续进行异步处理数据
    @staticmethod
    def handler(reports, user):
        """
        处理上传的报告，如果报告的类型不存在，则忽略本次上传；
        检查用户与agent的权限
        :param reports:
        :return:
        """
        try:
            report_type = reports.get('type')
            # 根据消息类型，转发上报到指定地址
            if report_type == 1:
                isCoreInstalled = reports.get("detail", {}).get("isCoreInstalled", None)
                isCoreRunning = reports.get("detail", {}).get("isCoreRunning", None)
                agentId = reports.get("detail", {}).get("agentId", 0)
                # is_core_running 0 未运行，1运行中，2已卸载
                if isCoreInstalled is None and isCoreRunning is None:
                    pass
                elif isCoreInstalled == 0:
                    is_core_running = 2
                    IastAgent.objects.filter(
                        user=user,
                        id=agentId).update(actual_running_status=2)
                    IastAgent.objects.filter(user=user, id=agentId).update(is_core_running=is_core_running)
                else:
                    if isCoreRunning == 1:
                        is_core_running = 1
                        IastAgent.objects.filter(
                            user=user,
                            id=agentId).update(actual_running_status=1)
                    else:
                        is_core_running = 0
                        IastAgent.objects.filter(
                            user=user,
                            id=agentId).update(actual_running_status=2)

                    IastAgent.objects.filter(user=user, id=agentId).update(is_core_running=is_core_running)
            # web hook
            # req = requests.post(
            #     settings.AGENT_ENGINE_URL.format(user_id=user.id, report_type=report_type),
            #     json=reports,
            #     timeout=60)
            class_of_handler = ReportHandler.HANDLERS.get(report_type)
            if class_of_handler is None:
                if report_type in [1, 81, 33, 36, 17, 18, 97, 37]:
                    logger.error(_('Report type {} handler does not exist').format(report_type))
                return None
            # if report_type == 36:
            #    jsonlogger = logging.getLogger('jsonlogger')
            #    jsonlogger.error('report', extra=reports)
            result = class_of_handler().handle(reports, user)
            return result
        except Exception as e:
            logger.error(e, exc_info=e)
        return None

    @classmethod
    def register(cls, handler_name):

        def wrapper(handler):
            async_send = settings.config.getboolean('task', 'async_send', fallback=False)
            if not async_send:
                cls.log_service_disabled = True
            if cls.log_service is None and not cls.log_service_disabled:
                host = settings.config.get('log_service', 'host')
                port = settings.config.getint('log_service', 'port')
                if not host or not port:
                    logger.error('log service must config host and post')
                    cls.log_service_disabled = True
                srv = LogService(host, port)
                if srv.create_socket():
                    cls.log_service = srv

            logger.info(
                _('Registration report type {} handler {}').format(
                    handler_name, handler.__name__))
            if handler_name not in cls.HANDLERS:
                cls.HANDLERS[handler_name] = handler
            return handler

        return wrapper
