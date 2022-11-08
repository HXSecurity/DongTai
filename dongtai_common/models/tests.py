from django.test import TestCase
import os
import json
from dongtai_common.models.url_blacklist import (
    IastAgentBlackRule,
    create_blacklist_rule,
)
from dongtai_common.models.url_blacklist import *


class VulEngineSearchTestCase(TestCase):

    def test_url_rule_create(self):
        create_blacklist_rule(TargetType.URL,
                              TargetOperator.CONTAIN,
                              value='123123',
                              user_id=1,
                              state=State.ENABLE)
