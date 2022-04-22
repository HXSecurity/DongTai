# Create your tests here.
from django.test import TestCase
from iast.views.agents_v2 import query_agent

class DashboardTestCase(TestCase):
    def test_query_agent(self):
        res = query_agent()
        print(res)
