from dongtai_common.models.agent import IastAgent
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
from asgiref.sync import sync_to_async
import asyncio
from typing import List, Tuple
#import asyncio_gevent

DELETE_BATCH_SIZE = 10000


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


@shared_task(queue='dongtai-periodic-task',
             time_limit=60 * 60 * 2,
             soft_time_limit=60 * 60 * 4)
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
        latest_id = MethodPool.objects.filter(
            update_time__lte=delete_time_stamp).order_by('-id').values_list(
            'id', flat=True).first()
        first_id = MethodPool.objects.filter(
            update_time__lte=delete_time_stamp).order_by('id').values_list(
            'id', flat=True).first()
        if not any([latest_id, first_id]):
            logger.info("no data for clean up")
        if all([latest_id, first_id]):
            assert isinstance(latest_id, int)
            assert isinstance(first_id, int)
            batch_clean(latest_id, first_id, 10000)
            # qs = MethodPool.objects.filter(pk__lte=latest_id)
            # qs._raw_delete(qs.db)

        logger.info(f'Delete offline agent 30 days ago')
        agent_latest_id = IastAgent.objects.filter(
            latest_time__lte=delete_time_stamp).order_by('-id').values_list(
            'id', flat=True).first()
        if any([agent_latest_id]):
            IastAgent.objects.filter(pk__lte=agent_latest_id,
                                     online=0).delete()


@sync_to_async(thread_sensitive=False)
def data_clean_batch(upper_id: int, lower_id: int):
    qs = MethodPool.objects.filter(pk__lt=upper_id, pk__gte=lower_id)
    logger.info(f"data cleaning {upper_id}-{lower_id} ")
    qs._raw_delete(qs.db)


#@asyncio_gevent.async_to_sync
async def loop_main(range_list: List[Tuple[int, int]]):
    coros = [
        data_clean_batch(upper_id, lower_id)
        for upper_id, lower_id in range_list
    ]
    await asyncio.gather(*coros)


def batch_clean(upper_id: int, lower_id: int, batch_size: int):
    chunk_range = list(
        zip(range(lower_id + batch_size, upper_id + batch_size, batch_size),
            range(lower_id, upper_id, batch_size)))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loop_main(chunk_range))
