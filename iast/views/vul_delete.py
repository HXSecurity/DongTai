#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/23 下午2:16
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vulnerablity import IastVulnerabilityModel


class VulDelete(UserEndPoint):
    name = 'api-v1-vul-delete-<id>'
    description = '删除漏洞'

    def post(self, request, id):
        """
        :param request:
        :return:
        """
        try:
            IastVulnerabilityModel.objects.get(
                id=id,
                agent_id__in=self.get_auth_agents_with_user(request.user)
            ).delete()
            return R.success(msg='删除成功')
        except IastVulnerabilityModel.DoesNotExist as e:
            return R.failure(msg='删除失败，原因：漏洞不存在')
        except Exception as e:
            return R.failure(msg=f'删除失败，原因：{e}')
