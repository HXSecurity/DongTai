from dongtai_common.utils import const
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.document import IastDocument

from dongtai_common.endpoint import R
from dongtai_common.endpoint import UserEndPoint
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _


class _DocumentArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    language = serializers.CharField(
        default=None, help_text=_("Document's corresponding programming language")
    )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastDocument
        fields = ["id", "title", "url", "language", "weight"]


class ResponseDataSerializer(serializers.Serializer):
    documents = DocumentSerializer(many=True)


_SuccessSerializer = get_response_serializer(ResponseDataSerializer())


class DocumentsEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        [_DocumentArgsSerializer],
        response_schema=_SuccessSerializer,
        summary=_("Get documents"),
        description=_("Get help documentation."),
        tags=[_("Documents")],
    )
    def get(self, request):
        ser = _DocumentArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data["page_size"]
                page = ser.validated_data["page"]
                language = ser.validated_data["language"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q(language=language) if language else Q()
        _, documents = self.get_paginator(
            IastDocument.objects.filter(q).order_by("-weight").all(), page, page_size
        )
        return R.success(
            data={"documents": [model_to_dict(document) for document in documents]}
        )
