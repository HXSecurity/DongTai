from rest_framework.test import APITestCase
from apiserver.views.agent_config import get_agent_config
from apiserver.views.agent_config import *


class VulDetailTestCase(APITestCase):

    def test_agent_config_generate(self):
        print(get_agent_config(1))

    def test_agent_detail_retrieve(self):
        res = get_agent_filter_details(1)
        print(res)

    def test_target_filter(self):
        res = get_agent_config_by_scan(1, 2)
        print(res)
