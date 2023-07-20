######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_vul_summary
# @created     : 星期三 12月 08, 2021 14:43:47 CST
#
# @description :
######################################################################

from rest_framework.test import APITestCase
from dongtai_common.models.user import User
import json
from dongtai_common.models.hook_strategy import HookStrategy


class EngineHookRuleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.filter(pk=1).first()
        assert self.user is not None
        self.client.force_authenticate(user=self.user)

    def test_create(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
            "ignore_blacklist": True,
            "ignore_internal": True,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)

    def test_create_1(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
            "ignore_blacklist": False,
            "ignore_internal": True,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)

    def test_create_2(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
            "ignore_blacklist": False,
            "ignore_internal": False,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)

    def test_legacy_modify_1(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)
        hook_rule = HookStrategy.objects.filter(value="1231231231").first()
        self.assertNotEqual(hook_rule, None)
        data2 = {
            "rule_id": hook_rule.id,
            "rule_type_id": 76,
            "rule_value": "123123123",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data2)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)

    def test_modify_2(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
            "ignore_blacklist": False,
            "ignore_internal": False,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)
        hook_rule = HookStrategy.objects.filter(value="1231231231").first()
        self.assertNotEqual(hook_rule, None)
        data2 = {
            "rule_id": hook_rule.id,
            "rule_type_id": 76,
            "rule_value": "123123123",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
            "ignore_blacklist": False,
            "ignore_internal": False,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data2)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)

    def test_create_legacy(self):
        data = {
            "rule_type_id": 76,
            "rule_value": "1231231231",
            "rule_target": "O",
            "rule_source": "O",
            "inherit": "false",
            "track": "false",
            "language_id": 1,
        }
        response = self.client.post("/api/v1/engine/hook/rule/add", data=data)
        self.assertEqual(response.status_code, 200)
        respdata = json.loads(response.content)
        self.assertEqual(respdata["status"], 201)
