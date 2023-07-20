######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_sensitive_info_rule
# @created     : 星期一 12月 13, 2021 19:50:46 CST
#
# @description :
######################################################################


from rest_framework.test import APITestCase
from dongtai_common.models.user import User


class SensitiveInfoRuleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.filter(pk=1).first()
        assert self.user is not None
        self.client.force_authenticate(user=self.user)

    def test_sensitive_info_rule_create(self):
        response = self.client.post(
            "/api/v1/sensitive_info_rule",
            data={
                "pattern": "0",
                "pattern_type_id": 1,
                "status": 0,
                "strategy_id": 2147483648,
            },
        )
        assert response.status_code == 200
