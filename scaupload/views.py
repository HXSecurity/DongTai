from django.shortcuts import render
from dongtai.endpoint import UserEndPoint
from django.db.models import Q
from dongtai.models.sca_maven_db import ScaMavenDb
from rest_framework import serializers
from rest_framework import generics
from rest_framework.serializers import ValidationError
from rest_framework import viewsets
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


class SCADBViewSet(UserEndPoint, viewsets.ViewSet):
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

