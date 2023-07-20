#!/usr/bin/env python

from dongtai_common.models.strategy_user import IastStrategyUser
from dongtai_common.utils import const
from dongtai_common.models.hook_type import HookType
from dongtai_common.models.strategy import IastStrategyModel

from django.db.models import Q
from dongtai_common.endpoint import R
from dongtai_common.utils import const
from dongtai_common.endpoint import UserEndPoint
from dongtai_web.serializers.strategy import StrategySerializer
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer
from dongtai_common.models.hook_type import HookType
from rest_framework import serializers
from dongtai_common.models.program_language import IastProgramLanguage
import time
from rest_framework.serializers import ValidationError
from dongtai_common.permissions import TalentAdminPermission
from rest_framework.decorators import permission_classes
from dongtai_common.models.vul_level import IastVulLevel


class _StrategyResponseDataStrategySerializer(serializers.Serializer):
    id = serializers.CharField(help_text=_("The id of agent"))
    vul_name = serializers.CharField(
        help_text=_("The name of the vulnerability type targeted by the strategy")
    )
    vul_type = serializers.CharField(
        help_text=_("Types of vulnerabilities targeted by the strategy")
    )
    enable = serializers.CharField(
        help_text=_("This field indicates whether the vulnerability is enabled, 1 or 0")
    )
    vul_desc = serializers.CharField(
        help_text=_("Description of the corresponding vulnerabilities of the strategy")
    )
    level = serializers.IntegerField(
        help_text=_("The strategy corresponds to the level of vulnerability")
    )
    dt = serializers.IntegerField(help_text=_("Strategy update time"))
    vul_fix = serializers.CharField(
        help_text=_(
            "Suggestions for repairing vulnerabilities corresponding to the strategy"
        )
    )


class StrategyCreateSerializer(serializers.Serializer):
    vul_name = serializers.CharField(
        help_text=_("The name of the vulnerability type targeted by the strategy")
    )
    vul_type = serializers.CharField(
        help_text=_("Types of vulnerabilities targeted by the strategy")
    )
    state = serializers.CharField(
        help_text=_("This field indicates whether the vulnerability is enabled, 1 or 0")
    )
    vul_desc = serializers.CharField(
        help_text=_("Description of the corresponding vulnerabilities of the strategy")
    )
    level_id = serializers.IntegerField(
        min_value=1,
        help_text=_("The strategy corresponds to the level of vulnerability"),
    )
    vul_fix = serializers.CharField(
        allow_blank=True,
        help_text=_(
            "Suggestions for repairing vulnerabilities corresponding to the strategy"
        ),
    )

    def validate_level_id(self, value):
        if not IastVulLevel.objects.filter(pk=value).exists():
            raise serializers.ValidationError("this vul level not exist")
        return value


_ResponseSerializer = get_response_serializer(
    data_serializer=_StrategyResponseDataStrategySerializer(many=True),
)


class _StrategyArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=None, help_text=_("Number per page"))
    page = serializers.IntegerField(default=None, help_text=_("Page index"))
    name = serializers.CharField(
        default=None,
        help_text=_("The name of the item to be searched, supports fuzzy search."),
    )


STATUS_DELETE = "delete"


class StrategyEndpoint(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("Strategy")],
        summary=_("Strategy retrieve"),
        description=_("Get a strategiey by id."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, pk):
        q = ~Q(state=STATUS_DELETE)
        q = q & Q(pk=pk)
        queryset = IastStrategyModel.objects.filter(q).first()
        return R.success(
            data=StrategySerializer(queryset).data,
        )


class StrategysEndpoint(UserEndPoint):
    permission_classes_by_action = {"POST": (TalentAdminPermission,)}

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.request.method]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [_StrategyArgsSerializer],
        tags=[_("Strategy")],
        summary=_("Strategy List"),
        description=_("Get a list of strategies."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        ser = _StrategyArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data["page_size"]
                page = ser.validated_data["page"]
                name = ser.validated_data["name"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        q = ~Q(state=STATUS_DELETE)
        if name:
            q = q & Q(vul_name__icontains=name)
        queryset = IastStrategyModel.objects.filter(q).order_by("-id").all()
        if page and page_size:
            page_summary, page_data = self.get_paginator(queryset, page, page_size)
            return R.success(
                data=StrategySerializer(page_data, many=True).data, page=page_summary
            )
        else:
            return R.success(
                data=StrategySerializer(queryset, many=True).data,
            )

        strategy_models = (
            HookType.objects.filter(type=const.RULE_SINK)
            .values("id", "name", "value", "enable")
            .exclude(enable=const.DELETE)
        )
        if strategy_models:
            models = {}
            for strategy_model in strategy_models:
                models[strategy_model["id"]] = {
                    "id": strategy_model["id"],
                    "vul_name": strategy_model["name"],
                    "vul_type": strategy_model["value"],
                    "state": const.STRATEGY_DISABLE
                    if strategy_model["enable"] is not None
                    and strategy_model["enable"] == 0
                    else const.STRATEGY_ENABLE,
                    "vul_desc": "",
                    "level": 1,
                    "dt": 1,
                }

            strategy_ids = models.keys()
            profiles = IastStrategyModel.objects.values(
                "level_id", "vul_desc", "vul_fix", "hook_type_id"
            ).filter(hook_type_id__in=strategy_ids)
            if profiles:
                for profile in profiles:
                    strategy_id = profile.get("hook_type_id")
                    models[strategy_id]["vul_desc"] = profile["vul_desc"]
                    models[strategy_id]["vul_fix"] = profile["vul_fix"]
                    models[strategy_id]["level"] = profile["level_id"]
            return R.success(data=list(models.values()))
        else:
            return R.success(msg=_("No strategy"))

    @extend_schema_with_envcheck(
        request=StrategyCreateSerializer,
        tags=[_("Strategy")],
        summary=_("Strategy Add"),
        description=_(
            "Generate corresponding strategy group according to the strategy selected by the user."
        ),
        response_schema=_ResponseSerializer,
    )
    def post(self, request):
        ser = StrategyCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        print(ser.validated_data)
        strategy = IastStrategyModel.objects.create(
            **ser.validated_data, user=request.user, dt=time.time()
        )
        strategy.save()
        content = IastStrategyUser.objects.get(pk=5).content.split(",")
        if str(strategy.id) not in content:
            content.append(str(strategy.id))
        IastStrategyUser.objects.filter(pk=5).update(content=",".join(content))
        for language in IastProgramLanguage.objects.all():
            HookType.objects.create(
                type=3,
                name=ser.validated_data["vul_name"],
                value=ser.validated_data["vul_type"],
                enable=1,
                create_time=time.time(),
                update_time=time.time(),
                created_by=request.user.id,
                language=language,
                vul_strategy=strategy,
            )
            HookType.objects.create(
                type=4,
                name=ser.validated_data["vul_name"],
                value=ser.validated_data["vul_type"],
                enable=1,
                create_time=time.time(),
                update_time=time.time(),
                created_by=request.user.id,
                language=language,
                vul_strategy=strategy,
            )
        return R.success(data=StrategySerializer(strategy).data)
