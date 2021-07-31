#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:37
# software: PyCharm
# project: lingzhi-webapi
from dongtai.endpoint import TalentAdminEndPoint, R


class AgentUpgradeOffline(TalentAdminEndPoint):
    name = "api-v1-agent-offline-upgrade"
    description = "离线升级agent"

    def post(self, request):
        file = request.FILES['file']
        status, filename = AgentUpgradeOffline.check_file(file.name)
        if status:
            AgentUpgradeOffline.handle_uploaded_file(filename, file)
            return R.success(msg='上传成功')
        return R.failure(msg=f'不支持{filename}文件')

    @staticmethod
    def handle_uploaded_file(filename, file):
        with open(f'iast/upload/iast-package/{filename}', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

    @staticmethod
    def check_file(filename):
        if filename in ['iast-agent.jar', 'iast-core.jar', 'iast-inject.jar']:
            return True, filename
        return False, filename
