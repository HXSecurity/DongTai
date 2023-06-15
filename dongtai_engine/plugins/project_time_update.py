from celery_singleton import Singleton
from celery import shared_task
from time import time
from dongtai_common.models.project import IastProject

@shared_task(
    queue='dongtai-project-time-stamp-update',
    base=Singleton,
    lock_expiry=20,
)
def project_time_stamp_update(project_id):
    timestamp = int(time())
    IastProject.objects.filter(pk=project_id).update(latest_time=timestamp)
