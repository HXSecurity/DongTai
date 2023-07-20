######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : sensitive_info_rule
# @created     : 星期三 11月 17, 2021 16:15:57 CST
#
# @description :
######################################################################


import contextlib

from django.core.exceptions import (
    ObjectDoesNotExist,
)

from dongtai_web.views.utils.commonview import (
    AllStatusUpdateSerializerView,
    BatchStatusUpdateSerializerView,
)

try:
    import re2 as re
except ImportError:
    import re
with contextlib.suppress(ImportError):
    import jq

import logging
import time

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, viewsets
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.sensitive_info import IastPatternType, IastSensitiveInfoRule
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_web.utils import extend_schema_with_envcheck

logger = logging.getLogger("dongtai-webapi")


class SensitiveInfoRuleSerializer(serializers.ModelSerializer):
    strategy_name = serializers.SerializerMethodField()
    strategy_id = serializers.SerializerMethodField()
    pattern_type_id = serializers.SerializerMethodField()
    pattern_type_name = serializers.SerializerMethodField()

    class Meta:
        model = IastSensitiveInfoRule
        fields = [
            "id",
            "strategy_name",
            "strategy_id",
            "pattern_type_id",
            "pattern_type_name",
            "pattern",
            "status",
            "latest_time",
        ]

    def get_strategy_name(self, obj):
        try:
            return obj.strategy.vul_name
        except ObjectDoesNotExist as e:
            print(e)
            return ""

    def get_strategy_id(self, obj):
        try:
            return obj.strategy.id
        except ObjectDoesNotExist as e:
            print(e)
            return 0

    def get_pattern_type_id(self, obj):
        try:
            return obj.pattern_type.id
        except ObjectDoesNotExist as e:
            print(e)
            return 0

    def get_pattern_type_name(self, obj):
        try:
            return obj.pattern_type.name
        except ObjectDoesNotExist as e:
            print(e)
            return ""


class SensitiveInfoPatternTypeSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = IastPatternType
        fields = ["id", "name", "url"]

    def get_url(self, obj):
        url_dict = {1: "regex", 2: "json"}
        return url_dict.get(obj.id, "")


class SensitiveInfoRuleCreateSerializer(serializers.Serializer):
    strategy_id = serializers.IntegerField(
        min_value=1, max_value=2147483646, required=True
    )
    pattern_type_id = serializers.IntegerField(
        min_value=1, max_value=2147483646, required=True
    )
    pattern = serializers.CharField(required=True)
    status = serializers.ChoiceField(choices=(0, 1), required=True)


class _SensitiveInfoArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    name = serializers.CharField(
        default=None,
        required=False,
        help_text=_("The name of the item to be searched, supports fuzzy search."),
    )


class _RegexPatternValidationSerializer(serializers.Serializer):
    pattern = serializers.CharField(help_text=_("regex pattern"))
    test_data = serializers.CharField(help_text=_("the data for test regex"))


