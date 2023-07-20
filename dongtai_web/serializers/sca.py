#!/usr/bin/env python
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.asset_aggr import AssetAggr
from dongtai_common.models.project_version import IastProjectVersion
from rest_framework import serializers

from dongtai_common.models.asset import Asset
from dongtai_common.models.project import IastProject
from django.utils.translation import gettext_lazy as _
from dongtai_common.models.sca_maven_db import ScaMavenDb
from dongtai_web.dongtai_sca.models import (
    PackageLicenseLevel,
    PackageLicenseInfo,
    Package,
)


class ScaSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    package_name = serializers.SerializerMethodField()
    project_id = serializers.SerializerMethodField()
    project_version = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_type = serializers.SerializerMethodField()
    agent_name = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    license = serializers.SerializerMethodField()
    project_cache = {}
    project_version_cache = {}
    AGENT_LANGUAGE_MAP = {}

    class Meta:
        model = Asset
        fields = [
            "id",
            "package_name",
            "version",
            "project_name",
            "project_id",
            "project_version",
            "language",
            "package_path",
            "agent_name",
            "signature_value",
            "level",
            "level_type",
            "vul_count",
            "dt",
            "license",
        ]

    def get_project_name(self, obj):
        project_id = obj.agent.bind_project_id
        if project_id == 0:
            return _("The application has not been binded")
        else:
            if project_id in self.project_cache:
                return self.project_cache[project_id]
            else:
                project = IastProject.objects.filter(id=project_id).first()

                self.project_cache[project_id] = project.name if project else ""
                return self.project_cache[project_id]

    def get_project_id(self, obj):
        return obj.agent.bind_project_id

    def get_project_version(self, obj):
        project_version_id = obj.agent.project_version_id
        if project_version_id:
            if project_version_id in self.project_version_cache:
                return self.project_version_cache[project_version_id]
            else:
                project_version = (
                    IastProjectVersion.objects.values("version_name")
                    .filter(id=project_version_id)
                    .first()
                )
                self.project_version_cache[project_version_id] = project_version[
                    "version_name"
                ]

            return self.project_version_cache[project_version_id]
        else:
            return _("No application version has been created")

    def get_level_type(self, obj):
        return obj.level.id

    def get_level(self, obj):
        return obj.level.name_value

    def get_agent_name(self, obj):
        return obj.agent.token

    def get_language(self, obj):
        if obj.agent_id not in self.AGENT_LANGUAGE_MAP:
            agent_model = IastAgent.objects.filter(id=obj.agent_id).first()
            if agent_model:
                self.AGENT_LANGUAGE_MAP[obj.agent_id] = agent_model.language
        return self.AGENT_LANGUAGE_MAP[obj.agent_id]

    def get_license(self, obj):
        try:
            if "license_dict" not in self.context:
                sca_package = Package.objects.filter(hash=obj.signature_value).first()
                return sca_package.license
            return self.context["license_dict"].get(obj.signature_value, "")
        except Exception:
            return ""

    def get_package_name(self, obj):
        if obj.package_name.startswith("maven:") and obj.package_name.endswith(":"):
            return obj.package_name.replace("maven:", "", 1)[:-1]
        return obj.package_name


class ScaAssetSerializer(serializers.ModelSerializer):
    package_name = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()
    level_type = serializers.SerializerMethodField()
    license = serializers.SerializerMethodField()
    license_level = serializers.SerializerMethodField()
    license_desc = serializers.SerializerMethodField()
    vul_high_count = serializers.SerializerMethodField()
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = [
            "id",
            "package_name",
            "version",
            "safe_version",
            "last_version",
            "language",
            "signature_value",
            "level",
            "level_type",
            "vul_count",
            "vul_high_count",
            "vul_medium_count",
            "vul_low_count",
            "vul_info_count",
            "project_count",
            "safe_version_list",
            "nearest_safe_version",
            "license",
            "latest_safe_version",
            "license_list",
            "highest_license",
            "license_level",
            "license_desc",
        ]

    def get_level_type(self, obj):
        return obj.level.id

    def get_level(self, obj):
        return obj.level.name_value

    def get_package_name(self, obj):
        if obj.package_name.startswith("maven:") and obj.package_name.endswith(":"):
            return obj.package_name.replace("maven:", "", 1)[:-1]
        return obj.package_name

    def get_license(self, obj):
        if not obj.license:
            obj.license = "未知"
        return obj.license

    def get_license_level(self, obj):
        obj.license_level = 0
        obj.license_desc = "允许商业集成"
        if obj.license:
            license_level = PackageLicenseLevel.objects.filter(
                identifier=obj.license
            ).first()
            obj.license_level = license_level.level_id if license_level else 0
            obj.license_desc = license_level.level_desc if license_level else "允许商业集成"

        return obj.license_level

    def get_license_desc(self, obj):
        return obj.license_desc

    def get_vul_high_count(self, obj):
        return obj.vul_high_count + obj.vul_critical_count

    def get_project_count(self, obj):
        return (
            Asset.objects.filter(
                signature_value=obj.signature_value,
                version=obj.version,
                project_id__gt=0,
            )
            .values("project_id")
            .distinct()
            .count()
        )
