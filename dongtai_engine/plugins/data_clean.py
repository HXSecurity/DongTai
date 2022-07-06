from dongtai_common.models.vulnerablity import IastVulnerabilityModel, IastVulnerabilityDocument
from celery import shared_task
from django.apps import apps
from django.db import transaction
from dongtai_common.models.asset import Asset, IastAssetDocument
from dongtai_common.models.asset_vul import IastVulAssetRelation, IastAssetVulnerabilityDocument
from dongtai_common.models.agent_method_pool import MethodPool
from time import time
from celery.apps.worker import logger


#@shared_task
def data_cleanup(days: int):
    delete_time_stamp = int(time()) - 60 * 60 * 24 * days
    MethodPool.objects.filter(update_time__lte=delete_time_stamp).delete()
