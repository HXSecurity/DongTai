#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# datetime:2021/01/14 下午3:13
# software: PyCharm
# project: lingzhi-webapi

import logging

from core.tasks import update_one_sca
from dongtai.endpoint import R, UserEndPoint
from core.web_hook import forward_for_upload
logger = logging.getLogger('dongtai-engine')


class AgentEndPoint(UserEndPoint):
    """
    收集agent流量
    """
    authentication_classes = []
    permission_classes = []
    name = "api-agent-report"
    description = "收集agent上报流量，并转发"

    def post(self, request):

        try:
            user_id = request.query_params.get('user_id')
            report_type = request.query_params.get('report_type')
            report_json = request.data
            if all([user_id, report_type]) is False:
                return R.failure(msg=f"数据不合法 user_id:{user_id}, report_type:{report_type}")
            logger.info(f'[+] web hook 正在下发上报任务')
            forward_for_upload.delay(user_id, report_json, report_type)
            logger.info(f'[+] web hook 上报任务下发完成')
            return R.success()
        except Exception as e:
            logger.info(f'[-] web hook 任务下发失败，原因：{e}')
            return R.failure(msg=f"{e}")

