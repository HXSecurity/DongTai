#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi

# status
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.vulnerablity import IastVulnerabilityStatus

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck


class VulStatus(UserEndPoint):
    name = "api-v1-vuln-status"
    description = _("Modify the vulnerability status")

    @extend_schema_with_envcheck([{
        'name': 'project_id',
        'type': int
    }, {
        'name': 'version_id',
        'type': str
    }])
    def post(self, request):
        vul_id = request.data.get('id')
        status = request.data.get('status')
        if vul_id and status:
            vul_model = IastVulnerabilityModel.objects.filter(
                id=vul_id,
                agent__in=self.get_auth_agents_with_user(
                    request.user)).first()
            status_, iscreate = IastVulnerabilityStatus.objects.get_or_create(
                name=status)
            vul_model.status_id = status_.id
            vul_model.save()
            msg = _('Vulnerability status is modified to {}').format(status)
        else:
            msg = _('Incorrect parameter')
        return R.success(msg=msg)
