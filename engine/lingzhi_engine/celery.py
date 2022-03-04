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
    Queue("dongtai-method-pool-scan", Exchange("dongtai-method-pool-scan"), routing_key="dongtai-method-pool-scan"),
    Queue("dongtai-replay-vul-scan", Exchange("dongtai-replay-vul-scan"), routing_key="dongtai-replay-vul-scan"),
    Queue("dongtai-strategy-scan", Exchange("dongtai-strategy-scan"), routing_key="dongtai-strategy-scan"),
    Queue("dongtai-search-scan", Exchange("dongtai-search-scan"), routing_key="dongtai-search-scan"),
    Queue("dongtai-periodic-task", Exchange("dongtai-periodic-task"), routing_key="dongtai-periodic-task"),
    Queue("dongtai-replay-task", Exchange("dongtai-replay-task"), routing_key="dongtai-replay-task"),
    Queue("dongtai-sca-task", Exchange("dongtai-sca-task"), routing_key="dongtai-sca-task"),
]
configs["CELERY_ROUTES"] = {
    "core.tasks.search_vul_from_method_pool": {'exchange': 'dongtai-method-pool-scan', 'routing_key': 'dongtai-method-pool-scan'},
    "core.tasks.search_vul_from_strategy": {'exchange': 'dongtai-strategy-scan', 'routing_key': 'dongtai-strategy-scan'},
    "core.tasks.search_vul_from_replay_method_pool": {'exchange': 'dongtai-replay-vul-scan', 'routing_key': 'dongtai-replay-vul-scan'},
    "core.tasks.search_sink_from_method_pool": {'exchange': 'dongtai-search-scan', 'routing_key': 'dongtai-search-scan'},
    "core.tasks.update_sca": {'exchange': 'dongtai-periodic-task', 'routing_key': 'dongtai-periodic-task'},
    "core.tasks.update_agent_status": {'exchange': 'dongtai-periodic-task', 'routing_key': 'dongtai-periodic-task'},
    "core.tasks.heartbeat": {'exchange': 'dongtai-periodic-task', 'routing_key': 'dongtai-periodic-task'},
    "core.tasks.clear_error_log": {'exchange': 'dongtai-periodic-task', 'routing_key': 'dongtai-periodic-task'},
    "core.tasks.export_report": {'exchange': 'dongtai-periodic-task', 'routing_key': 'dongtai-periodic-task'},
    "core.tasks.vul_recheck": {'exchange': 'dongtai-replay-task', 'routing_key': 'dongtai-replay-task'},
}
configs["CELERY_ENABLE_UTC"] = False
configs["CELERY_TIMEZONE"] = settings.TIME_ZONE
configs["DJANGO_CELERY_BEAT_TZ_AWARE"] = False
configs["CELERY_BEAT_SCHEDULER"] = 'django_celery_beat.schedulers:DatabaseScheduler'

app.namespace = 'CELERY'
app.conf.update(configs)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
