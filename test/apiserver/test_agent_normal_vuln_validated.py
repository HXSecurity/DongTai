import json
from test.apiserver.test_agent_base import AgentTestCase

from dongtai_common.models.vulnerablity import IastVulnerabilityModel

with open("./test/integration/mockdata/validated_method_pool.json") as fp:
    json_1 = json.load(fp)


class AgentNormalMultiVulTestCase(AgentTestCase):
    def test_agent_validated_vuln_upload(self):
        json_1["detail"]["agentId"] = self.agent_id
        self.agent_report(json_1)
        vul = IastVulnerabilityModel.objects.filter(agent_id=self.agent_id, level_id=1).first()
        self.assertIsNotNone(vul)
        self.assertEqual(len(list(filter(lambda x: "validators" in x, json.loads(vul.full_stack)[0]))), 1)
