#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/8/25 下午4:14
# project: dongtai-engine

import logging

from dongtai.endpoint import R, AnonymousAndUserEndPoint

logger = logging.getLogger('dongtai-engine')


class HealthEndPoint(AnonymousAndUserEndPoint):
    def get(self, request):
        import redis
        mock_data = {
            "dongtai_engine": {
                "status": 1
            },
            "engine_monitoring_indicators": [
                {
                    "key": "dongtai-replay-vul-scan",
                    "value": 0,
                    "name": "dongtai-replay-vul-scan"
                },
                {
                    "key": "dongtai_method_pool_scan",
                    "value": 0,
                    "name": "dongtai-method-pool-scan"
                },
            ],
        }
        # 读取数据库中的redis键，然后查找队列大小
        from dongtai.models.engine_monitoring_indicators import IastEnginMonitoringIndicators
        monitor_models = IastEnginMonitoringIndicators.objects.all()
        if monitor_models.values('id').count() > 0:
            from lingzhi_engine import settings
            redis_cli = redis.StrictRedis(
                host=settings.config.get("redis", 'host'),
                password=settings.config.get("redis", 'password'),
                port=settings.config.get("redis", 'port'),
                db=settings.config.get("redis", 'db'),
            )

            monitor_models = monitor_models.values('key', 'name', 'name_en', 'name_zh')
            mock_data['engine_monitoring_indicators'] = list()
            for monitor_model in monitor_models:
                mock_data['engine_monitoring_indicators'].append({
                    'key': monitor_model['key'],
                    'name': monitor_model['name'],
                    'name_en': monitor_model['name_en'],
                    'name_zh': monitor_model['name_zh'],
                    'value': redis_cli.llen(monitor_model['key'])
                })
        return R.success(data=mock_data)
