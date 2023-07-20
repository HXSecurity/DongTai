import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_mock(self):
        import redis

        mock_data = {
            "dongtai_engine": {"status": 1},
            "engine_monitoring_indicators": [
                {
                    "key": "dongtai-replay-vul-scan",
                    "value": 11,
                    "name": "dongtai-replay-vul-scan",
                },
                {
                    "key": "dongtai_method_pool_scan",
                    "value": 11,
                    "name": "dongtai-method-pool-scan",
                },
            ],
        }
        # 读取数据库中的redis键，然后查找队列大小
        from dongtai_common.models.engine_monitoring_indicators import (
            IastEnginMonitoringIndicators,
        )

        monitor_models = IastEnginMonitoringIndicators.objects.all()
        if monitor_models.values("id").count() > 0:
            from dongtai_conf import settings

            redis_cli = redis.StrictRedis(
                host=settings.config.get("redis", "host"),
                password=settings.config.get("redis", "password"),
                port=settings.config.get("redis", "port"),
                db=settings.config.get("redis", "db"),
            )

            monitor_models = monitor_models.values("key", "name")
            mock_data["engine_monitoring_indicators"] = list()
            for monitor_model in monitor_models:
                mock_data["engine_monitoring_indicators"].append(
                    {
                        "key": monitor_model["key"],
                        "name": monitor_model["name"],
                        "value": redis_cli.llen(monitor_model["key"]),
                    }
                )
        print(mock_data)


if __name__ == "__main__":
    unittest.main()
