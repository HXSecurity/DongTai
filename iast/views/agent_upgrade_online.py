#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/25 下午2:37
# software: PyCharm
# project: lingzhi-webapi
from urllib.parse import urljoin

import requests
from rest_framework.request import Request

from base import R
from iast.base.user import TalentAdminEndPoint
from dongtai_models.models import User


# 在线更新如何设计？
class AgentUpgradeOnline(TalentAdminEndPoint):
    name = "api-v1-agent-install"
    description = "在线升级agent"

    def post(self, request: Request):
        url = request.data['url']
        token = request.data['token']
        try:
            self.download(url, token)
            User.objects.filter(id=request.user.id).update(upgrade_url=url)
            return R.success(msg='在线升级成功')
        except Exception as e:
            return R.failure(msg='token验证失败，请确认输入的地址和token是正确的')

    # 暂未使用
    def token_verify(self, url, token):
        req_url = urljoin(url, 'token/verify')
        resp = requests.get(req_url, headers={'Authorization': f'Token {token}'})
        return (resp.status_code == 200 and resp.json()['status'] == 201)

    def download(self, url, token):
        headers = {'Authorization': f'Token {token}'}
        resp = requests.get(url=urljoin(url, "iast-agent.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-agent.jar", 'wb') as f:
            f.write(resp.content)

        resp = requests.get(url=urljoin(url, "iast-inject.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-inject.jar", 'wb') as f:
            f.write(resp.content)

        resp = requests.get(url=urljoin(url, "iast-core.jar"), headers=headers)
        with open("iast/upload/iast-package/iast-core.jar", 'wb') as f:
            f.write(resp.content)
