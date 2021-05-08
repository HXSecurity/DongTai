#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/18 下午4:07
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_models.models import User
from dongtai_models.models.talent import Talent


class TalentSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()

    class Meta:
        model = Talent
        fields = ['id', 'talent_name', 'create_time', 'update_time', 'created', 'is_active']

    def get_created(self, obj):
        user = User.objects.filter(id=obj.created_by).first()
        return user.get_username()
