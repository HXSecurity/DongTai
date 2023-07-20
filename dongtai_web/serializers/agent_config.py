#!/usr/bin/env python

import time

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class AgentConfigSettingSerializer(serializers.Serializer):
    details = serializers.JSONField(
        help_text=_("The details config to the agent."), required=True
    )
    hostname = serializers.CharField(
        help_text=_("The hostname of the agent."),
        max_length=100,
        required=False,
        allow_blank=True,
    )
    ip = serializers.CharField(
        help_text=_("The ip of the agent."),
        max_length=100,
        required=False,
        allow_blank=True,
    )
    port = serializers.IntegerField(
        help_text=_("The port of the agent."), required=False, default=80
    )
    id = serializers.IntegerField(
        help_text=_("The port of the agent."), required=False, default=None
    )
    cluster_name = serializers.CharField(
        help_text=_("The cluster_name of the agent."),
        max_length=255,
        required=False,
        allow_blank=True,
    )
    cluster_version = serializers.CharField(
        help_text=_("The cluster_version of the agent."),
        max_length=100,
        required=False,
        allow_blank=True,
    )
    priority = serializers.IntegerField(
        help_text=_("The priority of the agent."), required=True
    )


class AgentWebHookSettingSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the webHook."), required=False)
    type_id = serializers.IntegerField(
        help_text=_("The type of the webHook."), required=True
    )
    headers = serializers.JSONField(
        help_text=_("The details config to the agent."), required=False
    )
    url = serializers.CharField(
        help_text=_("The cluster_name of the agent."), max_length=255, required=True
    )


class AgentWebHookDelSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text=_("The id of the webHook."), required=True)
