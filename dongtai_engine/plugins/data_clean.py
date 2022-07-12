from dongtai_common.models.vulnerablity import IastVulnerabilityModel, IastVulnerabilityDocument
from celery import shared_task
from django.apps import apps
from django.db import transaction
from dongtai_common.models.asset import Asset, IastAssetDocument
from dongtai_common.models.asset_vul import IastVulAssetRelation, IastAssetVulnerabilityDocument
from dongtai_common.models.agent_method_pool import MethodPool
from time import time
from celery.apps.worker import logger
from dongtai_conf.settings import ELASTICSEARCH_STATE

DELETE_BATCH_SIZE = 20000


def chunked_queryset(queryset, chunk_size):
    """ Slice a queryset into chunks. """

    start_pk = 0
    queryset = queryset.order_by('pk')

    while True:
        # No entry left
        if not queryset.filter(pk__gt=start_pk).exists():
            break

        try:
            # Fetch chunk_size entries if possible
            end_pk = queryset.filter(pk__gt=start_pk).values_list(
                'pk', flat=True)[chunk_size - 1]

            # Fetch rest entries if less than chunk_size left
        except IndexError:
            end_pk = queryset.values_list('pk', flat=True).last()

        yield queryset.filter(pk__gt=start_pk).filter(pk__lte=end_pk)

        start_pk = end_pk


@shared_task(queue='dongtai-periodic-task')
def data_cleanup(days: int):
    delete_time_stamp = int(time()) - 60 * 60 * 24 * days
    if ELASTICSEARCH_STATE:
        # use delete to trigger the signal to delete related elasticsearch doc
        qs = MethodPool.objects.filter(update_time__lte=delete_time_stamp)
        for i in chunked_queryset(qs, DELETE_BATCH_SIZE):
            i.delete()
    else:
        # use _raw_delete to reduce the delete time and memory usage.
        # it could aviod to load every instance into memory.
        qs = MethodPool.objects.filter(update_time__lte=delete_time_stamp)
        qs._raw_delete(qs.db)
