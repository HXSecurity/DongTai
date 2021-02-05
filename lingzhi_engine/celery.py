#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/26 下午7:27
# software: PyCharm
# project: lingzhi-engine

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
from kombu import Queue, Exchange

from lingzhi_engine import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lingzhi_engine.settings')

app = Celery('lingzhi-engine')

configs = {k: v for k, v in settings.__dict__.items() if k.startswith('CELERY')}
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

configs["CELERY_QUEUES"] = [
    Queue("vul-scan-method-pool", Exchange("method_pool"), routing_key="method_pool"),
    Queue("vul-scan-strategy", Exchange("strategy"), routing_key="strategy"),
    Queue("vul-scan-search", Exchange("search"), routing_key="search"),
]
configs["CELERY_ROUTES"] = {
    "core.tasks.search_vul_from_method_pool": {'exchange': 'method_pool', 'routing_key': 'method_pool'},
    "core.tasks.search_vul_from_strategy": {'exchange': 'strategy', 'routing_key': 'strategy'},
    "core.tasks.search_sink_from_method_pool": {'exchange': 'search', 'routing_key': 'search'},
}

app.namespace = 'CELERY'
app.conf.update(configs)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
