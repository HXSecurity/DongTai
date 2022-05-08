#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
import time

from dongtai.endpoint import UserEndPoint, R
from dongtai.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from iast.serializers.agent_config import AgentConfigSettingSerializer
from rest_framework.serializers import ValidationError

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The setting is complete')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class AgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-threshold-config-setting"
    description = _("config Agent")

    def create_agent_config(self,user, details, hostname, ip, port, cluster_name, cluster_version, priority,id):
        try:

            timestamp = int(time.time())
            if id:
                strategy = IastAgentConfig.objects.filter(user=user,id=id).order_by("-create_time").first()
            else:
                strategy = IastAgentConfig.objects.filter(user=user, id=id).order_by("-create_time").first()
            if strategy:
                strategy.details = details
                strategy.hostname = hostname
                strategy.ip = ip
                strategy.port = port
                strategy.cluster_name = cluster_name
                strategy.cluster_version = cluster_version
                strategy.priority = priority
            else:
                strategy = IastAgentConfig(
                    user=user,
                    details=details,
                    hostname=hostname,
                    ip=ip,
                    port=port,
                    cluster_name=cluster_name,
                    cluster_version=cluster_version,
                    priority=priority,
                    create_time=timestamp
                )
            strategy.save()
            return strategy
        except Exception as e:

            return None

    @extend_schema_with_envcheck(
        tags=[_('Agent')],
        summary=_('Agent threshold Config'),
        description=_("Configure agent disaster recovery strategy"),
        response_schema=_ResponseSerializer)
    def post(self, request):

        ser = AgentConfigSettingSerializer(data=request.data)
        user = request.user
        try:
            if ser.is_valid(True):
                details = ser.validated_data.get('details', {})
                hostname = ser.validated_data.get('hostname', "").strip()
                ip = ser.validated_data.get('ip', "")
                id = ser.validated_data.get('id', "")
                port = ser.validated_data.get('port', 80)
                cluster_name = ser.validated_data.get('cluster_name', "").strip()
                cluster_version = ser.validated_data.get('cluster_version', "")
                priority = ser.validated_data.get('priority', 0)

        except ValidationError as e:

            return R.failure(data=e.detail)

        config = self.create_agent_config(user, details, hostname, ip, port, cluster_name, cluster_version, priority,id)
        if config:
            return R.success(msg=_('保存成功'))
        else:
            return R.failure(msg=_('保存失败'))


from rest_framework import serializers
from django.db.models import IntegerChoices
from rest_framework import viewsets
from dongtai.models.agent_config import (
    IastCircuitTarget,
    IastCircuitConfig,
    IastCircuitMetric,
    TargetType,
    Operator,
    DealType,
    MetricType,
    MetricGroup,
)
from collections.abc import Iterable


class AgentConfigSettingV2TargetSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(TargetType.choices)
    opt = serializers.ChoiceField(Operator.choices)
    value = serializers.CharField()


class AgentConfigSettingV2MetricSerializer(serializers.Serializer):
    metric_type = serializers.ChoiceField(MetricType.choices)
    opt = serializers.ChoiceField(Operator.choices)
    value = serializers.CharField()


class AgentConfigSettingV2Serializer(serializers.Serializer):
    name = serializers.CharField()
    targets = serializers.ListField(
        child=AgentConfigSettingV2TargetSerializer())
    metric_group = serializers.ChoiceField(MetricGroup.choices)
    metrics = serializers.ListField(
        child=AgentConfigSettingV2MetricSerializer())
    interval = serializers.IntegerField()
    deal = serializers.ChoiceField(DealType.choices)
    is_enable = serializers.ChoiceField(DealType.choices)


from django.db.models import Max


def get_priority_now() -> int:
    res = IastCircuitConfig.objects.all().aggregate(Max("priority"))
    return res["priority__max"] + 1

def config_create(data, user):
    fields = ('name', 'metric_group', 'is_enable', 'deal',
              "interval")
    filted_data = get_data_from_dict_by_key(data, fields)
    metric_types = get_metric_types(data['metrics'])
    targets = get_targets(data['targets'])
    obj = IastCircuitConfig.objects.create(**filted_data,
                                           metric_types=metric_types,
                                           targets=targets,
                                           user=user)
    for i in data['targets']:
        create_target(i, obj)

    for i in data['metrics']:
        create_metric(i, obj)


def config_update(data, config_id):
    fields = ('name', 'metric_group', 'is_enable',  'deal',
              "interval")
    filted_data = get_data_from_dict_by_key(data, fields)
    metric_types = get_metric_types(data['metrics'])
    targets = get_targets(data['targets'])
    IastCircuitConfig.objects.filter(
        pk=config_id).update(**filted_data,
                             metric_types=metric_types,
                             targets=targets)
    IastCircuitTarget.objects.filter(
            circuit_config_id=config_id).delete()
    IastCircuitMetric.objects.filter(
            circuit_config_id=config_id).delete()
    obj = IastCircuitConfig.objects.filter(pk=config_id).first()
    for i in data['targets']:
        create_target(i, obj)

    for i in data['metrics']:
        create_metric(i, obj)


def create_metric(metrics: dict, circuit_config: IastCircuitConfig):
    IastCircuitMetric.objects.create(circuit_config=circuit_config, **metrics)


def create_target(target: dict, circuit_config: IastCircuitConfig):
    IastCircuitTarget.objects.create(circuit_config=circuit_config, **target)


METRIC_READABLE_DICT = {}
TARGET_READABLE_DICT = {}


def get_metric_types(metrics):
    metric_type_str = ""
    return metric_type_str
    for metric in metrics:
        metric_type_str += METRIC_READABLE_DICT[metric['name']]
    return metric_type_str


def get_targets(targets):
    target_type_str = ""
    return target_type_str
    for target in targets:
        target_type_str += TARGET_READABLE_DICT[target['target_type']]
    return target_type_str


def get_data_from_dict_by_key(dic: dict, fields: Iterable) -> dict:
    return {i: dic[i] for i in fields}


class AgentThresholdConfigV2(UserEndPoint, viewsets.ViewSet):
    name = "api-v1-agent-threshold-config-setting-v2"
    description = _("config Agent V2")

    @extend_schema_with_envcheck(
        [AgentConfigSettingV2Serializer],
        summary=_('Create AgentThresholdConfig'),
        description=_("Create AgentThresholdConfigV2"),
        tags=[_('AgentThresholdConfigV2')])
    def create(self, request):
        ser = AgentConfigSettingV2Serializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        config_create(ser.data, request.user)
        return R.success()

    def retrieve(self, request, pk):
        obj = IastCircuitConfig.objects.filter(pk=pk,
                                               is_deleted=0).values().first()
        if not obj:
            return R.failure()
        obj['targets'] = list(
            IastCircuitTarget.objects.filter(
                circuit_config_id=pk).values().all())
        obj['metrics'] = list(
            IastCircuitMetric.objects.filter(
                circuit_config_id=pk).values().all())
        return R.success(data=obj)

    def list(self, request):
        page = request.query_params.get('page', 1)
        page_size = request.query_params.get("page_size", 10)
        queryset = IastCircuitConfig.objects.filter(
            is_deleted=0).order_by('-priority').values()
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(page=page_summary, data=list(page_data))

    def update(self, request, pk):
        ser = AgentConfigSettingV2Serializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        config_update(ser.data, pk)
        return R.success()

    def reset(self, request, pk):
        return R.success()

    def delete(self, request, pk):
        IastCircuitConfig.objects.filter(pk=pk).update(is_deleted=1)
        return R.success()
