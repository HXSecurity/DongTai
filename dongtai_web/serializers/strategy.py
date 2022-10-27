#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
from rest_framework import serializers

from dongtai_common.models.strategy import IastStrategyModel


from _typeshed import Incomplete
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model: Incomplete = IastStrategyModel
        fields: Incomplete = ['id', 'vul_type','vul_fix', 'level_id', 'state', 'vul_name', 'vul_desc', 'dt']
