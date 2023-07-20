######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : commonview
# @created     : 星期五 12月 03, 2021 11:01:55 CST
#
# @description :
######################################################################

from dongtai_common.models.sensitive_info import IastPatternType, IastSensitiveInfoRule
from rest_framework import serializers
from dongtai_common.endpoint import UserEndPoint, R
from rest_framework.serializers import ValidationError


class BatchStatusUpdateSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
    status = serializers.ChoiceField((-1, 0, 1))


class BatchStatusUpdateSerializerView(UserEndPoint):
    serializer = BatchStatusUpdateSerializer
    status_field = ""

    def post(self, request):
        data = self.get_params(request.data)
        self.update_model(request, data)
        return R.success(msg="update success")

    def get_params(self, data):
        ser = self.serializer(data=data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError:
            return {"ids": [], "status": 0}
        return ser.validated_data

    def update_model(self, request, validated_data):
        self.model.objects.filter(
            pk__in=validated_data["ids"], user__in=[request.user]
        ).update(**{self.status_field: validated_data["status"]})


class AllStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField((-1, 0, 1))


class AllStatusUpdateSerializerView(UserEndPoint):
    serializer = AllStatusUpdateSerializer
    status_field = "status"

    def post(self, request):
        data = self.get_params(request.data)
        self.update_model(request, data)
        return R.success(msg="update success")

    def get_params(self, data):
        ser = self.serializer(data=data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError:
            return {"status": 0}
        return ser.validated_data

    def update_model(self, request, validated_data):
        self.model.objects.filter(user__in=[request.user]).update(
            **{self.status_field: validated_data["status"]}
        )
