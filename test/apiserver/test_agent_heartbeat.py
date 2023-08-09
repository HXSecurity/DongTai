from test.apiserver.test_agent_base import AgentTestCase
from time import time
from django.core.cache import cache

from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_engine.tasks import is_alive
from dongtai_engine.tasks import update_agent_status


class ApiHeartBeatTestCase(AgentTestCase):
    def test_agent_heart_beat(self):
        data = {
            "detail": {
                "agentId": 28,
                "disk": '{"rate":71}',
                "memory": '{"total":"875MB","rate":7,"use":"65.872MB"}',
                "performance": '[{"metricsKey":"cpuUsage","collectDate":"2022-12-14 12:02:05.009","metricsValue":{"cpuUsagePercentage":0.16666666666667052}},{"metricsKey":"memoryUsage","collectDate":"2022-12-14 12:02:05.009","metricsValue":{"init":65011712,"systemMaxLimit":9223372036854771712,"committed":124256256,"memUsagePercentage":9.841756766183035,"max":917504000,"used":90298512}},{"metricsKey":"memoryNoHeapUsage","collectDate":"2022-12-14 12:02:05.009","metricsValue":{"init":4121784320,"systemMaxLimit":9223372036854771712,"committed":3886866432,"memUsagePercentage":94.30057786235646,"max":4121784320,"used":3886866432}},{"metricsKey":"garbageInfo","collectDate":"2022-12-14 12:02:05.009","metricsValue":{"collectionInfoList":[{"collectionTime":18049,"collectionCount":2715,"tenured":false,"collectionName":"PS Scavenge"},{"collectionTime":948,"collectionCount":4,"tenured":true,"collectionName":"PS MarkSweep"}]}},{"metricsKey":"threadInfo","collectDate":"2022-12-14 12:02:05.225","metricsValue":{"dongTaiThreadInfoList":[{"cpuUsage":0,"cpuTime":29161574907,"name":"DongTai-IAST-ServerConfigMonitor","id":14},{"cpuUsage":0,"cpuTime":27679480672,"name":"DongTai-IAST-ConfigMonitor","id":15},{"cpuUsage":0.035035544200697016,"cpuTime":13643355644,"name":"DongTai-IAST-PerformanceMonitor","id":16},{"cpuUsage":0,"cpuTime":111735614230,"name":"DongTai-IAST-EngineMonitor","id":17},{"cpuUsage":0,"cpuTime":61038194468,"name":"DongTai-IAST-HearBeatMonitor","id":18},{"cpuUsage":0,"cpuTime":303498408,"name":"DongTai-IAST-SecondFallbackMonitor","id":19},{"cpuUsage":0,"cpuTime":859911477,"name":"DongTai-IAST-DongTaiThreadMonitor","id":20},{"cpuUsage":0,"cpuTime":26344322815,"name":"DongTai-IAST-HeartBeat","id":64}],"threadCount":51,"dongTaiThreadCount":8,"daemonThreadCount":47,"peakThreadCount":53}}]',
                "returnQueue": 0,
                "cpu": '{"rate":0}',
            },
            "type": 1,
        }
        data["detail"]["agentId"] = self.agent_id
        self.agent_report(data, agentId=self.agent_id)
        self.assertTrue(is_alive(self.agent_id, int(time())))
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).cpu,
            data["detail"]["cpu"],
        )
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).memory,
            data["detail"]["memory"],
        )
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).disk,
            data["detail"]["disk"],
        )

    def test_agent_heart_beat_2(self):
        update_agent_status()
        self.assertFalse(is_alive(self.agent_id, int(time())))
        data = {
            "type": 1,
            "detail": {
                "agentId": 515,
                "memory": '{"total":"1.778GB","use":"295.194MB","rate":16}',
                "cpu": '{"rate":36}',
                "disk": '{"rate":72}',
                "returnQueue": 0,
            },
        }
        data["detail"]["agentId"] = self.agent_id
        self.agent_report(data, agentId=self.agent_id)
        self.assertTrue(is_alive(self.agent_id, int(time())))
        update_agent_status()
        cache.delete(f"heartbeat-{self.agent_id}")
        update_agent_status()
        self.assertFalse(is_alive(self.agent_id, int(time())))
        data = {
            "type": 1,
            "detail": {
                "agentId": 515,
                "memory": '{"total":"1.778GB","use":"295.194MB","rate":16}',
                "cpu": '{"rate":36}',
                "disk": '{"rate":72}',
                "returnQueue": 0,
            },
        }
        data["detail"]["agentId"] = self.agent_id
        self.agent_report(data, agentId=self.agent_id)
        self.assertTrue(is_alive(self.agent_id, int(time())))
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).cpu,
            data["detail"]["cpu"],
        )
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).memory,
            data["detail"]["memory"],
        )
        self.assertEqual(
            IastHeartbeat.objects.get(agent_id=self.agent_id).disk,
            data["detail"]["disk"],
        )
