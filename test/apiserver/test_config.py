from rest_framework.test import APITestCase
from dongtai_protocol.views.agent_config import get_agent_config
from dongtai_protocol.views.agent_config import *
from dongtai_common.models.user import User


from dongtai_protocol.views.agent_config import *
from _typeshed import Incomplete
class VulDetailTestCase(APITestCase):

    user: Incomplete
    def test_agent_config_generate(self) -> None:
        print(get_agent_config(1))

    def test_agent_detail_retrieve(self) -> None:
        res = get_agent_filter_details(1)
        print(res)

    def test_target_filter(self) -> None:
        res = get_agent_config_by_scan(1, 2)
        print(res)


    def test_agent_config_request(self) -> None:
        self.user = User.objects.filter(pk=1).first()
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/agent/thresholdv2')
