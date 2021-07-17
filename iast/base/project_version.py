import time
from django.db.models import Q
from dongtai.models.project_version import IastProjectVersion


def version_modify(user, versionData=None):
    if versionData is None:
        return {
            "status": "202",
            "msg": "参数错误"
        }
    version_id = versionData.get("version_id", 0)
    project_id = versionData.get("project_id", 0)
    current_version = versionData.get("current_version", 0)
    version_name = versionData.get("version_name", "")
    description = versionData.get("description", "")
    if not version_name or not project_id:
        return {
            "status": "202",
            "msg": "参数错误"
        }
    baseVersion = IastProjectVersion.objects.filter(
             project_id=project_id,
             version_name=version_name,
             user=user,
             status=1
         )
    if version_id:
         baseVersion = baseVersion.filter(~Q(id=version_id))
    existVersion = baseVersion.exists()
    if existVersion:
        return {
            "status": "202",
            "msg": "版本名称重复"
        }
    if version_id:
        version = IastProjectVersion.objects.filter(id=version_id, project_id=project_id, user=user, status=1).first()
        if not version:
            return {
                "status": "202",
                "msg": "版本不存在"
            }
        else:
            version.update_time = int(time.time())
    else:
        version = IastProjectVersion.objects.create(project_id=project_id, user=user, status=1, current_version=current_version)
    version.version_name = version_name
    version.description = description
    version.save()
    return {
        "status": "201",
        "msg": "success",
        "data": {
            "version_id": version.id,
            "version_name": version_name,
            "description": description
        }
    }


# 获取项目版本信息
def get_project_version(project_id,auth_users):
    versionInfo = IastProjectVersion.objects.filter(project_id=project_id, status=1, current_version=1, user__in=auth_users).first()
    if versionInfo:
        current_project_version = {
            "version_id": versionInfo.id,
            "version_name": versionInfo.version_name,
            "description": versionInfo.description
        }
    else:
        current_project_version = {
            "version_id": 0,
            "version_name": "",
            "description": "",
        }
    return current_project_version
