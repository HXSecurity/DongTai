#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/5/22 18:28
# software: PyCharm
# project: webapi

import time

from rest_framework import serializers


from _typeshed import Incomplete
class ErrorlogSerializer(serializers.Serializer):
    errorlog: Incomplete = serializers.CharField()
    state: Incomplete = serializers.CharField()
    dt: Incomplete = serializers.IntegerField(default=int(time.time()))
    agent_app: Incomplete = serializers.CharField()
