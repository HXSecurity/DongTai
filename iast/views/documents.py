from dongtai.utils import const
from dongtai.models.hook_type import HookType
from dongtai.models.strategy import IastStrategyModel
from dongtai.models.document import IastDocument

from dongtai.endpoint import R
from dongtai.utils import const
from dongtai.endpoint import UserEndPoint
from iast.serializers.strategy import StrategySerializer
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
from rest_framework.serializers import ValidationError
from iast.utils import extend_schema_with_envcheck




class DocumentArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20)
    page = serializers.IntegerField(default=1)
    language = serializers.CharField(default=None)


class DocumentsEndpoint(UserEndPoint):
    @extend_schema_with_envcheck([DocumentArgsSerializer])
    def get(self, request):
        ser = DocumentArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
                language = ser.validated_data['language']
        except ValidationError as e:
            return R.failure(data=e.detail)
        if language:
            q = Q(language=language)
        else:
            q = Q()
        _, documents = self.get_paginator(
            IastDocument.objects.filter(q).order_by('-weight').all(), page,
            page_size)
        return R.success(data={
            'documents': [model_to_dict(document) for document in documents]
        })
