#!/usr/bin/env python
import logging

from dongtai_common.endpoint import UserEndPoint, R
from dongtai_common.models.hook_strategy import HookStrategy
from dongtai_common.utils import const
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from rest_framework import serializers
from dongtai_common.models.hook_type import HookType

logger = logging.getLogger("dongtai-webapi")

OP_CHOICES = ("enable", "disable", "delete")
SCOPE_CHOICES = ("all",)


class EngineHookRuleStatusGetQuerySerializer(serializers.Serializer):
    rule_id = serializers.IntegerField(
        required=False, help_text=_("The id of hook rule")
    )
    type = serializers.IntegerField(
        required=False, help_text=_("The id of hook rule type")
    )
    op = serializers.ChoiceField(
        OP_CHOICES, required=False, help_text=_("The state of the hook rule")
    )
    scope = serializers.ChoiceField(
        SCOPE_CHOICES, required=False, help_text=_("The scope of the hook rule")
    )
    language_id = serializers.IntegerField(
        required=False, help_text=_("The language_id")
    )
    hook_rule_type = serializers.IntegerField(
        required=False, help_text=_("The type of hook rule")
    )


class EngineHookRuleStatusPostBodySerializer(serializers.Serializer):
    ids = serializers.CharField(
        help_text=_('The id corresponding to the hook type, use"," for segmentation.')
    )
    op = serializers.ChoiceField(OP_CHOICES, help_text=_("The state of the hook rule"))


_GetResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Operation success")), ""),
        ((202, _("Operation type does not exist")), ""),
        ((202, _("Strategy does not exist")), ""),
    )
)

_PostResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Operation success")), ""),
        ((202, _("Operation type does not exist")), ""),
        ((202, _("Incorrect parameter")), ""),
    )
)


class EngineHookRuleEnableEndPoint(UserEndPoint):
    def parse_args(self, request):
        rule_id = request.query_params.get("rule_id")
        rule_type = request.query_params.get("type")
        scope = request.query_params.get("scope")
        op = request.query_params.get("op")
        return (
            rule_id,
            rule_type,
            scope,
            op,
            request.query_params.get("language_id"),
            request.query_params.get("hook_rule_type"),
        )

    @staticmethod
    def set_strategy_status(strategy_id, strategy_ids, enable_status):
        if strategy_id:
            rule = HookStrategy.objects.filter(
                id=strategy_id,
            ).first()
            if rule:
                rule.enable = enable_status
                rule.save()
                return 1
        elif strategy_ids:
            return HookStrategy.objects.filter(
                id__in=strategy_ids,
            ).update(enable=enable_status)
        return 0

    @staticmethod
    def check_op(op):
        if op == "enable":
            op = const.ENABLE
        elif op == "disable":
            op = const.DISABLE
        elif op == "delete":
            op = const.DELETE
        else:
            op = None
        return op

    @extend_schema_with_envcheck(
        [EngineHookRuleStatusGetQuerySerializer],
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Status Modify"),
        description=_(
            "Modify the status of the rule corresponding to the specified id."
        ),
        response_schema=_GetResponseSerializer,
    )
    def get(self, request):
        rule_id, rule_type, scope, op, language_id, hook_rule_type = self.parse_args(
            request
        )
        try:
            if rule_id:
                rule_id = int(rule_id)
            if rule_type:
                rule_type = int(rule_type)
        except BaseException:
            return R.failure(_("Parameter error"))
        status = False

        op = self.check_op(op)
        if op is None:
            return R.failure(msg=_("Operation type does not exist"))
        if rule_type is not None and scope == "all":
            count = HookStrategy.objects.filter(hooktype__id=rule_type).update(
                enable=op
            )
            logger.info(
                _("Policy type {} operation success, total of {} Policy types").format(
                    rule_type, count
                )
            )
            status = True
        if hook_rule_type is not None and language_id is not None and scope == "all":
            hook_type_ids = (
                HookType.objects.filter(language_id=language_id, type=hook_rule_type)
                .values_list("id", flat=True)
                .all()
            )
            count = HookStrategy.objects.filter(
                hooktype__id__in=hook_type_ids,
            ).update(enable=op)
            logger.info(_("total of {} Policy types").format(count))
            status = True
        elif rule_id is not None:
            status = self.set_strategy_status(
                strategy_id=rule_id, strategy_ids=None, enable_status=op
            )
            logger.info(_("Policy {} succeed").format(rule_id))

        if status:
            return R.success(msg=_("Operation success"))
        else:
            return R.failure(msg=_("Strategy does not exist"))

    @extend_schema_with_envcheck(
        request=EngineHookRuleStatusPostBodySerializer,
        tags=[_("Hook Rule")],
        summary=_("Hook Rule Status Modify (Batch)"),
        description=_(
            "Batch modify the status of the rule corresponding to the specified id"
        ),
        response_schema=_PostResponseSerializer,
    )
    def post(self, request):
        op = request.data.get("op")
        op = self.check_op(op)
        if op is None:
            return R.failure(msg=_("Operation type does not exist"))

        strategy_ids = request.data.get("ids")
        try:
            strategy_ids = [int(i) for i in strategy_ids.split(",")]
        except BaseException:
            return R.failure(_("Parameter error"))
        if strategy_ids:
            count = self.set_strategy_status(
                strategy_id=None, strategy_ids=strategy_ids, enable_status=op
            )
            logger.info(_("Strategy operation success, total {}").format(count))
            return R.success(msg=_("Operation success"))
        else:
            return R.failure(msg=_("Incorrect parameter"))
