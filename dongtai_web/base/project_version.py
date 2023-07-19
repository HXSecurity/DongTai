import time

from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion


class VersionModifySerializer(serializers.Serializer):
    version_id = serializers.CharField(help_text=_("The version id of the project"))
    version_name = serializers.CharField(help_text=_("The version name of the project"))
    description = serializers.CharField(
        help_text=_("Description of the project versoin")
    )
    project_id = serializers.IntegerField(help_text=_("The id of the project"))
    current_version = serializers.IntegerField(
        help_text=_("Whether it is the current version, 1 means yes, 0 means no.")
    )


@transaction.atomic
def version_modify(user, department, versionData=None):
    version_id = versionData.get("version_id", 0)
    project_id = versionData.get("project_id", 0)
    current_version = versionData.get("current_version", 0)
    version_name = versionData.get("version_name", "")
    description = versionData.get("description", "")
    project = (
        IastProject.objects.filter(department__in=department, id=project_id)
        .only("id", "user")
        .first()
    )
    if not version_name or not project:
        return {"status": "202", "msg": _("Parameter error")}
    baseVersion = IastProjectVersion.objects.filter(
        project_id=project.id,
        version_name=version_name,
        status=1,
    )
    if version_id:
        baseVersion = baseVersion.filter(~Q(id=version_id))
    existVersion = baseVersion.exists()
    if existVersion:
        return {"status": "202", "msg": _("Repeated version name")}
    if version_id:
        version = IastProjectVersion.objects.filter(
            id=version_id, project_id=project.id, status=1
        ).first()
        if not version:
            return {"status": "202", "msg": _("Version does not exist")}
        version.update_time = int(time.time())
        version.version_name = version_name
        version.description = description
        version.save()
    else:
        version, created = IastProjectVersion.objects.get_or_create(
            project_id=project.id,
            user=project.user,
            current_version=current_version,
            version_name=version_name,
            description=description,
        )
    version.status = 1
    version.save()
    return {
        "status": "201",
        "msg": "success",
        "data": {
            "version_id": version.id,
            "version_name": version_name,
            "description": description,
        },
    }


def get_project_version(project_id, auth_users=None):
    versionInfo = IastProjectVersion.objects.filter(
        project_id=project_id,
        current_version=1,
    ).first()
    if versionInfo:
        current_project_version = {
            "version_id": versionInfo.id,
            "version_name": versionInfo.version_name,
            "description": versionInfo.description,
        }
    else:
        current_project_version = {
            "version_id": 0,
            "version_name": "",
            "description": "",
        }
    return current_project_version


def get_project_version_by_id(version_id):
    versionInfo = IastProjectVersion.objects.filter(pk=version_id).first()
    if versionInfo:
        current_project_version = {
            "version_id": versionInfo.id,
            "version_name": versionInfo.version_name,
            "description": versionInfo.description,
        }
    else:
        current_project_version = {
            "version_id": 0,
            "version_name": "",
            "description": "",
        }
    return current_project_version


class ProjectsVersionDataSerializer(serializers.Serializer):
    description = serializers.CharField(help_text=_("Description of the project"))
    version_id = serializers.CharField(help_text=_("The version id of the project"))
    version_name = serializers.CharField(help_text=_("The version name of the project"))
