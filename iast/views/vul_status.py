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
from iast.utils import extend_schema_with_envcheck, get_response_serializer
import logging

logger = logging.getLogger('dongtai-webapi')

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('Vulnerability status is modified to {}')), ''),
    ((202, _('Incorrect parameter')), ''),
))

class VulStatus(UserEndPoint):
    name = "api-v1-vuln-status"
    description = _("Modify the vulnerability status")

    @extend_schema_with_envcheck(
        [],
        [
            {
                'name': _("Update with status_id"),
                "description":
                _("Update vulnerability status with status id."),
                'value': {
                    'id': 1,
                    'status_id': 1
                },
            },
            {
                'name': _("Update with status name(Not recommended)"),
                "description":
                _("Update vulnerability status with status name."),
                'value': {
                    'id': 1,
                    'status': "str"
                },
            },
        ],
        [{
            'name':
            _('Get data sample'),
            'description':
            _("The aggregation results are programming language, risk level, vulnerability type, project"
              ),
            'value': {
                "status": 201,
                "msg": "Vulnerability status is modified to Confirmed"
            }
        }],
        tags=[_('Vulnerability')],
        summary=_("Vulnerability Status Modify"),
        description=_("""Modify the vulnerability status of the specified id. 
        The status is specified by the following two parameters. 
        Status corresponds to the status noun and status_id corresponds to the status id. 
        Both can be obtained from the vulnerability status list API, and status_id is preferred."""
                      ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        vul_id = request.data.get('id')
        status = request.data.get('status', None)
        status_id = request.data.get('status_id', None)
        if vul_id and (status or status_id):
            auth_users = self.get_auth_users(request.user)
            auth_agents = self.get_auth_agents(auth_users)
            vul_model = IastVulnerabilityModel.objects.filter(
                id=vul_id,
                agent__in=auth_agents).first()
            if status_id:
                try:
                    status_ = IastVulnerabilityStatus.objects.get(status_id)
                except Exception as e:
                    logger.error(e)
                    print(e)
            else:
                status_, iscreate = IastVulnerabilityStatus.objects.get_or_create(
                    name=status)
            try:
                vul_model.status_id = status_.id
                vul_model.save(update_fields=['status_id'])
                msg = _('Vulnerability status is modified to {}').format(
                    status)
                return R.success(msg=msg)
            except Exception as e:
                print(e)
                pass
        msg = _('Incorrect parameter')
        return R.failure(msg=msg)
