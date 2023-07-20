import json
from datetime import datetime
from enum import IntEnum

from django.forms.models import model_to_dict
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.profile import IastProfile
from dongtai_conf.settings import config
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class VulType(IntEnum):
    APPLICATION = 1
    ASSET = 2


def get_json_from_iast_profile(
    key: str, _serializer: type[serializers.Serializer]
) -> dict:
    profile = (
        IastProfile.objects.filter(key=key).values_list("value", flat=True).first()
    )
    profile_data = json.loads(profile) if profile else {}
    ser = _serializer(data=profile_data)
    ser.is_valid()
    return dict(ser.data)


def get_data_gather_data() -> dict:
    return {}