class SensitiveInfoRuleViewSet(UserEndPoint, viewsets.ViewSet):
    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @extend_schema_with_envcheck(
        [_SensitiveInfoArgsSerializer],
        tags=[_("敏感信息规则")],
        summary=_("SensitiveInfoRule List"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def list(self, request):
        ser = _SensitiveInfoArgsSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                name = ser.validated_data["name"]
                page = ser.validated_data["page"]
                page_size = ser.validated_data["page_size"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        users = self.get_auth_users(request.user)
        q = Q(user__in=users) & ~Q(status=-1)
        if name:
            strategys = IastStrategyModel.objects.filter(vul_name__icontains=name).all()
            q = Q(strategy__in=strategys) & q
        queryset = IastSensitiveInfoRule.objects.filter(q).order_by("-latest_time")
        page_summary, page_data = self.get_paginator(queryset, page, page_size)
        return R.success(
            data=SensitiveInfoRuleSerializer(page_data, many=True).data,
            page=page_summary,
        )

    @extend_schema_with_envcheck(
        request=SensitiveInfoRuleCreateSerializer,
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则创建"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def create(self, request):
        ser = SensitiveInfoRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                strategy_id = ser.validated_data["strategy_id"]
                pattern_type_id = ser.validated_data["pattern_type_id"]
                pattern = ser.validated_data["pattern"]
                status = ser.validated_data["status"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        strategy = IastStrategyModel.objects.filter(pk=strategy_id).first()
        pattern_type = IastPatternType.objects.filter(pk=pattern_type_id).first()
        pattern_test_dict = {1: regexcompile, 2: jqcompile}
        test = pattern_test_dict.get(pattern_type_id, None)
        if not test:
            return R.failure()
        status_ = test(pattern)
        if strategy and pattern_type and status_:
            obj = IastSensitiveInfoRule.objects.create(
                strategy=strategy,
                pattern_type=pattern_type,
                pattern=pattern,
                status=status,
                user=request.user,
            )
            return R.success(
                msg=_("create success"), data=SensitiveInfoRuleSerializer(obj).data
            )
        return R.failure()

    @extend_schema_with_envcheck(
        request=SensitiveInfoRuleCreateSerializer,
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则更新"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def update(self, request, pk):
        ser = SensitiveInfoRuleCreateSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                ser.validated_data["strategy_id"]
                ser.validated_data["pattern_type_id"]
                ser.validated_data["pattern"]
                ser.validated_data["status"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        users = self.get_auth_users(request.user)
        IastSensitiveInfoRule.objects.filter(pk=pk, user__in=users).update(
            **ser.validated_data, latest_time=time.time()
        )
        return R.success(msg=_("update success"))

    @extend_schema_with_envcheck(
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则删除"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def destory(self, request, pk):
        users = self.get_auth_users(request.user)
        IastSensitiveInfoRule.objects.filter(pk=pk, user__in=users).update(status=-1)
        return R.success(msg=_("delete success"))

    @extend_schema_with_envcheck(
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则获取"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def retrieve(self, request, pk):
        users = self.get_auth_users(request.user)
        obj = IastSensitiveInfoRule.objects.filter(pk=pk, user__in=users).first()
        if not obj:
            return R.failure()
        return R.success(data=SensitiveInfoRuleSerializer(obj).data)


class SensitiveInfoPatternTypeView(UserEndPoint):
    @extend_schema_with_envcheck(
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则模式类型列表"),
        description=_("Get the item corresponding to the user."),
    )
    def get(self, request):
        objs = IastPatternType.objects.all()
        return R.success(data=SensitiveInfoPatternTypeSerializer(objs, many=True).data)


class SensitiveInfoPatternValidationView(UserEndPoint):
    @extend_schema_with_envcheck(
        request=_RegexPatternValidationSerializer,
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则数据验证"),
        description=_(
            "Get the item corresponding to the user, support fuzzy search based on name."
        ),
    )
    def post(self, request, pattern_type):
        pattern_test_dict = {"regex": regextest, "json": jsontest}
        ser = _RegexPatternValidationSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                test_data = ser.validated_data["test_data"]
                pattern = ser.validated_data["pattern"]
            if pattern_type not in pattern_test_dict.keys():
                return R.failure()
        except ValidationError as e:
            return R.failure(data=e.detail)
        test = pattern_test_dict[pattern_type]
        data, status = test(test_data, pattern)
        return R.success(data={"status": status, "data": data})


def regexcompile(pattern):
    try:
        re.compile(pattern)
    except Exception as e:
        logger.debug(e, exc_info=e)
        logger.info("error:%s pattern: %s ", e, pattern)
        return False
    return True


def jqcompile(pattern):
    try:
        jq.compile(pattern)
    except Exception as e:
        logger.debug(e, exc_info=e)
        logger.info("error:%s pattern: %s ", e, pattern)
        return False
    return True


def regextest(test_data, pattern):
    try:
        regex = re.compile(pattern, re.M)
    except Exception as e:
        logger.debug(e, exc_info=e)
        logger.info("error:%s pattern: %s data: %s", e, pattern, test_data)
        data = ""
        status = 0
        return data, status
    result = regex.search(test_data)
    if result and (result.groups() or result.group()):
        return result.group(0), 1
    return "", 1


def jsontest(test_data, pattern):
    try:
        data = jq.compile(pattern).input(text=test_data).text()
        status = 1
    except Exception as e:
        logger.debug(e, exc_info=e)
        data = ""
        status = 0
    return data, status


class SensitiveInfoRuleBatchView(BatchStatusUpdateSerializerView):
    status_field = "status"
    model = IastSensitiveInfoRule

    @extend_schema_with_envcheck(
        request=BatchStatusUpdateSerializerView.serializer,
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则状态批量更新"),
        description=_("batch update status."),
    )
    def post(self, request):
        data = self.get_params(request.data)
        self.update_model(request, data)
        return R.success(msg="操作成功")
        return R.success(msg=_("update success"))


class SensitiveInfoRuleAllView(AllStatusUpdateSerializerView):
    status_field = "status"
    model = IastSensitiveInfoRule

    @extend_schema_with_envcheck(
        request=AllStatusUpdateSerializerView.serializer,
        tags=[_("敏感信息规则")],
        summary=_("敏感信息规则全部状态更新"),
        description=_("all update status."),
    )
    def post(self, request):
        data = self.get_params(request.data)
        self.update_model(request, data)
        return R.success(msg="操作成功")
        return R.success(msg=_("update success"))
