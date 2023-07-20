#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime:2020/5/22 18:28

import time

from rest_framework import serializers


class ErrorlogSerializer(serializers.Serializer):
    errorlog = serializers.CharField()
    state = serializers.CharField()
    dt = serializers.IntegerField(default=int(time.time()))
    agent_app = serializers.CharField()
