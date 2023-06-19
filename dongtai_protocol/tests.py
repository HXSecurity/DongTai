from dongtai_protocol.report.handler.heartbeat_handler import HeartBeatHandler
from dongtai_common.utils import const
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_protocol.report.handler.heartbeat_handler import (
    addtional_agent_ids_query_deployway_and_path,
    addtional_agenti_ids_query_filepath_simhash)
from os.path import exists
import requests
from test.apiserver.test_agent_base import AgentTestCase, gzipdata
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
import gzip
import base64
from dongtai_protocol.report.report_handler_factory import ReportHandler
import json
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from result import Ok, Err, Result
import unittest
from django.test import TestCase


@unittest.skip("waiting for rebuild mock data")
class AgentMethodPoolUploadTestCase(AgentTestCase):

    def test_benchmark_agent_method_pool_upload(self):
        data = []
        res = download_if_not_exist(
            "https://huoqi-public.oss-cn-beijing.aliyuncs.com/iast/test_data/server.log",
            "/tmp/test_apiserver_server.log")
        with open('/tmp/test_apiserver_server.log') as f:
            for line in f:
                data.append(json.loads(line))
        for report in data:
            report["detail"]["agentId"] = self.agent_id
            del report["message"]
            res = ReportHandler.handler(report, self.user)
            assert res == ""
            assert MethodPool.objects.filter(
                url=report['detail']["url"]).exists()
        assert MethodPool.objects.filter(
            agent_id=self.agent_id).count() == len(data)


def download_file(url, filepath):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return Ok()


def download_if_not_exist(url: str, path: str) -> Result:
    if exists(path):
        return Ok()
    res = download_file(url, path)
    return res


class AgentHeartBeatTestCase(AgentTestCase):

    def test_agent_replay_queryset(self):
        self.agent = IastAgent.objects.filter(pk=self.agent_id).first()
        project_agents = IastAgent.objects.values_list('id', flat=True).filter(
            bind_project_id=self.agent.bind_project_id,
            language=self.agent.language).union(
                addtional_agenti_ids_query_filepath_simhash(
                    self.agent.filepathsimhash, language=self.agent.language),
                addtional_agent_ids_query_deployway_and_path(
                    self.agent.servicetype,
                    self.agent.server.path,
                    self.agent.server.hostname,
                    language=self.agent.language))
        replay_queryset = IastReplayQueue.objects.values(
            'id', 'relation_id', 'uri', 'method', 'scheme', 'header', 'params',
            'body',
            'replay_type').filter(agent_id__in=project_agents,
                                  state__in=[const.WAITING,
                                             const.SOLVING])[:200]

    def test_agent_replay_queryset_result(self):
        self.agent = IastAgent.objects.filter(pk=self.agent_id).first()
        handler = HeartBeatHandler()
        handler.agent = self.agent
        handler.anget_id = self.agent_id
        handler.return_queue = 1
        res1 = handler.get_result()
        res2 = handler.get_result()
        res3 = handler.get_result()
        set1, set2, set3 = map(get_replay_id_set, [res1, res2, res3])
        assert set3.intersection(set1) == set([])


def get_replay_id_set(replay_list: list) -> set:
    return set([i['id'] for i in replay_list])


@unittest.skip("waiting for rebuild mock data")
class AgentSaasMethodPoolParseApiTestCase(AgentTestCase):

    def test_api_parse(self):
        mp = MethodPool.objects.filter(pk=500483715).first()
        mp.req_header
        headers_bytes = base64.b64decode(mp.req_header)
        from dongtai_engine.filters.utils import parse_headers_dict_from_bytes
        res = parse_headers_dict_from_bytes(headers_bytes)
        from http.cookies import SimpleCookie
        cookie = SimpleCookie()
        cookie.load(res['cookie'])
        print(cookie.keys())


class SimhashTypingCheckTestCase(TestCase):

    def test_data_dump(self):
        from dongtai_protocol.report.handler.agent_filepath_handler import _data_dump
        serviceDir = "F:\\projects\\huoxian\\iast\\vul\\SecExample\\.git\\config\n"
        res = _data_dump(serviceDir)
        self.assertIsInstance(res, str)
