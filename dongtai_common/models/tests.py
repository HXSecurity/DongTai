from django.test import TestCase
from dongtai_common.models.url_blacklist import (
    IastAgentBlackRule,
    create_blacklist_rule,
    TargetType,
    TargetOperator,
    State,
)


class VulEngineSearchTestCase(TestCase):

    def test_url_rule_create(self):
        create_blacklist_rule(TargetType.URL,
                              TargetOperator.CONTAIN,
                              value='123123',
                              user_id=1,
                              state=State.ENABLE)
        rule = IastAgentBlackRule.objects.filter(user_id=1).first()
        assert [{
            'target_type': 'URL',
            'operator': 'CONTAIN',
            'value': '123123'
        }] == rule.to_full_rule()

    def test_url_rule_create_header(self):
        create_blacklist_rule(TargetType.HEADER_KEY,
                              TargetOperator.CONTAIN,
                              value='123123',
                              user_id=1,
                              state=State.ENABLE)
        rule = IastAgentBlackRule.objects.filter(user_id=1).first()
        assert [{
            'target_type': 'HEADER_KEY',
            'operator': 'CONTAIN',
            'value': '123123'
        }] == rule.to_full_rule()
