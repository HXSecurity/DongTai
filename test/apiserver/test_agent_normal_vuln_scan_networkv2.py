######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_hardencode_vuln
# @created     : 星期六 12月 18, 2021 11:40:31 CST
#
# @description :
######################################################################

import json
import uuid
from test.apiserver.test_agent_base import AgentTestCase

from dongtai_common.engine.vul_engine import VulEngine

with open("./test/integration/mockdata/2individualpath.json") as fp:
    json_1 = json.load(fp)

with open("./test/integration/mockdata/2pathdifferentsourcev2.json") as fp:
    json_2 = json.load(fp)

with open("./test/integration/mockdata/2pathdifferentsourcev1.json") as fp:
    json_3 = json.load(fp)


def mock_uuid():
    return uuid.UUID(int=0)


class AgentNormalMultiVulTestCase(AgentTestCase):
    def test_agent_vuln_upload1(self):
        engine = VulEngine()
        engine.method_pool = json_1
        engine.search(
            method_pool=json_1,
            vul_method_signature="java.lang.Runtime.exec",
        )
        self.assertEqual(2, len(engine.results()))

    def test_agent_vuln_upload2(self):
        engine = VulEngine()
        engine.method_pool = json_2
        engine.search(
            method_pool=json_2,
            vul_method_signature="java.lang.Runtime.exec",
        )
        self.assertEqual(2, len(engine.results()))

    def test_agent_vuln_upload3(self):
        engine = VulEngine()
        engine.method_pool = json_3
        engine.search(
            method_pool=json_3,
            vul_method_signature="java.lang.Runtime.exec",
        )
        self.assertEqual(2, len(engine.results()))
