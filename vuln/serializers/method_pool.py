#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/28 上午11:10
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from vuln.models.agent_method_pool import IastAgentMethodPool


class MethodPoolSerialize(serializers.ModelSerializer):
    class Meta:
        model = IastAgentMethodPool
        fields = ['url', 'uri', 'http_method', 'req_header', 'req_params', 'req_data', 'res_header', 'res_body',
                  'context_path', 'language', 'method_pool', 'clent_ip', 'create_time', 'update_time']
