import logging

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.utils import const

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework.serializers import ValidationError
from rest_framework import viewsets

from django.db import models
from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_common.models.user import User
import time
from django.db.models import Q
from dongtai_common.permissions import TalentAdminPermission
from dongtai_common.models.project import IastProject
from dongtai_web.serializers.project import ProjectSerializer
from dongtai_web.views.utils.commonview import (
    BatchStatusUpdateSerializerView,
    AllStatusUpdateSerializerView,
)
from dongtai_common.common.utils import disable_cache
from dongtai_engine.common.queryset import load_sink_strategy


logger = logging.getLogger('dongtai-webapi')


class ScanStrategySerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = IastStrategyUser
        fields = ['id', 'name', 'content', 'user', 'status', 'created_at']

    def get_content(self, obj):
        try:
            return [int(i) for i in obj.content.split(',')]
        except Exception as e:
            print(e)
            return []


class _ScanStrategyArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    name = serializers.CharField(
        required=False,
        help_text=_(
            "The name of the item to be searched, supports fuzzy search."))


class _ProjectSerializer(ProjectSerializer):
    class Meta:
        model = IastProject
        fields = ['id', 'name']


class ScanCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.ChoiceField((-1, 0, 1), required=True)
    content = serializers.ListField(child=serializers.IntegerField(),
                                    required=True)


class _ScanStrategyRelationProjectArgsSerializer(serializers.Serializer):
    size = serializers.IntegerField(default=5,
                                    max_value=50,
                                    min_value=1,
                                    required=False,
                                    help_text=_('Number per page'))


class ScanStrategyRelationProject(UserEndPoint):
    @extend_schema_with_envcheck(
        request=ScanCreateSerializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy Relation Projects'),
        description=_("Get scan strategy relation projects"
                      ),
    )
    def get(self, request, pk):
        ser = _ScanStrategyRelationProjectArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                size = ser.validated_data['size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        scan_strategy = IastStrategyUser.objects.filter(pk=pk).first()
        projects = IastProject.objects.filter(
            scan=scan_strategy).order_by('-latest_time')[::size]
        return R.success(data=_ProjectSerializer(projects, many=True).data)


class ScanStrategyViewSet(UserEndPoint, viewsets.ViewSet):

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
        [_ScanStrategyArgsSerializer],
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy List'),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."
                      ),
    )
    def list(self, request):
        ser = _ScanStrategyArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                name = ser.validated_data.get('name', None)
                page = ser.validated_data['page']
                page_size = ser.validated_data['page_size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = ~Q(status=-1)
        if name:
            q = Q(name__icontains=name) & q
        queryset = IastStrategyUser.objects.filter(q).order_by('-created_at')
        if name:
            queryset = queryset.filter(name__icontains=name)
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(data=ScanStrategySerializer(page_data,
                                                     many=True).data,
                         page=page_summary)

    @extend_schema_with_envcheck(
        request=ScanCreateSerializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy Create'),
        description=_("Create ScanStrategy"
                      ),
    )
    def create(self, request):
        ser = ScanCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                name = ser.validated_data['name']
                content = ser.validated_data['content']
                status = ser.validated_data['status']
        except ValidationError as e:
            return R.failure(data=e.detail)
        try:
            ser.validated_data['content'] = ','.join([str(i) for i in content])
            obj = IastStrategyUser.objects.create(**ser.validated_data,
                                                  user=request.user)
            return R.success(msg=_('create success'),
                             data=ScanStrategySerializer(obj).data)
        except Exception as e:
            logger.error(e)
            return R.failure()

    @extend_schema_with_envcheck(
        request=ScanCreateSerializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy Update'),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."
                      ),
    )
    def update(self, request, pk):
        ser = ScanCreateSerializer(data=request.data, partial=True)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        if ser.validated_data.get('content', None):
            ser.validated_data['content'] = ','.join(
                [str(i) for i in ser.validated_data['content']])
        obj = IastStrategyUser.objects.filter(pk=pk).update(
            **ser.validated_data)
        disable_cache(load_sink_strategy, (), kwargs={"scan_id": pk})
        return R.success(msg=_('update success'))

    @extend_schema_with_envcheck(
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy delete'),
        description=_("Get the item corresponding to the user, support fuzzy search based on name."
                      ),
    )
    def destory(self, request, pk):
        scan = IastStrategyUser.objects.filter(pk=pk).first()
        if not scan:
            return R.failure(msg='No scan strategy found')
        if checkusing(scan):
            return R.failure(msg='someproject is using this scan strategy')
        try:
            IastStrategyUser.objects.filter(pk=pk, ).update(status=-1)
            return R.success(msg=_('delete success'))
        except Exception as e:
            logger.error(e)
            return R.failure()

    @extend_schema_with_envcheck(
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy get'),
        description=_("Get the item with pk"),
    )
    def retrieve(self, request, pk):
        obj = IastStrategyUser.objects.filter(pk=pk).first()
        return R.success(data=ScanStrategySerializer(obj).data)


class ScanStrategyBatchView(BatchStatusUpdateSerializerView):
    status_field = 'status'
    model = IastStrategyUser

    @extend_schema_with_envcheck(
        request=BatchStatusUpdateSerializerView.serializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy batch status'),
        description=_("batch update status."),
    )
    def post(self, request):
        data = self.get_params(request.data)
        user = request.user
        data['ids'] = filter_using(data['ids'], [user])
        self.update_model(request, data)
        return R.success(msg=_('update success'))


class ScanStrategyAllView(AllStatusUpdateSerializerView):
    status_field = 'status'
    model = IastStrategyUser

    @extend_schema_with_envcheck(
        request=BatchStatusUpdateSerializerView.serializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy all status'),
        description=_("all update status."),
    )
    def post(self, request):
        data = self.get_params(request.data)
        self.update_model(request, data)
        return R.success(msg=_('update success'))

    def update_model(self, request, validated_data):
        ids = self.model.objects.values_list('id', flat=True).all()
        filter_ids = filter_using(ids, request.user)
        self.model.objects.filter(pk__in=filter_ids,
                                  user__in=[request.user]).update(**{
                                      self.status_field:
                                      validated_data['status']
                                  })


def filter_using(ids, users):
    after_filter_ids = []
    for obj in IastStrategyUser.objects.filter(pk__in=ids, user__in=[users]).all():
        if checkusing(obj):
            continue
        after_filter_ids.append(obj.id)
    return after_filter_ids


def checkusing(scanstrategy):
    return IastProject.objects.filter(scan=scanstrategy).exists()
