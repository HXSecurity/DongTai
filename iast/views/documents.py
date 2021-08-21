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

class DocumentSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=1)
    page = serializers.IntegerField(default=1)
    language = serializers.CharField(default=None)

    def validate_page_size(self, value):
        try:
            print(value)
            value = int(value)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("page_size must be number")
        return value

    def validate_page(self, value):
        try:
            print(value)
            value = int(value)
        except Exception as e:
            print(e)
            raise serializers.ValidationError("page must be number")
        return value

class DocumentsEndpoint(UserEndPoint):
    @extend_schema(parameters=[DocumentSerializer])
    def get(self, request):
        page_size = request.GET.get('page_size', 100)
        page = request.GET.get('page', 1)
        language = request.GET.get('language', None)
        ser = DocumentSerializer(data=request.GET)
        print(ser.is_valid())
        print(ser.validated_data)
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

