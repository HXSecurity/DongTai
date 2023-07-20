#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_common.models import User
from dongtai_common.models.talent import Talent


class TalentSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()

    class Meta:
        model = Talent
        fields = [
            "id",
            "talent_name",
            "create_time",
            "update_time",
            "created",
            "is_active",
        ]

    def get_created(self, obj):
        user = User.objects.filter(id=obj.created_by).first()
        return user.get_username()
