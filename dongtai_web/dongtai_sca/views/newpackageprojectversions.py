import logging
from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.assetv2 import AssetV2
from dongtai_common.models.project import IastProject
from dongtai_web.utils import extend_schema_with_envcheck_v2, get_response_serializer

logger = logging.getLogger(__name__)


@dataclass
class RelationProjectVersion:
    project_version_name: str
    package_path: str


class RelationProjectVersionArgsSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20, help_text=_("Number per page"))
    page = serializers.IntegerField(default=1, help_text=_("Page index"))
    project_id = serializers.IntegerField(help_text=_("project with be the first"))


class RelationProjectVersionSerializer(serializers.ModelSerializer):
    project_version_name = serializers.CharField(source="project_version.version_name")

    class Meta:
        model = AssetV2
        fields = ["project_version_name", "project_version_id", "package_path"]


FullRelationProjectVersionResponseSerializer = get_response_serializer(RelationProjectVersionSerializer(many=True))


class NewPackageRelationProjectVersion(UserEndPoint):
    @extend_schema_with_envcheck_v2(
        request=RelationProjectVersionArgsSerializer,
        tags=[_("Component")],
        summary="组件相关的项目版本",
        responses={200: FullRelationProjectVersionResponseSerializer},
    )
    def get(self, request, language_id, package_name, package_version, project_id):
        departments = request.user.get_relative_department()
        queryset = IastProject.objects.filter(department__in=departments).order_by("-latest_time")
        assets = (
            AssetV2.objects.filter(
                language_id=language_id,
                package_name=package_name,
                version=package_version,
                project_id__in=queryset,
                project_id=project_id,
            )
            .order_by("-dt")
            .select_related("project_version")
            .all()
        )
        return R.success(
            data=RelationProjectVersionSerializer(assets, many=True).data,
        )
