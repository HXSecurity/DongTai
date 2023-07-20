#!/usr/bin/env python
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.utils import const
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("dongtai-webapi")


class EngineHookRuleTypeEnableSerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(
        help_text=_("The id of hook type"), default=const.RULE_PROPAGATOR
    )


_GetResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Enable successfully")), ""),
        ((202, _("Operation type does not exist")), ""),
        ((202, _("Strategy type does not exist")), ""),
    )
)


class EngineHookRuleTypeEnableEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_id = request.query_params.get("rule_id", const.RULE_PROPAGATOR)
            return int(rule_id)
        except Exception as e:
            logger.exception(
                _("Parameter processing failed, error message: "), exc_info=e
            )
            return None

    @extend_schema_with_envcheck(
        [EngineHookRuleTypeEnableSerializer],
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Status Enable"),
        description=_(
            "Enable the status of the rule corresponding to the specified id."
        ),
        response_schema=_GetResponseSerializer,
    )
    def get(self, request):
        rule_id = self.parse_args(request)
        if rule_id is None:
            return R.failure(msg=_("Strategy does not exist"))

        rule = HookStrategy.objects.filter(id=rule_id).first()
        if rule:
            rule_type = rule.type.first()
            if rule_type:
                rule_type.enable = const.ENABLE
                rule.save()
                return R.success(msg=_("Enable successfully"))
        return R.failure(msg=_("Strategy type does not exist"))
