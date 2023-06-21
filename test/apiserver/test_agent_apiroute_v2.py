from test.apiserver.test_agent_base import AgentTestCase
from dongtai_common.models.api_route_v2 import IastApiRouteV2
from dongtai_common.models.agent import IastAgent
import json


class ApiRouteV2TestCase(AgentTestCase):

    def test_agent_api_upload(self):
        with open('./test/integration/mockdata/api-report.json') as fp:
            data = json.load(fp)
        data['detail']['agentId'] = self.agent_id
        res = self.agent_report(data, agentId=self.agent_id)
        self.assertGreater(
            IastApiRouteV2.objects.filter(
                project_version__iastagent__pk=self.agent_id).count(), 0)
