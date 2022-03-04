######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : agent_limit
# @created     : 星期三 10月 20, 2021 12:24:20 CST
#
# @description :
######################################################################



import base64
import logging
import time

from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.server import IastServer
from drf_spectacular.utils import extend_schema
from rest_framework.request import Request
from django.utils.translation import gettext_lazy as _
from dongtai.models.profile import IastProfile
from dongtai.endpoint import OpenApiEndPoint, R

from apiserver.api_schema import DongTaiAuth, DongTaiParameter
from apiserver.decrypter import parse_data
from drf_spectacular.utils import extend_schema
from apiserver.api_schema import DongTaiParameter, DongTaiAuth

logger = logging.getLogger('dongtai.openapi')
from django.forms.models import model_to_dict


class LimitView(OpenApiEndPoint):
    @extend_schema(description='Agent Limit', auth=[DongTaiAuth.TOKEN])
    def get(self, request):
        keys = ['cpu_limit']
        profiles = IastProfile.objects.filter(key__in=keys).all()
        if profiles:
            data = [model_to_dict(profile) for profile in profiles]
        else:
            data = [{'id': 1, 'key': 'cpu_limit', 'value': '60'}]
        return R.success(data=data)
