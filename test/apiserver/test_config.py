from rest_framework.test import APITestCase
from dongtai_protocol.views.agent_config import (
    get_agent_config,
    get_agent_filter_details,
    get_agent_config_by_scan,
)
from dongtai_common.models.user import User
from dongtai_common.models.agent_config import MetricGroup


class VulDetailTestCase(APITestCase):

    def test_agent_config_generate(self):
        print(get_agent_config(1))

    def test_agent_detail_retrieve(self):
        res = get_agent_filter_details(1)
        print(res)

    def test_target_filter(self):
        res = get_agent_config_by_scan(1, MetricGroup.SYSTEM)
        print(res)

    def test_agent_config_request(self):
        self.user = User.objects.filter(pk=1).first()
        assert self.user is not None
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/v1/agent/thresholdv2')
