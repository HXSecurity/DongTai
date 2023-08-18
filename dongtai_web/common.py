import json
from enum import IntEnum

from rest_framework import serializers

from dongtai_common.models.profile import IastProfile


class VulType(IntEnum):
    APPLICATION = 1
    ASSET = 2


def get_json_from_iast_profile(key: str, _serializer: type[serializers.Serializer]) -> dict:
    profile = IastProfile.objects.filter(key=key).values_list("value", flat=True).first()
    profile_data = json.loads(profile) if profile else {}
    ser = _serializer(data=profile_data)
    ser.is_valid()
    return dict(ser.data)
