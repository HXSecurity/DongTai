from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.base.project_version import (
    get_project_version,
    get_project_version_by_id,
)
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer


class _DocumentArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    version_id = serializers.IntegerField(default=1, help_text="项目版本id")


class ProjectSummaryDataTypeSummarySerializer(serializers.Serializer):
    type_name = serializers.CharField(help_text="漏洞类型")
    type_count = serializers.IntegerField(help_text="该类型的漏洞总数")
    type_level = serializers.IntegerField(help_text="该类型的危险等级")
    type_total_percentage = serializers.FloatField(help_text="该类型在总漏洞的数量占比")


_ProjectSummaryResponseSerializer = get_response_serializer(ProjectSummaryDataTypeSummarySerializer())


class ProjectSummaryVulType(UserEndPoint):
    @extend_schema_with_envcheck(
        [_DocumentArgsSerializer],
        tags=[_("Project")],
        summary=_("项目类型汇总列表"),
        description=_("Get project deatils and its statistics data about vulnerablity."),
        response_schema=_ProjectSummaryResponseSerializer,
    )
    def get(self, request, id):
        project = request.user.get_projects().filter(id=id).first()
        if not project:
            return R.failure(msg="项目不存在")
        ser = _DocumentArgsSerializer(data=request.GET)
        version_id = request.GET.get("version_id", None)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data["page_size"]
                page = ser.validated_data["page"]
        except ValidationError as e:
            return R.failure(data=e.detail)
        if not version_id:
            current_project_version = get_project_version(project.id)
        else:
            current_project_version = get_project_version_by_id(version_id)
        project_version_id = current_project_version.get("version_id", 0)
        if not project_version_id:
            return R.failure(msg="项目版本不存在")
        project_id = project.id
        queryset = (
            IastVulnerabilityModel.objects.filter(
                project_id=project_id, project_version_id=project_version_id, is_del=0
            )
            .values("strategy_id")
            .annotate(vul_count=Count("strategy_id"))
            .filter(vul_count__gt=0)
            .order_by("-vul_count")
        )
        data = {"type_summary": []}
        q = ~Q(hook_type_id=0)
        queryset = queryset.filter(q)
        page_info, queryset = self.get_paginator(queryset, page, page_size)
        typeArr = {}
        typeLevel = {}
        # strategy_ids = queryset.values_list("strategy_id", flat=True).distinct()
        strategy_ids = (i["strategy_id"] for i in queryset)
        strategys = {
            strategy["id"]: strategy
            for strategy in IastStrategyModel.objects.filter(pk__in=strategy_ids)
            .values("id", "vul_name", "level_id")
            .all()
        }
        if queryset:
            for one in queryset:
                hook_type_name = ""
                strategy = strategys.get(one["strategy_id"], None)
                strategy_name = strategy["vul_name"] if strategy else None
                type_ = list(filter(lambda x: x is not None, [strategy_name, hook_type_name]))
                one["type"] = type_[0] if type_ else ""
                typeArr[one["type"]] = one["vul_count"]
                typeLevel[one["type"]] = strategy["level_id"]
            typeArrKeys = typeArr.keys()
            data["type_summary"].extend(
                {
                    "type_name": item_type,
                    "type_count": typeArr[item_type],
                    "type_level": typeLevel[item_type],
                }
                for item_type in typeArrKeys
            )
        type_summary_total_count = sum(i["type_count"] for i in data["type_summary"])
        for type_summary in data["type_summary"]:
            type_summary["type_total_percentage"] = type_summary["type_count"] / type_summary_total_count
        return R.success(data=data["type_summary"], page=page_info)
