from django.shortcuts import render
from dongtai.endpoint import UserEndPoint
from django.db.models import Q
from dongtai.models.sca_maven_db import ScaMavenDb
from rest_framework import serializers
from rest_framework import generics
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from django.utils.translation import gettext_lazy as _
from dongtai.endpoint import R
# Create your views here.


class ScaDBSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField()
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))


class ScaMavenDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScaMavenDb
        fields = '__all__'


class ScaUploadSerializer(ScaMavenDbSerializer):
    language_id = serializers.IntegerField()

    class Meta:
        model = ScaMavenDb
        fields = ScaMavenDbSerializer.Meta.fields
        extra_fields = ['language_id']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(ScaUploadSerializer,
                                self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class SCADBBulkViewSet(UserEndPoint, viewsets.ViewSet):
    @extend_schema_with_envcheck([ScaDBSerializer],
                                 summary=_('Get sca db bulk'),
                                 description=_("Get sca list"),
                                 tags=[_('SCA DB')])
    def list(self, request):
        ser = ScaDBSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = Q(language_id=ser.language_id)
        queryset = ScaMavenDb.objects.filter(q).order_by('-import_from')
        page_summary, page_data = self.get_paginator(queryset, ser.page,
                                                     ser.page_size)
        return R.success(data=ScaDBSerializer(page_data, many=True).data)

    def create(self, request):
        ser = ScaDBSerializer(data=request.data,many=True)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        objs = [ScaMavenDb(**i) for i in ser.data]
        ScaMavenDb.objects.create(objs, ignore_conflicts=True)
        return R.success()

class SCADBViewSet(UserEndPoint, viewsets.ViewSet):
    @extend_schema_with_envcheck([ScaDBSerializer],
                                 summary=_('Get sca db'),
                                 description=_("Get sca list"),
                                 tags=[_('SCA DB')])
    def retrieve(self, request, pk):
        q = Q(pk=pk)
        data = ScaMavenDb.objects.filter(q).first()
        return R.success(data=ScaDBSerializer(data).data)

    def create(self, request):
        ser = ScaDBSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        ScaMavenDb.objects.create(**ser.data)
        return R.success()
