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

logger = logging.getLogger('dongtai-webapi')


class VulDelete(UserEndPoint):
    name = 'api-v1-vul-delete-<id>'
    description = _('Delete vulnerability')

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
            return R.success(msg=_('successfully deleted'))
        except IastVulnerabilityModel.DoesNotExist as e:
            return R.failure(msg=_('Delete failed, the reason: the vulnerability does not exist'))
        except Exception as e:
            logger.error(f'user_id:{request.user.id} msg:{e}')
            return R.failure(msg=_('failed to delete'))
