#!/usr/bin/env python

import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Deleted Successfully")), ""),
        ((202, _("Deletion failed")), ""),
    )
)


class VulDelete(UserEndPoint):
    name = "api-v1-vul-delete-<id>"
    description = _("Delete vulnerability")

    @extend_schema_with_envcheck(
        summary=_("Vulnerability Delete"),
        tags=[_("Vulnerability")],
        description=_("Delete the corresponding vulnerability by specifying the id"),
    )
    def post(self, request, id):
        """
        :param request:
        :return:
        """
        try:
            IastVulnerabilityModel.objects.get(
                id=id, agent_id__in=self.get_auth_agents_with_user(request.user)
            ).delete()
            return R.success(msg=_("Deleted Successfully"))
        except IastVulnerabilityModel.DoesNotExist:
            return R.failure(
                msg=_("Failed to delete, error message: Vulnerability does not exist")
            )
        except Exception as e:
            logger.error(f"user_id:{request.user.id} msg:{e}")
            return R.failure(msg=_("Deletion failed"))
