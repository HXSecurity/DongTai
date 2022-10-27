######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_register
# @created     : 星期五 12月 10, 2021 14:46:44 CST
#
# @description :
######################################################################


from test.apiserver.test_agent_base import AgentTestCase
from dongtai_common.models.agent import IastAgent
import json


from _typeshed import Incomplete
class AgentRegisterTestCase(AgentTestCase):
    test_agent_id: Incomplete
    def setUp(self) -> None:
        super().setUp()
        self.test_agent_id = []

    def test_rep_register(self) -> None:
        data1 = self.raw_register(name='rep_data')
        self.agent_heartbeat()
        data2 = self.raw_register(name='rep_data')
        assert data1.status_code == 200 and data2.status_code == 200
        self.test_agent_id += [
            json.loads(data2.content)['data']['id'],
            json.loads(data1.content)['data']['id']
        ]
        assert data1.content == data2.content

    def test_register(self) -> None:
        assert not IastAgent.objects.filter(pk=self.agent_id,
                                            project_version_id=0).exists()
