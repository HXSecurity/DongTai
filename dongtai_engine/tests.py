from test.apiserver.test_agent_base import AgentTestCase, gzipdata
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
from django.test import TestCase
from dongtai_common.models.user import User
import unittest


@unittest.skip("waiting for rebuild mock data")
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
        data = MethodPool.objects.all()
        vul_count_begin = IastVulnerabilityModel.objects.all().count()
        for method_pool in data:
            method_pool.agent_id = self.agent_id
            method_pool.save()
            search_vul_from_method_pool(method_pool.pool_sign,
                                        method_pool.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                url=method_pool.url, agent_id=self.agent_id).exists()
        vul_count_after = IastVulnerabilityModel.objects.all().count()
        assert len(data) == vul_count_after - vul_count_begin

    def test_params_empty_count(self):
        data = MethodPool.objects.all()
        vul_count_without_param_mark_begin = IastVulnerabilityModel.objects.filter(
            param_name='{}', level_id__lte=2).all().count()
        for method_pool in data:
            method_pool.agent_id = self.agent_id
            method_pool.save()
            search_vul_from_method_pool(method_pool.pool_sign,
                                        method_pool.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                url=method_pool.url, agent_id=self.agent_id).exists()
        vul_count_without_param_mark_after = IastVulnerabilityModel.objects.filter(param_name='{}',
                                                                                   level_id__lte=2).all().count()
        res = vul_count_without_param_mark_after - vul_count_without_param_mark_begin
        print([
            i.uri for i in IastVulnerabilityModel.objects.filter(
                param_name='{}', level_id__lte=2).all()
        ])
        assert res == 0

    def test_params_single_uri(self):
        data = MethodPool.objects.filter(uri='/benchmark/cmdi-00/BenchmarkTest00573').all()
        vul_count_without_param_mark_begin = IastVulnerabilityModel.objects.filter(
            param_name='{}', level_id__lte=2).all().count()
        for method_pool in data:
            method_pool.agent_id = self.agent_id
            method_pool.save()
            search_vul_from_method_pool(method_pool.pool_sign,
                                        method_pool.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                url=method_pool.url, agent_id=self.agent_id).exists()
        vul_count_without_param_mark_after = IastVulnerabilityModel.objects.filter(param_name='{}',
                                                                                   level_id__lte=2).all().count()
        res = vul_count_without_param_mark_after - vul_count_without_param_mark_begin
        print([
            i.uri for i in IastVulnerabilityModel.objects.filter(
                param_name='{}', level_id__lte=2).all()
        ])
        assert res == 0


@unittest.skip("waiting for rebuild mock data")
class CoreTaskTestCase(AgentTestCase):

    def test_search_method_pool(self):
        method_pool_id = 4439061
        method_pool = MethodPool.objects.filter(pk=method_pool_id).first()
        from dongtai_engine.tasks import search_vul_from_method_pool
        search_vul_from_method_pool(method_pool.pool_sign, method_pool.agent_id)


class LoadSinkStrategyTestCase(TestCase):

    def test_load_sink_strategy(self):
        from dongtai_engine.tasks import load_sink_strategy
        strategies = load_sink_strategy()
        assert isinstance(strategies, list)
        assert len(strategies) > 0
        for language in (1, 2, 3, 4):
            strategies = load_sink_strategy(User.objects.get(pk=1), language)
            assert isinstance(strategies, list)
            assert len(strategies) > 0
