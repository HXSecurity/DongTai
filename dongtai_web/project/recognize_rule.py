from dongtai_common.utils import const
import logging

from dongtai_common.endpoint import R
from dongtai_common.utils import const
from dongtai_common.endpoint import UserEndPoint
from django.forms.models import model_to_dict
from django.db.models import Q
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework.viewsets import ViewSet
from django.utils.translation import gettext_lazy as _
from django.db import models
from dongtai_common.models.recognize_rule import (
    IastRecognizeRule,
    RuleTypeChoices,
)

logger = logging.getLogger('dongtai-webapi')


class DeleteTypeChoices(models.IntegerChoices):
    ALL = 1
    BATCH = 2

class RecognizeRuleListSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    project_id = serializers.IntegerField(help_text=_('Page index'),
                                          required=True)
    rule_type = serializers.ChoiceField(
        help_text=_('Rule type'),
        required=True,
        choices=RuleTypeChoices,
    )


class RecognizeRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = IastRecognizeRule
        fields = ['rule_detail', 'rule_type', 'pk']


class RecognizeRuleCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField(help_text=_('project id'),
                                          required=True)

    class Meta:
        model = IastRecognizeRule
        fields = ['project_id', 'rule_detail', 'rule_type']


class RecognizeRuleBatchDeleteSerializer(serializers.Serializer):
    rule_type = serializers.ChoiceField(
        help_text=_('Rule type'),
        required=True,
        choices=RuleTypeChoices,
    )
    delete_type = serializers.ChoiceField(
        help_text=_('Delete Type'),
        required=True,
        choices=DeleteTypeChoices,
    )
    project_id = serializers.IntegerField(help_text=_('project id'),
                                          required=True)
    delete_ids = serializers.ListField(
        child=serializers.IntegerField(required=True, ),
        help_text=_('Delete Type'),
        required=False,
        default=[],
    )


class RecognizeRuleViewSet(UserEndPoint, ViewSet):

    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            return [
                permission() for permission in
                self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [RecognizeRuleListSerializer],
        tags=[_('RecognizeRule')],
        summary=_('RecognizeRule List'),
    )
    def list(self, request):
        ser = RecognizeRuleListSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q()
        if ser.validated_data['project_id']:
            q = q & Q(project_id=ser.validated_data['project_id'])
        if ser.validated_data['rule_type']:
            q = q & Q(rule_type=ser.validated_data['rule_type'])
        queryset = IastRecognizeRule.objects.filter(q).order_by('-updated')
        page_summary, page_data = self.get_paginator(
            queryset, ser.validated_data['page'],
            ser.validated_data['page_size'])
        return R.success(data=RecognizeRuleSerializer(page_data,
                                                      many=True).data,
                         page=page_summary)

    @extend_schema_with_envcheck(
        request=RecognizeRuleCreateSerializer,
        tags=[_('RecognizeRule')],
        summary=_('RecognizeRule Create'),
        description=_("Create RecognizeRule"),
    )
    def create(self, request):
        ser = RecognizeRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            obj = IastRecognizeRule.objects.create(**ser.validated_data, )
            return R.success(msg=_('create success'),
                             data=RecognizeRuleSerializer(obj).data)
        except Exception as e:
            logger.error(e)
            return R.failure()

    @extend_schema_with_envcheck(
        request=RecognizeRuleCreateSerializer,
        tags=[_('RecognizeRule')],
        summary=_('RecognizeRule Update'),
    )
    def update(self, request, pk):
        ser = RecognizeRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        obj = IastRecognizeRule.objects.filter(pk=pk).update(
            **ser.validated_data)
        return R.success(msg=_('update success'))

    @extend_schema_with_envcheck(
        request=RecognizeRuleBatchDeleteSerializer,
        tags=[_('RecognizeRule')],
        summary=_('RecognizeRule delete'),
    )
    def destory(self, request):
        """
        Example:

        -------------------------
        {
            "delete_type":1,
            "project_id":1
        }
        -------------------------
        {
            "delete_type":2,
            "project_id":1,
            "delete_ids": [1,2,3]
        }
        ------------------------
        """
        ser = RecognizeRuleBatchDeleteSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        if ser.validated_data['delete_type'] == DeleteTypeChoices.ALL:
            IastRecognizeRule.objects.filter(
                project_id=ser.validated_data['project_id'],
                rule_type=ser.validated_data['rule_type'],
            ).delete()
        else:
            IastRecognizeRule.objects.filter(
                project_id=ser.validated_data['project_id'],
                pk__in=ser.validated_data['delete_ids'],
                rule_type=ser.validated_data['rule_type'],
            ).delete()
        return R.success(msg=_('delete success'))

    @extend_schema_with_envcheck(
        tags=[_('RecognizeRule')],
        summary=_('RecognizeRule get'),
        description=_("Get the item with pk"),
    )
    def retrieve(self, request, pk):
        obj = IastRecognizeRule.objects.filter(pk=pk).first()
        return R.success(data=RecognizeRuleSerializer(obj).data)
