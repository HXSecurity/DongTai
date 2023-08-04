#!/usr/bin/env python
from collections import defaultdict
from typing import TYPE_CHECKING

from django.db.models import Count, Q, QuerySet
from rest_framework import serializers

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.project import IastProject
from dongtai_common.models.vulnerablity import IastVulnerabilityModel

if TYPE_CHECKING:
    from django.core.paginator import _SupportsPagination


def get_vul_levels_dict(queryset: "QuerySet | _SupportsPagination", exclude_vul_status: int | None) -> defaultdict:
    vul_levels = (
        IastVulnerabilityModel.objects.values("level__name_value", "level", "project_id")
        .filter(
            ~Q(status_id=exclude_vul_status) if exclude_vul_status is not None else Q(),
            project_id__in=list(queryset.values_list("id", flat=True)),
            is_del=0,
        )
        .annotate(total=Count("level"))
    )
    vul_levels_dict = defaultdict(list)
    for k in vul_levels:
        k["agent__bind_project_id"] = k["project_id"]
        vul_levels_dict[k["agent__bind_project_id"]].append(k)
    return vul_levels_dict


def get_project_language(queryset: "QuerySet | _SupportsPagination") -> defaultdict:
    project_languages = (
        IastAgent.objects.values("bind_project_id", "language")
        .filter(bind_project_id__in=list(queryset.values_list("id", flat=True)))
        .distinct()
    )
    project_language_dict = defaultdict(list)
    for k in project_languages:
        project_language_dict[k["bind_project_id"]].append(k["language"])
    return project_language_dict


def get_agent_count(queryset: "QuerySet | _SupportsPagination") -> defaultdict:
    agent_counts = (
        IastAgent.objects.values("bind_project_id")
        .filter(bind_project_id__in=list(queryset.values_list("id", flat=True)))
        .annotate(agent_count=Count("id"))
    )
    agent_count_dict = defaultdict(int)
    for k in agent_counts:
        agent_count_dict[k["bind_project_id"]] = k["agent_count"]
    return agent_count_dict


class BaseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = IastProject
        fields = [
            "id",
            "name",
            "mode",
            "latest_time",
            "vul_validation",
            "status",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        if "exclude_vul_status" in kwargs:
            self.exclude_vul_status = kwargs.pop("exclude_vul_status")
        else:
            self.exclude_vul_status = None
        super().__init__(*args, **kwargs)

    vul_count = serializers.SerializerMethodField(help_text="Vulnerability Count")
    agent_count = serializers.SerializerMethodField(help_text="Agent Count")
    owner = serializers.SerializerMethodField(help_text="Project owner")
    agent_language = serializers.SerializerMethodField(help_text="Agent language currently included in the project")
    project_group_name = serializers.SerializerMethodField(help_text="项目组名称列表")
    USER_MAP = {}

    class Meta:
        model = IastProject
        fields = [
            "id",
            "name",
            "mode",
            "vul_count",
            "agent_count",
            "owner",
            "latest_time",
            "agent_language",
            "vul_validation",
            "status",
            "project_group_name",
        ]

    def get_agents(self, obj):
        try:
            all_agents = obj.project_agents
        except Exception:
            all_agents = obj.iastagent_set.all()
            obj.project_agents = all_agents
        return all_agents

    def get_vul_count(self, obj) -> list:
        if "vul_levels_dict" in self.context:
            vul_levels = self.context["vul_levels_dict"][obj.id]
        else:
            vul_levels = (
                IastVulnerabilityModel.objects.values("level__name_value", "level")
                .filter(
                    Q(status_id=self.exclude_vul_status) if self.exclude_vul_status is not None else Q(),
                    project_id=obj.id,
                    is_del=0,
                )
                .annotate(total=Count("level"))
            )
        for vul_level in vul_levels:
            vul_level["name"] = vul_level["level__name_value"]
        return list(vul_levels) if vul_levels else []

    def get_owner(self, obj) -> str:
        if obj not in self.USER_MAP:
            self.USER_MAP[obj] = obj.user.get_username()
        return self.USER_MAP[obj]

    def get_agent_language(self, obj) -> list:
        if "project_language_dict" in self.context:
            res = self.context["project_language_dict"][obj.id]
        else:
            res = obj.iastagent_set.values_list("language", flat=True).distinct()
        return list(res)

    def get_agent_count(self, obj) -> int:
        if "agent_count_dict" in self.context:
            res = self.context["agent_count_dict"][obj.id]
        else:
            res = obj.iastagent_set.count()
        return res

    def get_project_group_name(self, obj: IastProject) -> list:
        if "project_group_name" in self.context:
            res = self.context["project_group_name"][obj.id]
        else:
            res = (x.name for x in obj.iastprojectgroup_set.all())
        return list(res)
