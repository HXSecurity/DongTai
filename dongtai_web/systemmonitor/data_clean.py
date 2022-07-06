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


class ProfilepostArgsSer(serializers.Serializer):
    clean_time = serializers.TimeField()
    days_before = serializers.IntegerField()
    enable = serializers.BooleanField()


class ProfileEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(summary=_('Get Profile'),
                                 description=_("Get Profile with key"),
                                 tags=[_('Profile')])
    def get(self, request, key):
        profile = IastProfile.objects.filter(key=key).values_list(
            'value', flat=True).first()
        if profile is None:
            return R.failure(
                msg=_("Failed to get {} configuration").format(key))
        return R.success(data={key: profile})

    @extend_schema_with_envcheck(summary=_('Profile modify'),
                                request=ProfilepostArgsSer,
                                 description=_("Modifiy Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request, key):
        if not request.user.is_talent_admin():
            return R.failure(
                msg=_("Current users have no permission to modify"))
        ser = ProfilepostArgsSer(data=request.data)
        try:
            if ser.is_valid(True):
                value = ser.validated_data['value']
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            obj, created = IastProfile.objects.update_or_create(
                {
                    'key': key,
                    'value': value
                }, key=key)
        except Exception as e:
            print(e)
            return R.failure(msg=_("Update {} failed").format(key))
        return R.success(data={key: obj.value})
