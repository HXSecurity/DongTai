#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai.models.heartbeat import IastHeartbeat

from rest_framework import serializers

from dongtai.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _

from collections import defaultdict

class AgentSerializer(serializers.ModelSerializer):
    USER_MAP = dict()
    SERVER_MAP = dict()
    system_load = serializers.SerializerMethodField()
    running_status = serializers.SerializerMethodField()
    server = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    flow = serializers.SerializerMethodField()

    class Meta:
        model = IastAgent
        fields = ['id', 'token', 'server', 'running_status', 'system_load', 'owner', 'latest_time', 'project_name',
                  'is_core_running', 'language', 'flow', 'is_control']

    def get_latest_heartbeat(self, obj):
        try:
            latest_heartbeat = getattr(obj, 'latest_heartbeat')
        except Exception as heartbeat_not_found:
            latest_heartbeat = obj.heartbeats.values('dt', 'cpu').order_by('-dt').first()
            setattr(obj, 'latest_heartbeat', latest_heartbeat)
        return latest_heartbeat

    def get_running_status(self, obj):
        mapping = defaultdict(str)
        mapping.update({1: _("Online"), 2: _("Offline")})
        return mapping[obj.online]

    def get_system_load(self, obj):
        """
        :param obj:
        :return:
        """
        heartbeat = self.get_latest_heartbeat(obj)
        if heartbeat:
            return heartbeat['cpu']
        else:
            return _("Load data is not uploaded")

    def get_server(self, obj):
        def get_server_addr():
            if obj.server_id not in self.SERVER_MAP:
                if obj.server.ip and obj.server.port and obj.server.port != 0:
                    self.SERVER_MAP[obj.server_id] = f'{obj.server.ip}:{obj.server.port}'
                else:
                    return _('No flow is detected by the probe')
            return self.SERVER_MAP[obj.server_id]

        if obj.server_id:
            return get_server_addr()
        return _('No flow is detected by the probe')

    def get_user(self, obj):
        if obj.user_id not in self.USER_MAP:
            self.USER_MAP[obj.user_id] = obj.user.get_username()
        return self.USER_MAP[obj.user_id]

    def get_owner(self, obj):
        return self.get_user(obj)

    def get_flow(self, obj):
        heartbeat = IastHeartbeat.objects.values('req_count').filter(agent=obj).first()
        return heartbeat['req_count'] if heartbeat else 0


class ProjectEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastAgent
        fields = ['id', 'token', 'is_core_running']
