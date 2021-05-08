#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/11/30 下午6:55
# software: PyCharm
# project: lingzhi-webapi
import time

from rest_framework import serializers

from dongtai_models.models.agent import IastAgent


class AgentSerializer(serializers.ModelSerializer):
    USER_MAP = dict()
    SERVER_MAP = dict()
    system_load = serializers.SerializerMethodField()
    running_status = serializers.SerializerMethodField()
    server = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = IastAgent
        fields = ['id', 'token', 'server', 'version', 'running_status', 'system_load', 'owner', 'latest_time',
                  'project_name']

    def get_latest_heartbeat(self, obj):
        try:
            latest_heartbeat = getattr(obj, 'latest_heartbeat')
        except Exception as e:
            latest_heartbeat = obj.heartbeats.values('dt', 'cpu').order_by('-dt').first()
            setattr(obj, 'latest_heartbeat', latest_heartbeat)
        return latest_heartbeat

    def get_running_status(self, obj):
        heartbeat = self.get_latest_heartbeat(obj)
        if heartbeat:
            return "运行中" if (time.time() - heartbeat['dt']) < 60 * 5 else '未运行'
        else:
            return "未运行"

    def get_system_load(self, obj):
        heartbeat = self.get_latest_heartbeat(obj)
        if heartbeat:
            return heartbeat['cpu']
        else:
            return "负载数据暂未上传"

    def get_server(self, obj):
        def get_server_addr():
            if obj.server_id not in self.SERVER_MAP:
                self.SERVER_MAP[obj.server_id] = f'{obj.server.ip}:{obj.server.port}'
            return self.SERVER_MAP[obj.server_id]

        if obj.server_id:
            return get_server_addr()
        return '暂未绑定服务器信息'

    def get_user(self, obj):
        if obj.user_id not in self.USER_MAP:
            self.USER_MAP[obj.user_id] = obj.user.get_username()
        return self.USER_MAP[obj.user_id]

    def get_owner(self, obj):
        return self.get_user(obj)


class ProjectEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastAgent
        fields = ['id', 'token']
