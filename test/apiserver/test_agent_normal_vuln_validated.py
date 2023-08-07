import json
from test.apiserver.test_agent_base import AgentTestCase

with open("./test/integration/mockdata/validated_method_pool.json") as fp:
    json_1 = json.load(fp)


class AgentNormalMultiVulTestCase(AgentTestCase):
    def test_agent_validated_vuln_upload(self):
        json_1["detail"]["agentId"] = self.agent_id
        self.agent_report(json_1)
