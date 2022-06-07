from test.apiserver.test_agent_base import AgentTestCase,gzipdata
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
import gzip
import base64
from dongtai_protocol.report.report_handler_factory import ReportHandler
import json
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from django.test import TestCase
from dongtai_engine.tasks import search_vul_from_method_pool
from dongtai_protocol.tests import download_if_not_exist
from django.db import connections


class CoreScanTestCase(AgentTestCase):

    def setUp(self):
        res = download_if_not_exist(
            "https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/test_data/iast_agent_method_pool.sql",
            "/tmp/test_core_iast_agent_method_pool.sql")
        super().setUp()
        cursor = connections['default'].cursor()
        sqlfile = ""
        with open('/tmp/test_core_iast_agent_method_pool.sql') as f:
            for line in f:
                sqlfile += line
        cursor.execute(sqlfile)

    def test_benchmark_method_pool_scan(self):
        data = MethodPool.objects.filter(agent_id=self.agent_id).all()
        vul_count_begin = IastVulnerabilityModel.objects.filter(
            agent_id=self.agent_id).all().count()
        for method_pool in data:
            method_pool.agent_id = self.agent_id
            method_pool.save()
            search_vul_from_method_pool(method_pool.pool_sign,
                                        method_pool.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                url=method_pool.url, agent_id=self.agent_id).exists()
        vul_count_after = IastVulnerabilityModel.objects.filter(
            agent_id=self.agent_id).all().count()
        assert len(data) == vul_count_after - vul_count_begin


class CoreTaskTestCase(AgentTestCase):

    def test_search_method_pool(self):
        method_pool_id = 4439061 
        method_pool = MethodPool.objects.filter(pk=method_pool_id).first()
        from dongtai_engine.tasks import search_vul_from_method_pool
        search_vul_from_method_pool(method_pool.pool_sign, method_pool.agent_id)
