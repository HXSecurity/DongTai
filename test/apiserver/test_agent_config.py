######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_register
# @created     : 星期五 12月 10, 2021 14:46:44 CST
#
# @description :
######################################################################

import json
from test.apiserver.test_agent_base import AgentTestCase

from dongtai_common.models.agent import IastAgent


class AgentConfigTestCase(AgentTestCase):
    def setUp(self):
        super().setUp()

    def test_rep_agent_config_avalible(self):
        res = self.client.get(
            f"/api/v1/agent/config?agent_id={self.agent_id}",
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 200)

    def test_rep_agent_config(self):
        res = self.client.get(
            f"/api/v1/agent/config?agent_id={self.agent_id}",
            content_type="application/json",
        )
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data["data"],
            {"report_validated_sink": False},
        )

    def test_rep_agent_config2(self):
        agent = IastAgent.objects.filter(pk=self.agent_id).first()
        assert agent is not None
        agent.bind_project.log_level = "INFO"
        agent.bind_project.enable_log = True
        agent.bind_project.save()
        res = self.client.get(
            f"/api/v1/agent/config?agent_id={self.agent_id}",
            content_type="application/json",
        )
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data["data"],
            {"enable_log": True, "log_level": "INFO", "report_validated_sink": False},
        )

    def test_rep_agent_config3(self):
        agent = IastAgent.objects.filter(pk=self.agent_id).first()
        assert agent is not None
        agent.bind_project.log_level = "INFO"
        agent.bind_project.save()
        res = self.client.get(
            f"/api/v1/agent/config?agent_id={self.agent_id}",
            content_type="application/json",
        )
        data = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data["data"],
            {"log_level": "INFO", "report_validated_sink": False},
        )
