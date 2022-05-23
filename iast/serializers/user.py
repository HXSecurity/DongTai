#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai.models import User
from dongtai.models.role import IastRoleUserRelation

class UserSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    talent = serializers.SerializerMethodField()
    role_id = serializers.SerializerMethodField()
    role_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'is_superuser', 'phone', 'talent',
            'department', 'is_active', 'date_joined', 'last_login', 'role_id',
            'role_name'
        ]

    def get_department(self, obj):
        department = obj.department.filter().first()
        return {'name': department.get_department_name(), 'id': department.id} if department else {'name': '', 'id': -1}

    def get_talent(self, obj):
        talent = obj.get_talent()
        return talent.get_talent_name() if talent else ''

    def get_role_id(self, obj):
        rolerelation = IastRoleUserRelation.objects.filter(
            user_id=obj.id).first()
        if rolerelation:
            return rolerelation.role.id

    def get_role_name(self, obj):
        rolerelation = IastRoleUserRelation.objects.filter(
            user_id=obj.id).first()
        if rolerelation:
            return rolerelation.role.name
