#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh

import time

from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class AgentConfigSettingSerializer(serializers.Serializer):
    # USER_MAP = dict()
    # details = dict()
    details = serializers.JSONField(help_text=_('The details config to the agent.'))
    hostname = serializers.CharField(help_text=_('The hostname of the agent.'), max_length=100)
    ip = serializers.CharField(help_text=_('The ip of the agent.'), max_length=100)
    port = serializers.IntegerField(help_text=_('The port of the agent.'))
    cluster_name = serializers.CharField(help_text=_('The cluster_name of the agent.'), max_length=255)
    cluster_version = serializers.CharField(help_text=_('The cluster_version of the agent.'), max_length=100)
    priority = serializers.IntegerField(help_text=_('The priority of the agent.'))



