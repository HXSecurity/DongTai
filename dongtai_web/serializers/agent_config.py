#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh

import time

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


from _typeshed import Incomplete
class AgentConfigSettingSerializer(serializers.Serializer):

    details: Incomplete = serializers.JSONField(help_text=_('The details config to the agent.'), required=True)
    hostname: Incomplete = serializers.CharField(help_text=_('The hostname of the agent.'), max_length=100, required=False, allow_blank=True)
    ip: Incomplete = serializers.CharField(help_text=_('The ip of the agent.'), max_length=100, required=False, allow_blank=True)
    port: Incomplete = serializers.IntegerField(help_text=_('The port of the agent.'), required=False, default=80)
    id: Incomplete = serializers.IntegerField(help_text=_('The port of the agent.'), required=False, default=None)
    cluster_name: Incomplete = serializers.CharField(help_text=_('The cluster_name of the agent.'), max_length=255,required=False, allow_blank=True)
    cluster_version: Incomplete = serializers.CharField(help_text=_('The cluster_version of the agent.'), max_length=100,required=False, allow_blank=True)
    priority: Incomplete = serializers.IntegerField(help_text=_('The priority of the agent.'), required=True)


class AgentWebHookSettingSerializer(serializers.Serializer):

    id: Incomplete = serializers.IntegerField(help_text=_('The id of the webHook.'), required=False)
    type_id: Incomplete = serializers.IntegerField(help_text=_('The type of the webHook.'), required=True)
    headers: Incomplete = serializers.JSONField(help_text=_('The details config to the agent.'), required=False)
    url: Incomplete = serializers.CharField(help_text=_('The cluster_name of the agent.'), max_length=255, required=True)


class AgentWebHookDelSerializer(serializers.Serializer):

    id: Incomplete = serializers.IntegerField(help_text=_('The id of the webHook.'), required=True)
