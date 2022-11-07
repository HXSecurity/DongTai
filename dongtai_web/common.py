
from enum import IntEnum



class VulType(IntEnum):
    APPLICATION = 1
    ASSET = 2

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from dongtai_conf.settings import config
from dongtai_common.models.profile import IastProfile
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.forms.models import model_to_dict
import json
from datetime import datetime
from typing import Type

def get_json_from_iast_profile(key: str,
                               _serializer: Type[serializers.Serializer]) -> dict:
    profile = IastProfile.objects.filter(key=key).values_list(
        'value', flat=True).first()
    profile_data = json.loads(profile) if profile else {}
    return _serializer(data=profile_data).data

def get_data_gather_data() -> dict:
    return {}
