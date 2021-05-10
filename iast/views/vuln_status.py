#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/5/8 下午4:56
# project: dongtai-webapi

# status
from dongtai_models.models.vulnerablity import IastVulnerabilityModel

from base import R
from iast.base.user import UserEndPoint


class VulnStatus(UserEndPoint):
    name = "api-v1-vuln-status"
    description = "修改漏洞状态"

    def post(self, request):
        vul_id = request.data.get('id')
        status = request.data.get('status')
        if vul_id and status:
            vul_model = IastVulnerabilityModel.objects.filter(id=vul_id, agent__in=self.get_auth_agents_with_user(
                request.user)).first()
            vul_model.status = status
            vul_model.save(update_fields=['status'])
            msg = f'漏洞状态修改为{status}'
        else:
            msg = '参数不正确'
        return R.success(msg=msg)
