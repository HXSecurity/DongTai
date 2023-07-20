#!/usr/bin/env python
import logging
import time

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.hook_type import HookType
from dongtai_common.utils import const
from dongtai_web.serializers.hook_strategy import HOOK_TYPE_CHOICE
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

ENABLE_CHOICE = (const.ENABLE, const.DISABLE)
logger = logging.getLogger("dongtai-webapi")


class _EngineHookRuleTypeAddSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        HOOK_TYPE_CHOICE,
        help_text=_(
            "type of hook rule \n 1 represents the propagation method, 2 represents the source method, 3 represents the filter method, and 4 represents the taint method"
        ),
        required=True,
    )
    enable = serializers.ChoiceField(
        ENABLE_CHOICE,
        help_text=_("The enabled state of the hook strategy: 0-disabled, 1-enabled"),
        required=True,
    )
    name = serializers.CharField(
        help_text=_("The name of hook type"), max_length=255, required=True
    )
    short_name = serializers.CharField(
        help_text=_("The short name of hook type"), max_length=255, required=True
    )
    language_id = serializers.ChoiceField(
        (1, 2, 3, 4),
        default=1,
        help_text=_(
            "The id of programming language,find it in the programming language api"
        ),
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Rule type successfully saved")), ""),
        ((202, _("Incomplete data")), ""),
    )
)


class EngineHookRuleTypeAddEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            ser = _EngineHookRuleTypeAddSerializer(data=request.data)
            try:
                ser.is_valid(True)
            except ValidationError:
                return None, None, None, None, None
            rule_type = ser.validated_data.get("type")
            rule_type = int(rule_type)
            if rule_type not in (
                const.RULE_SOURCE,
                const.RULE_ENTRY_POINT,
                const.RULE_PROPAGATOR,
            ):
                rule_type = None

            name = ser.validated_data.get("name")

            short_name = ser.validated_data.get("short_name")

            enable = ser.validated_data.get("enable")
            enable = int(enable)
            language_id = ser.validated_data.get("language_id", 1)
            if enable not in ENABLE_CHOICE:
                return None, None, None, None, None
        except Exception as e:
            logger.exception(_("Parameter parsing failed, error message: "), exc_info=e)
            return None, None, None, None, None
        else:
            return rule_type, name, short_name, enable, language_id

    @extend_schema_with_envcheck(
        request=_EngineHookRuleTypeAddSerializer,
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Type Add"),
        description=_("Create hook rule type based on incoming parameters"),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        rule_type, name, short_name, enable, language_id = self.parse_args(request)
        if all((rule_type, name, short_name, language_id)) is False:
            return R.failure(msg=_("Incomplete data"))
        timestamp = int(time.time())
        hook_type = HookType(
            enable=enable,
            type=rule_type,
            name=short_name,
            value=name,
            create_time=timestamp,
            update_time=timestamp,
            created_by=request.user.id,
            language_id=language_id,
            vul_strategy_id=-1,
        )
        hook_type.save()
        return R.success(msg=_("Rule type successfully saved"))
