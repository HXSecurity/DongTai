#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:luzy
# datetime:2021/01/14 下午3:13
# software: PyCharm
# project: lingzhi-webapi

import logging

from core.tasks import update_one_sca
from dongtai.endpoint import R, UserEndPoint

logger = logging.getLogger('dongtai-engine')


class ScaEndPoint(UserEndPoint):
    """
    运行sca
    """
    authentication_classes = []
    permission_classes = []
    name = "api-sca-run"
    description = "运行sca检测，检测组件信息和漏洞"

    def get(self, request):

        try:
            agent_id = request.query_params.get('agent_id')
            package_path = request.query_params.get('package_path')
            package_signature = request.query_params.get('package_signature')
            package_name = request.query_params.get('package_name')
            package_algorithm = request.query_params.get('package_algorithm')

            if all([agent_id, package_path, package_name]) is False:
                return R.failure(msg=f"数据不合法 agent_id:{agent_id}, package_path:{package_path}, package_name:{package_name}")

            self.handler_sca_request(agent_id, package_path, package_signature, package_name, package_algorithm)

            return R.success()
        except Exception as e:
            logger.info(f'[-] SCA任务下发失败，原因：{e}')
            return R.failure(msg=f"{e}")

    @staticmethod
    def handler_sca_request(agent_id, package_path, package_signature, package_name, package_algorithm):
        logger.info(f'[+] 处理SCA请求[{agent_id}, {package_path}, {package_signature}, {package_name}, {package_algorithm}]正在下发扫描任务')
        update_one_sca.delay(agent_id, package_path, package_signature, package_name, package_algorithm)
        logger.info(f'[+] 处理SCA请求[{agent_id}, {package_path}, {package_signature}, {package_name}, {package_algorithm}]任务下发完成')
