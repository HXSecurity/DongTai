#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/27 下午5:00
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_models.models import User
from dongtai_models.models.department import Department


class DepartmentSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'create_time', 'update_time', 'user_count', 'created')

    def get_user_count(self, obj):
        return obj.users.count()

    def get_created(self, obj):
        user = User.objects.filter(id=obj.created_by).first()
        return user.get_username()
