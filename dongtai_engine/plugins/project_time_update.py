from celery_singleton import Singleton
from celery import shared_task
from time import time
from dongtai_common.models.project import IastProject
from dongtai_common.models.project_version import IastProjectVersion


@shared_task(
    queue='dongtai-project-time-stamp-update',
    base=Singleton,
    lock_expiry=20,
)
def project_time_stamp_update(project_id):
    timestamp = int(time())
    IastProject.objects.filter(pk=project_id).update(latest_time=timestamp)


@shared_task(
    queue='dongtai-project-time-stamp-update',
    base=Singleton,
    lock_expiry=20,
)
def project_version_time_stamp_update(project_version_id):
    timestamp = int(time())
    IastProjectVersion.objects.filter(pk=project_version_id).update(
        update_time=timestamp)
from dongtai_engine.plugins.project_time_update import (
    project_time_stamp_update,
    project_version_time_stamp_update,
)
