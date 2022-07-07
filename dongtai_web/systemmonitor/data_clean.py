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
from django_celery_beat.models import (
    CrontabSchedule,
    PeriodicTask,
)
from dongtai_engine.plugins.data_clean import data_cleanup

class DataCleanSettingsSer(serializers.Serializer):
    clean_time = serializers.TimeField(format="%H:%M:%S")
    days_before = serializers.IntegerField()
    enable = serializers.BooleanField()

class DataCleanDoItNowArgsSer(serializers.Serializer):
    days_before = serializers.IntegerField()

class DataCleanEndpoint(UserEndPoint):

    @extend_schema_with_envcheck(summary=_('Get Profile'),
                                 description=_("Get Profile with key"),
                                 tags=[_('Profile')])
    def get(self, request):
        key = 'data_clean'
        profile = IastProfile.objects.filter(key=key).values_list(
            'value', flat=True).first()
        if profile is None:
            return R.failure(
                msg=_("Failed to get {} configuration").format(key))
        data = json.loads(profile)
        return R.success(data=data)

    @extend_schema_with_envcheck(summary=_('Profile modify'),
                                 request=DataCleanSettingsSer,
                                 description=_("Modifiy Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request):
        ser = DataCleanSettingsSer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        key = 'data_clean'
        datetime_obj = datetime.strptime(ser.data['clean_time'], '%H:%M:%S')
        hour = datetime_obj.hour
        minute = datetime_obj.hour
        enabled = 1 if ser.data['enable'] else 0
        kwargs = {'days': int(ser.data['days_before'])}
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
        PeriodicTask.objects.get_or_create(
            name='data clean functions',  # simply describes this periodic task.
            defaults={
                'crontab': schedule,  # we created this above.
                'enabled': enabled,
                'task':
                'dongtai_engine.plugins.data_clean.data_cleanup',  # name of task.
                'args': json.dumps([]),
                'kwargs': json.dumps(kwargs),
            })
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

class DataCleanDoItNowEndpoint(UserEndPoint):

    @extend_schema_with_envcheck(summary=_('Get Profile'),
                                 request=DataCleanDoItNowArgsSer,
                                 description=_("Get Profile with key"),
                                 tags=[_('Profile')])
    def post(self, request):
        ser = DataCleanDoItNowArgsSer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        data_cleanup.delay(days=ser.data['days_before'])
        return R.success()
