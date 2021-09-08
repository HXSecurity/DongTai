#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework.request import Request

from dongtai.endpoint import R
from dongtai.endpoint import UserEndPoint
from dongtai.models.vulnerablity import IastVulnerabilityModel
from django.utils.translation import gettext_lazy as _
import logging
from iast.utils import extend_schema_with_envcheck

logger = logging.getLogger('dongtai-webapi')


class VulDelete(UserEndPoint):
    name = 'api-v1-vul-delete-<id>'
    description = _('Delete vulnerability')

    @extend_schema_with_envcheck(
        summary=_('Vulnerability Delete'),
        tags=[_('Vulnerability')],
        description=_(
            "Delete the corresponding vulnerability by specifying the id"),
    )
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
            return R.success(msg=_('Deleted Successfully'))
        except IastVulnerabilityModel.DoesNotExist as e:
            return R.failure(msg=_('Failed to delete, error message: Vulnerability does not exist'))
        except Exception as e:
            logger.error(f'user_id:{request.user.id} msg:{e}')
            return R.failure(msg=_('Deletion failed'))
