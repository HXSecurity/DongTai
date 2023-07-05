#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:sjh
# software: PyCharm
# project: webApi
# agent threshold setting
from dongtai_conf.settings import DEFAULT_CIRCUITCONFIG
from django.db.models import F
from django.forms.models import model_to_dict
from django.db.models import Max, Min
from inflection import underscore
from collections.abc import Iterable
from dongtai_common.models.agent_config import (
    IastCircuitTarget,
    IastCircuitConfig,
    IastCircuitMetric,
    TargetType,
    TargetOperator,
    DealType,
    MetricType,
    MetricGroup,
    MetricOperator,
    SystemMetricType,
    JVMMetricType,
    ApplicationMetricType,
    UNIT_DICT,
)
from rest_framework import viewsets
from rest_framework import serializers
import time

from dongtai_common.endpoint import UserEndPoint, R, TalentAdminEndPoint
from dongtai_common.models.agent_config import IastAgentConfig
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_web.serializers.agent_config import AgentConfigSettingSerializer
from rest_framework.serializers import ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict
from typing import Dict
from collections import OrderedDict

_ResponseSerializer = get_response_serializer(status_msg_keypair=(
    ((201, _('The setting is complete')), ''),
    ((202, _('Incomplete parameter, please try again later')), '')
))


class AgentThresholdConfig(UserEndPoint):
    name = "api-v1-agent-threshold-config-setting"
    description = _("config Agent")

    def create_agent_config(self, user, details, hostname, ip, port, cluster_name, cluster_version, priority, id):
        try:

            timestamp = int(time.time())
            if id:
                strategy = IastAgentConfig.objects.filter(user=user, id=id).order_by("-create_time").first()
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

        config = self.create_agent_config(user, details, hostname, ip, port, cluster_name, cluster_version, priority, id)
        if config:
            return R.success(msg=_('保存成功'))
        else:
            return R.failure(msg=_('保存失败'))


def intable_validate(value):
    try:
        a = int(value)
    except ValueError as e:
        raise serializers.ValidationError('This field must be an intable.')


class AgentConfigSettingV2TargetSerializer(serializers.Serializer):
    target_type = serializers.ChoiceField(TargetType.choices)
    opt = serializers.ChoiceField(TargetOperator.choices)
    value = serializers.CharField()


class AgentConfigSettingV2MetricSerializer(serializers.Serializer):
    metric_type = serializers.ChoiceField(MetricType.choices)
    opt = serializers.ChoiceField(MetricOperator.choices)
    value = serializers.CharField(validators=[intable_validate])


class AgentConfigSettingV2Serializer(serializers.Serializer):
    name = serializers.CharField()
    targets = serializers.ListField(
        child=AgentConfigSettingV2TargetSerializer())
    metric_group = serializers.ChoiceField(MetricGroup.choices)
    metrics = serializers.ListField(
        child=AgentConfigSettingV2MetricSerializer())
    interval = serializers.IntegerField(default=30)
    deal = serializers.ChoiceField(DealType.choices)
    is_enable = serializers.IntegerField()


def get_priority_max_now() -> int:
    res = IastCircuitConfig.objects.all().aggregate(Max("priority"))
    return res["priority__max"] + 1


def get_priority_min_now() -> int:
    res = IastCircuitConfig.objects.all().aggregate(Min("priority"))
    return res["priority__min"] - 1


def config_create(data, user):
    fields = ('name', 'metric_group', 'is_enable', 'deal',
              "interval")
    filted_data = get_data_from_dict_by_key(data, fields)
    metric_types = get_metric_types(data['metrics'])
    targets = get_targets(data['targets'])
    obj = IastCircuitConfig.objects.create(**filted_data,
                                           metric_types=metric_types,
                                           target_types=targets,
                                           priority=get_priority_max_now(),
                                           user=user)
    for i in data['targets']:
        create_target(i, obj)

    for i in data['metrics']:
        create_metric(i, obj)


def config_update(data, config_id):
    fields = ('name', 'metric_group', 'is_enable', 'deal',
              "interval")
    filted_data = get_data_from_dict_by_key(data, fields)
    metric_types = get_metric_types(data['metrics'])
    targets = get_targets(data['targets'])
    IastCircuitConfig.objects.filter(
        pk=config_id).update(**filted_data,
                             metric_types=metric_types,
                             target_types=targets)
    IastCircuitTarget.objects.filter(
        circuit_config_id=config_id).delete()
    IastCircuitMetric.objects.filter(
        circuit_config_id=config_id).delete()
    obj = IastCircuitConfig.objects.filter(pk=config_id).first()
    if obj is None:
        return
    for i in data['targets']:
        create_target(i, obj)

    for i in data['metrics']:
        create_metric(i, obj)


def create_metric(metrics: dict | OrderedDict,
                  circuit_config: IastCircuitConfig):
    IastCircuitMetric.objects.create(circuit_config=circuit_config, **metrics)


def create_target(target: dict | OrderedDict,
                  circuit_config: IastCircuitConfig):
    IastCircuitTarget.objects.create(circuit_config=circuit_config, **target)


def get_metric_types(metrics):
    str_list = []
    for metric in metrics:
        str_list.append(str(MetricType(metric['metric_type']).label))
    return "、".join(str_list)


def get_targets(targets):
    str_list = []
    for target in targets:
        str_list.append(str(TargetType(target['target_type']).label))
    res = "、".join(str_list)
    if not res:
        return str(_("全部"))
    return res


def get_data_from_dict_by_key(dic: ReturnDict | Dict,
                              fields: Iterable) -> Dict:
    return {i: dic[i] for i in fields}


