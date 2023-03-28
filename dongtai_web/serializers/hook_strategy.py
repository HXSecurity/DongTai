#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# software: PyCharm
# project: lingzhi-engine
from dongtai_common.models import User
from dongtai_common.models.hook_strategy import HookStrategy
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.utils.text import format_lazy
from dongtai_common.utils import const


SINK_POSITION_HELP_TEXT = _("""
Examples in a single case: O, P<1,2,3,4,...>, R
Combination situation: O&R, O&P1, etc.
O represents the object itself; R represents the return value; P represents the parameter, and the number represents the position of the parameter
""")

HOOK_TYPE_CHOICE = (const.RULE_SOURCE, const.RULE_ENTRY_POINT,
                    const.RULE_PROPAGATOR, const.RULE_FILTER, const.RULE_SINK)


class SinkSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookStrategy
        fields = ['value']


class HookRuleSerializer(serializers.ModelSerializer):
    USER = dict()
    rule_type = serializers.SerializerMethodField(
        help_text=_('The name of hook rule type.'))
    rule_type_id = serializers.SerializerMethodField(
        help_text=_('The id of hook rule type.'))
    user = serializers.SerializerMethodField(
        help_text=_('The user who created the hook rule type.'))
    id = serializers.IntegerField(help_text=_('The id of strategy'))
    value = serializers.CharField(
        help_text=_('The value of strategy'),
        max_length=255,
    )
    source = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Source of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
    )
    target = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Target of taint"),
                              SINK_POSITION_HELP_TEXT),
        max_length=255,
    )
    inherit = serializers.CharField(
        help_text=_('Inheritance type, false-only detect current class, true-inspect subclasses, all-check current class and subclasses'
                    ),
        max_length=255,
    )
    track = serializers.CharField(
        help_text=_("Indicates whether taint tracking is required, true-required, false-not required."
                    ),
        max_length=5,
    )
    update_time = serializers.IntegerField(
        help_text=_("The update time of hook strategy"), )
    enable = serializers.IntegerField(help_text=_(
        "The enabled state of the hook strategy: 0-disabled, 1-enabled, -1-deleted"
    ),
        default=1)

    class Meta:
        model = HookStrategy
        fields = [
            'id',
            'rule_type_id',
            'rule_type',
            'value',
            'source',
            'target',
            'inherit',
            'track',
            'update_time',
            'enable',
            'user',
            'strategy',
            'ignore_blacklist',
            'ignore_internal',
        ]

    def get_rule_type(self, obj):
        if obj.type == 4:
            return obj.strategy.vul_name
        rule_type = obj.hooktype
        if rule_type:
            return rule_type.name
        else:
            return 'Unknown'

    def get_rule_type_id(self, obj):
        if obj.type == 4:
            return obj.strategy.id
        rule_type = obj.hooktype
        if rule_type:
            return rule_type.id
        else:
            return -1

    def get_user(self, obj):
        if obj.created_by not in self.USER:
            temp_user = User.objects.filter(id=obj.created_by).first()
            self.USER[obj.created_by] = temp_user.get_username() if temp_user else ''
        return self.USER[obj.created_by]
