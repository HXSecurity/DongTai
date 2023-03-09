import logging

from dongtai_common.endpoint import UserEndPoint, R

from dongtai_common.utils import const
from dongtai_web.utils import get_model_field
from dongtai_common.models.agent import IastAgent
from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_common.models.dast_integration import IastDastIntegration

logger = logging.getLogger('dongtai-webapi')

class VulRelativeDAST(UserEndPoint):

    def get(self, request, vul_id):
        try:
            if int(vul_id) <= 0:
                return R.failure(msg=_("Can't find relevant data"))
        except Exception as e:
            logger.debug(e, exc_info=e)
            return R.failure(msg=_("Can't find relevant data"))
        dast_integrations = IastDastIntegration.objects.filter(
            vul_id=vul_id).all()
        return R.success(data=[
            model_to_dict(dast_integration)
            for dast_integration in dast_integrations
        ])
