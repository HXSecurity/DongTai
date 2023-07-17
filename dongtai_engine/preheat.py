from importlib import import_module
from celery import shared_task
from celery.apps.worker import logger
from dongtai_common.common.utils import make_hash
from django.core.cache import cache
import random
from datetime import datetime, timedelta
from django.db.utils import OperationalError
from django.db import connection as conn

# def function_preheat(func__module__: str, func__name__: str, *args, **kwargs):
#    module = import_module(func__module__)
#    func = getattr(module, func__name__)
#    try:
#        func(*args, **kwargs)
#    except Exception as e:
#        logger.error(e, exc_info=True)


@shared_task(queue='dongtai-periodic-task')
def function_preheat():
    from dongtai_common.models.log import IastLog
    time_threshold = datetime.now() - timedelta(hours=1)
    need_preheat = IastLog.objects.filter(
        action_time__gt=time_threshold).exists()
    if need_preheat:
        time_min = datetime.now() - timedelta(hours=72)
        user_ids = list(
            IastLog.objects.filter(action_time__gt=time_min).values_list(
                'user__id', flat=True).distinct().order_by('user__id').all())
        logger.info(f"user_ids: {user_ids}")
        for user_id in user_ids:
            for func in PreHeatRegister.functions:
                try:
                    func(user_id)
                except OperationalError as e:
                    logger.error(e, exc_info=True)
                    logger.error(f'user_id: {user_id}')
                    logger.error(f'function name : {func.__name__}')
                    logger.error(f'latest 5 query:{conn.queries[-5:]}')
                except Exception as e:
                    logger.error(e, exc_info=True)
                    continue


class PreHeatException(Exception):
    pass


class PreHeatRegister:
    functions = []

    @classmethod
    def register(cls, function):
        annotation_dict = function.__annotations__.copy()
        if 'return' in annotation_dict:
            del annotation_dict['return']

        if annotation_dict == {'user_id': int} or annotation_dict == {'user_id': 'int'}:
            pass
        else:
            logger.info(f'{function.__name__} annotations not fit in')
            raise PreHeatException(
                'function {function.__name__} is not fit in , please  annotation user_id :int in params'
            )
        if function in cls.functions:
            logger.info(
                f'{function.__name__} already in PreHeatRegister.functions')
            return
        cls.functions.append(function)
        logger.debug(f"preheat functions {PreHeatRegister.functions}")


@shared_task(queue='dongtai-function-flush-data')
def function_flush(func__module__, func__name__, cache_time, args, kwargs):
    module = import_module(func__module__)
    func = getattr(module, func__name__)
    if not getattr(func, '__origin__name__', None) == 'cached':
        logger.error(
            'this function is not supported , please use cached to warp function.'
        )
        return
    origin_func = func.__wrapped__
    random_range = func.__random_range__
    try:
        res = origin_func(*args, **kwargs)
        cache_key = make_hash((origin_func.__module__ + origin_func.__name__,
                               tuple(args), kwargs))
        logger.debug(cache_key)
        if random_range:
            cache_time = random.randint(*random_range)
        cache.set(cache_key, res, cache_time)
    except Exception as e:
        logger.error(e, exc_info=True)
