######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################

from test.apiserver.test_agent_base import AgentTestCase
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.strategy import IastStrategyModel
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
import json
from unittest.mock import patch, MagicMock
import uuid
from dongtai_engine.tasks import search_vul_from_method_pool
import pickle

with open('./test/integration/mockdata/new-exec.json') as fp:
    new_exec_json = json.load(fp)

with open('./test/integration/mockdata/old-exec.json') as fp:
    old_exec_json = json.load(fp)

with open('./test/integration/mockdata/new-novul.json') as fp:
    new_novul_json = json.load(fp)

with open('./test/integration/mockdata/exec2.json') as fp:
    exec2_json = json.load(fp)

with open('./test/integration/mockdata/xss.json') as fp:
    xss_json = json.load(fp)

with open('./test/integration/mockdata/recursive_depth_1.pickle', 'rb') as fp:
    recursive_pickle = pickle.load(fp)


def mock_uuid():
    return uuid.UUID(int=0)


class AgentNormalVulTestCase(AgentTestCase):

    def test_agent_vuln_upload(self):
        res = self.agent_report(new_exec_json)

    def test_agent_vuln_upload2(self):
        with patch('uuid.uuid4', mock_uuid):
            res = self.agent_report(new_exec_json)
            search_vul_from_method_pool(str(uuid.UUID(int=0).hex),
                                        self.agent_id)
        print(
            IastVulnerabilityModel.objects.filter(agent_id=self.agent_id,
                                                  level_id=1).count())
        assert IastVulnerabilityModel.objects.filter(agent_id=self.agent_id,
                                                     level_id=1).count() == 1
        vul = IastVulnerabilityModel.objects.filter(agent_id=self.agent_id,
                                                    level_id=1).first()

    def test_agent_vuln_upload3(self):
        with patch('uuid.uuid4', mock_uuid):
            res = self.agent_report(old_exec_json)
            search_vul_from_method_pool(str(uuid.UUID(int=0).hex),
                                        self.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                agent_id=self.agent_id, level_id=1).count() == 1

    def test_agent_vuln_upload4(self):
        with patch('uuid.uuid4', mock_uuid):
            res = self.agent_report(new_novul_json)
            search_vul_from_method_pool(str(uuid.UUID(int=0).hex),
                                        self.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                agent_id=self.agent_id, level_id=1).count() == 0

    def test_agent_vuln_upload5(self):
        with patch('uuid.uuid4', mock_uuid):
            res = self.agent_report(exec2_json)
            search_vul_from_method_pool(str(uuid.UUID(int=0).hex),
                                        self.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                agent_id=self.agent_id, level_id=1).count() == 1

    def test_agent_vuln_upload6(self):
        with patch('uuid.uuid4', mock_uuid):
            res = self.agent_report(xss_json)
            search_vul_from_method_pool(str(uuid.UUID(int=0).hex),
                                        self.agent_id)
            assert IastVulnerabilityModel.objects.filter(
                agent_id=self.agent_id, level_id=2).count() == 0

    def test_agent_vuln_upload7(self):
        recursive_pickle.agent_id = self.agent_id
        recursive_pickle.save()
        search_vul_from_method_pool(recursive_pickle.pool_sign, self.agent_id)
        assert IastVulnerabilityModel.objects.filter(
            agent_id=self.agent_id,
            level_id=1,
        ).count() == 1