# when target_priority < config.priorty
def set_config_change_lt(config_id, target_priority: int):
    config = IastCircuitConfig.objects.filter(pk=config_id).first()
    if not config:
        return
    IastCircuitConfig.objects.filter(
        priority__gte=target_priority,
        priority__lt=config.priority).update(priority=F('priority') + 1)
    config.priority = target_priority
    config.save()


def set_config_top(config_id):
    return set_config_change_lt(config_id,
                                target_priority=get_priority_min_now())


# when target_priority > config.priorty
def set_config_change_gt(config_id, target_priority: int):
    config = IastCircuitConfig.objects.filter(pk=config_id).first()
    if not config:
        return
    IastCircuitConfig.objects.filter(
        priority__lte=target_priority,
        priority__gt=config.priority).update(priority=F('priority') - 1)
    config.priority = target_priority
    config.save()


def set_config_bottom(config_id):
    set_config_change_gt(config_id, target_priority=get_priority_max_now())


def set_config_change_proprity(config_id, priority_range: list):
    config = IastCircuitConfig.objects.filter(pk=config_id).first()
    if not config:
        return
    if min(priority_range) > config.priority:
        set_config_change_gt(config.id, min(priority_range))
    if max(priority_range) < config.priority:
        set_config_change_lt(config.id, max(priority_range))


class AgentThresholdConfigV2(TalentAdminEndPoint, viewsets.ViewSet):
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

    @extend_schema_with_envcheck(
        summary=_('AgentThresholdConfig Detail'),
        tags=[_('AgentThresholdConfigV2')])
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

    @extend_schema_with_envcheck(
        summary=_('AgentThresholdConfig List'),
        tags=[_('AgentThresholdConfigV2')])
    def list(self, request):
        #        page = request.query_params.get('page', 1)
        #        page_size = request.query_params.get("page_size", 10)
        queryset = IastCircuitConfig.objects.filter(
            is_deleted=0).order_by('priority').prefetch_related(
                'iastcircuittarget_set', 'iastcircuitmetric_set').all()
        # page_summary, page_data = self.get_paginator(queryset, page, page_size)
        obj_list = []
        for data in queryset:
            obj = model_to_dict(data)
            obj['targets'] = list(data.iastcircuittarget_set.values().all())
            obj['metrics'] = list(data.iastcircuitmetric_set.values().all())
            obj_list.append(obj)
        return R.success(data=obj_list)

    @extend_schema_with_envcheck(
        summary=_('Update AgentThresholdConfig'),
        description=_("Update AgentThresholdConfigV2"),
        tags=[_('AgentThresholdConfigV2')])
    def update(self, request, pk):
        ser = AgentConfigSettingV2Serializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        config_update(ser.data, pk)
        return R.success()

    @extend_schema_with_envcheck(
        summary=_('重置 AgentThresholdConfig'),
        description=_("重置 AgentThresholdConfigV2"),
        tags=[_('AgentThresholdConfigV2')])
    def reset(self, request, pk):
        if IastCircuitConfig.objects.filter(pk=pk).exists():
            config = IastCircuitConfig.objects.filter(pk=pk, ).first()
            if config is None:
                return R.failure()
            mg = MetricGroup(config.metric_group)
            data = DEFAULT_CIRCUITCONFIG[mg.name]
            config_update(data, pk)
            return R.success()
        return R.failure()

    def change_priority(self, request, pk):
        type_ = request.data.get('type')
        priority_range = request.data.get('priority_range')
        if IastCircuitConfig.objects.filter(pk=pk).exists():
            if type_ == 1:
                set_config_top(pk)
                return R.success()
            if type_ == 2 and priority_range:
                set_config_change_proprity(pk, priority_range)
                return R.success()
            if type_ == 3:
                set_config_bottom(pk)
                return R.success()
        return R.failure()

    @extend_schema_with_envcheck(
        summary=_('Delete AgentThresholdConfig'),
        description=_("Delete AgentThresholdConfigV2"),
        tags=[_('AgentThresholdConfigV2')])
    def delete(self, request, pk):
        IastCircuitConfig.objects.filter(pk=pk).update(is_deleted=1)
        return R.success()

    @extend_schema_with_envcheck(
        summary=_('获取 AgentThresholdConfig 枚举'),
        description=_("获取 AgentThresholdConfigV2 枚举"),
        tags=[_('AgentThresholdConfigV2')])
    def enum(self, request, enumname):
        able_to_search = (TargetType, MetricType, MetricGroup, TargetOperator,
                          MetricOperator, DealType, SystemMetricType,
                          JVMMetricType, ApplicationMetricType)
        able_to_search_dict = {
            underscore(item.__name__): item
            for item in able_to_search
        }
        if enumname not in able_to_search_dict.keys():
            return R.failure()
        return R.success(data=convert_choices_to_value_dict(
            able_to_search_dict.get(enumname)))

    @extend_schema_with_envcheck(
        summary=_('获取 AgentThresholdConfig 所有枚举'),
        tags=[_('AgentThresholdConfigV2')])
    def enumall(self, request):
        able_to_search = (TargetType, MetricType, MetricGroup, TargetOperator,
                          MetricOperator, DealType, SystemMetricType,
                          JVMMetricType, ApplicationMetricType)
        res = {
            underscore(item.__name__): convert_choices_to_value_dict(item)
            for item in able_to_search
        }
        res['UNIT_DICT'] = UNIT_DICT
        return R.success(data=res)


def convert_choices_to_dict(choices):
    fields = ['value', 'name', 'label']
    return [{field: getattr(choice, field)
             for field in fields}
            for choice in choices]


def convert_choices_to_value_dict(choices):
    fields = ['name', 'label']
    return {
        choice.value: {field: getattr(choice, field)
                       for field in fields}
        for choice in choices
    }
