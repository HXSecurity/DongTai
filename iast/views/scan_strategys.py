import logging

from dongtai.endpoint import UserEndPoint, R
from dongtai.utils import const

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.text import format_lazy
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from django.db import connection

from django.db import models
from dongtai.models.strategy import IastStrategyUser
from dongtai.models.user import User
import time
from django.db.models import Q
from dongtai.permissions import TalentAdminPermission
from dongtai.models.project import IastProject
from dongtai.serializers.project import ProjectSerializer

logger = logging.getLogger('dongtai-webapi')


class ScanStrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = IastStrategyUser
        fields = ['id', 'name', 'content', 'user', 'status', 'created_at']


class _ScanStrategyArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))
    name = serializers.CharField(
        default=None,
        required=False,
        help_text=_(
            "The name of the item to be searched, supports fuzzy search."))


class _ProjectSerializer(ProjectSerializer):
    class Meta:
        model = IastProject
        fields = ['id', 'name']


class ScanCreateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.IntegerField(required=True)
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
        description=
        _("Get scan strategy relation projects"
          ),
    )
    def get(self, request, pk):
        ser = _ScanStrategyRelationProjectArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                size = ser.validated_data['size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        user = self.get_auth_users(request.user)
        scan_strategy = IastStrategyUser.objects.filter(pk=pk,
                                                        user__in=user).first()
        projects = IastProject.filter(
            scan=scan_strategy).order_by('-latest_time')[::size]
        return R.success(data=_ProjectSerializer(projects).data)


class ScanStrategyViewSet(UserEndPoint, viewsets.ViewSet):

    permission_classes_by_action = {
        'destory': (TalentAdminPermission, ),
    }

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
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def list(self, request):
        ser = _ScanStrategyArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                name = ser.validated_data['name']
                page = ser.validated_data['page']
                page_size = ser.validated_data['page_size']
        except ValidationError as e:
            return R.failure(data=e.detail)
        users = self.get_auth_users(request.user)
        q = Q(user__in=users) & ~Q(status=-1)
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
        description=
        _("Create ScanStrategy"
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
            ser.validated_data['content'] = ','.join(content)
            obj = IastStrategyUser.objects.create(**ser.validated_data,
                                                  user=request.user)
            return R.success(msg='create success',
                             data=ScanStrategySerializer(obj).data)
        except Exception as e:
            logger.error(e)
            return R.failure()

    @extend_schema_with_envcheck(
        request=ScanCreateSerializer,
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy Update'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def update(self, request, pk):
        ser = ScanCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                name = ser.validated_data['name']
                content = ser.validated_data['content']
                status = ser.validated_data['status']
        except ValidationError as e:
            return R.failure(data=e.detail)
        ser.validated_data['content'] = ','.join(content)
        obj = IastStrategyUser.objects.filter(
            pk=pk).update(**ser.validated_data, latest_time=time.time())
        return R.success(msg='update success')

    @extend_schema_with_envcheck(
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy delete'),
        description=
        _("Get the item corresponding to the user, support fuzzy search based on name."
          ),
    )
    def destory(self, request, pk):
        scan = IastStrategyUser.objects.filter(pk=pk).first()
        if not scan:
            return R.failure(msg='No scan strategy found')
        if checkusing(scan):
            return R.failure(msg='someproject is using this scan strategy')
        try:
            IastStrategyUser.objects.filter(pk=pk).update(status=-1)
            return R.success(msg='delete success')
        except Exception as e:
            logger.error(e)
            return R.failure()

    @extend_schema_with_envcheck(
        tags=[_('ScanStrategy')],
        summary=_('ScanStrategy get'),
        description=_("Get the item with pk"),
    )
    def retrieve(self, request, pk):
        obj = IastStrategyUser.objects.filter(pk=pk, user=request.user).first()
        return R.success(data=ScanStrategySerializer(obj).data)


def checkusing(scanstrategy):
    return IastProject.filter(scan=scanstrategy).exists()
