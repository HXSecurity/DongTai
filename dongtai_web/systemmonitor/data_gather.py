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


class DataGatherSettingsSer(serializers.Serializer):
    method_pool_max_length = serializers.IntegerField()
    gather_res_body = serializers.BooleanField()


def get_json_from_iast_profile(key: str,
                               _serializer: serializer.Serializer) -> dict:
    profile = IastProfile.objects.filter(key=key).values_list(
        'value', flat=True).first()
    profile_data = json.loads(profile) if profile else {}
    return _serializer(data=profile_data).data


class DataGatherEndpoint(UserEndPoint):

    @extend_schema_with_envcheck(summary=_('Get Profile'),
                                 description=_("Get Profile with key"),
                                 tags=[_('Profile')])
    def get(self, request):
        key = 'data_gather'
        data = get_json_from_iast_profile(key, DataGatherSettingsSer)
        return R.success(data=data)

    @extend_schema_with_envcheck(summary=_('Profile modify'),
                                 request=DataGatherSettingsSer,
                                 description=_("Modifiy Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request):
        ser = DataGatherSettingsSer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        value = json.dumps(ser.data)
        try:
            obj, created = IastProfile.objects.update_or_create(
                {
                    'key': key,
                    'value': value
                }, key=key)
        except Exception as e:
            return R.failure(msg=_("Update {} failed").format(key))
        data = json.loads(value)
        return R.success(data=data)
