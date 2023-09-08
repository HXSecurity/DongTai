#!/usr/bin/env python
import logging
import time

from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.common.agent_command_check import (
    get_validatation_detail_message,
    tag_validator,
    taint_command_validator,
)
from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.utils import const
from dongtai_web.serializers.hook_strategy import SINK_POSITION_HELP_TEXT, StrategyTypeChoice
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("dongtai-webapi")


class _HookRuleAddBodyargsSerializer(serializers.Serializer):
    rule_type_id = serializers.IntegerField(help_text=_("The id of hook rule type."))
    language_id = serializers.IntegerField(help_text=_("The id of language."))
    rule_value = serializers.CharField(
        help_text=_("The value of strategy"),
        max_length=2000,
        allow_blank=True,
    )
    rule_source = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Source of taint"), SINK_POSITION_HELP_TEXT),
        max_length=255,
        allow_blank=True,
    )
    rule_target = serializers.CharField(
        help_text=format_lazy("{}\n{}", _("Target of taint"), SINK_POSITION_HELP_TEXT),
        max_length=255,
        allow_blank=True,
        default="",
    )
    inherit = serializers.CharField(
        help_text=_(
            "Inheritance type, false-only detect current class, true-inspect subclasses, all-check current class and subclasses"
        ),
        max_length=255,
    )
    track = serializers.CharField(
        help_text=_("Indicates whether taint tracking is required, true-required, false-not required."),
        max_length=5,
    )
    ignore_blacklist = serializers.BooleanField(
        required=False,
        default=False,
    )
    ignore_internal = serializers.BooleanField(
        required=False,
        default=False,
    )
    tags = serializers.ListField(
        child=serializers.CharField(validators=[tag_validator]),
        required=False,
        default=list,
    )
    untags = serializers.ListField(
        child=serializers.CharField(validators=[tag_validator]),
        required=False,
        default=list,
    )
    command = serializers.CharField(
        max_length=255,
        validators=[taint_command_validator],
        required=False,
        default="",
        allow_blank=True,
    )
    stack_blacklist = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
    )
    type = serializers.ChoiceField(
        required=False,
        help_text="".join([f" {i.label}: {i.value} " for i in StrategyTypeChoice]),
        choices=StrategyTypeChoice,
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Policy enabled success, total {} hook rules")), ""),
        ((202, _("Incomplete parameter, please check again")), ""),
        ((202, _("Failed to create strategy")), ""),
    )
)


class EngineHookRuleAddEndPoint(UserEndPoint):
    def parse_args(self, request):
        """
        :param request:
        :return:
        """
        try:
            rule_type = request.data.get("rule_type_id")
            rule_value = request.data.get("rule_value").strip()
            rule_source = request.data.get("rule_source").strip()
            inherit = request.data.get("inherit").strip()
            is_track = request.data.get("track").strip()
            language_id = request.data.get("language_id")
            ignore_blacklist = request.data.get("ignore_blacklist", False)
            ignore_internal = request.data.get("ignore_internal", False)
            request.data.get("tags", [])
            request.data.get("untags", [])
            request.data.get("command", "")
            request.data.get("stack_blacklist", [])
        except Exception as e:
            logger.exception("uncatched exception: ", exc_info=e)
            return None, None, None, None, None, None, None, None
        else:
            return (
                rule_type,
                rule_value,
                rule_source,
                inherit,
                is_track,
                language_id,
                ignore_blacklist,
                ignore_internal,
            )

    @staticmethod
    def create_strategy(
        value,
        source,
        target,
        inherit,
        track,
        created_by,
        language_id,
        type_,
        ignore_blacklist,
        ignore_internal,
        tags,
        untags,
        command,
        stack_blacklist,
    ):
        try:
            timestamp = int(time.time())
            strategy = HookStrategy(
                value=value,
                source=source,
                target=target,
                inherit=inherit,
                track=track,
                create_time=timestamp,
                update_time=timestamp,
                created_by=created_by,
                enable=const.ENABLE,
                language_id=language_id,
                type=type_,
                ignore_blacklist=ignore_blacklist,
                ignore_internal=ignore_internal,
                tags=tags,
                untags=untags,
                command=command,
                stack_blacklist=stack_blacklist,
            )
            strategy.save()
        except Exception as e:
            logger.info(e, exc_info=e)
            return None
        else:
            return strategy

    @extend_schema_with_envcheck(
        request=_HookRuleAddBodyargsSerializer,
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Add"),
        description=_("Generate corresponding strategy group according to the strategy selected by the user."),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        # bad parameter parse and validate example, don't do this again.
        # don't use it again when old fields change.
        (
            rule_type,
            rule_value,
            rule_source,
            inherit,
            is_track,
            language_id,
            ignore_blacklist,
            ignore_internal,
        ) = self.parse_args(request)
        if all((rule_type, rule_value, rule_source, inherit, is_track)) is False:
            return R.failure(msg=_("Incomplete parameter, please check again"))

        ser = _HookRuleAddBodyargsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail, msg=get_validatation_detail_message(e))
        # for compatibility only
        # the "type" not in ser.validated_data should be remove.
        if ("type" in ser.validated_data and ser.validated_data["type"] == 4) or (
            "type" not in ser.validated_data and ser.validated_data["rule_target"] == ""
        ):
            hook_type = IastStrategyModel.objects.filter(
                id=rule_type,
                user_id__in=[request.user.id, const.SYSTEM_USER_ID],
            ).first()
        else:
            hook_type = HookType.objects.filter(
                id=rule_type,
                created_by__in=(request.user.id, const.SYSTEM_USER_ID),
            ).first()
        if not hook_type:
            return R.failure(msg=_("Failed to create strategy"))
        # for compatibility only
        # the "type" not in ser.validated_data should be remove.
        type_ = (
            (4 if ser.validated_data["rule_target"] == "" else hook_type.type)
            if "type" not in ser.validated_data
            else ser.validated_data["type"]
        )

        if HookStrategy.objects.filter(
            language_id=ser.validated_data["language_id"], type=type_, value=rule_value
        ).exists():
            return R.failure(msg="Already exists same rule")

        strategy = self.create_strategy(
            rule_value,
            rule_source,
            ser.validated_data["rule_target"],
            inherit,
            is_track,
            request.user.id,
            language_id,
            type_,
            ignore_blacklist,
            ignore_internal,
            ser.validated_data["tags"],
            ser.validated_data["untags"],
            ser.validated_data["command"],
            ser.validated_data["stack_blacklist"],
        )
        if strategy:
            hook_type.strategies.add(strategy)
            return R.success(msg=_("Strategy has been created successfully"))
        return R.failure(msg=_("Failed to create strategy"))
