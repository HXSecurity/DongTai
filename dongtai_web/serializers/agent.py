#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-webapi
import time
from dongtai_common.models.heartbeat import IastHeartbeat

from rest_framework import serializers

from dongtai_common.models.agent import IastAgent
from django.utils.translation import gettext_lazy as _
from dongtai_common.models.agent_method_pool import MethodPool
from collections import defaultdict


class AgentSerializer(serializers.ModelSerializer):
    USER_MAP = dict()
    SERVER_MAP = dict()
    system_load = serializers.SerializerMethodField()
    running_status = serializers.SerializerMethodField()
    server = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    flow = serializers.SerializerMethodField()
    report_queue = serializers.SerializerMethodField()
    method_queue = serializers.SerializerMethodField()
    replay_queue = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()
    register_time = serializers.SerializerMethodField()
    latest_time = serializers.SerializerMethodField()

    class Meta:
        model = IastAgent
        fields = [
            "id",
            "token",
            "server",
            "running_status",
            "system_load",
            "owner",
            "latest_time",
            "project_name",
            "is_core_running",
            "language",
            "flow",
            "is_control",
            "report_queue",
            "method_queue",
            "replay_queue",
            "alias",
            "register_time",
            "startup_time",
            "is_audit",
        ]

    def get_latest_heartbeat(self, obj):
        try:
            latest_heartbeat = getattr(obj, "latest_heartbeat")
        except Exception as heartbeat_not_found:
            latest_heartbeat = (
                obj.heartbeats.values("dt", "cpu").order_by("-dt").first()
            )
            setattr(obj, "latest_heartbeat", latest_heartbeat)
        return latest_heartbeat

    def get_running_status(self, obj):
        mapping = defaultdict(str)
        mapping.update({1: _("Online"), 0: _("Offline")})
        return mapping[obj.online]

    def get_system_load(self, obj):
        """
        :param obj:
        :return:
        """
        heartbeat = self.get_latest_heartbeat(obj)
        if heartbeat:
            return heartbeat["cpu"]
        else:
            return _("Load data is not uploaded")

    def get_server(self, obj):
        def get_server_addr():
            if obj.server_id not in self.SERVER_MAP:
                if obj.server.ip and obj.server.port and obj.server.port != 0:
                    self.SERVER_MAP[
                        obj.server_id
                    ] = f"{obj.server.ip}:{obj.server.port}"
                else:
                    return _("No flow is detected by the probe")
            return self.SERVER_MAP[obj.server_id]

        if obj.server_id:
            return get_server_addr()
        return _("No flow is detected by the probe")

    def get_user(self, obj):
        if obj.user_id not in self.USER_MAP:
            self.USER_MAP[obj.user_id] = obj.user.get_username()
        return self.USER_MAP[obj.user_id]

    def get_owner(self, obj):
        return self.get_user(obj)

    def get_flow(self, obj):
        heartbeat = IastHeartbeat.objects.values("req_count").filter(agent=obj).first()
        return heartbeat["req_count"] if heartbeat else 0

    def get_method_queue(self, obj):
        heartbeat = (
            IastHeartbeat.objects.values("method_queue")
            .filter(agent_id=obj.id)
            .order_by("-dt")
            .first()
        )
        return heartbeat["method_queue"] if heartbeat is not None else 0

    def get_report_queue(self, obj):
        heartbeat = (
            IastHeartbeat.objects.values("report_queue")
            .filter(agent_id=obj.id)
            .order_by("-dt")
            .first()
        )
        return heartbeat["report_queue"] if heartbeat is not None else 0

    def get_replay_queue(self, obj):
        heartbeat = (
            IastHeartbeat.objects.values("replay_queue")
            .filter(agent_id=obj.id)
            .order_by("-dt")
            .first()
        )
        return heartbeat["replay_queue"] if heartbeat is not None else 0

    def get_register_time(self, obj):
        if obj.register_time == 0:
            return obj.latest_time
        return obj.register_time

    def get_alias(self, obj):
        if obj.alias == "":
            return obj.token
        return obj.alias

    def get_latest_time(self, obj):
        latest_heartbeat = (
            obj.heartbeats.values_list("dt", flat=True).order_by("-dt").first()
        )
        if latest_heartbeat:
            return latest_heartbeat
        return obj.latest_time


class ProjectEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastAgent
        fields = ["id", "token", "is_core_running"]


class AgentToggleArgsSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id corresponding to the agent."))
    ids = serializers.CharField(
        help_text=_('The id corresponding to the agent, use"," for segmentation.')
    )


class AgentInstallArgsSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id corresponding to the agent."))
