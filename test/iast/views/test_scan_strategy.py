######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : scan_strategy
# @created     : 星期四 12月 02, 2021 19:57:44 CST
#
# @description :
######################################################################



from rest_framework.test import APITestCase
from django.urls import include, path, reverse
from dongtai_web.views.scan_strategys import ScanStrategyViewSet
from dongtai_common.models.user import User


class ScanStrategyTestCase(APITestCase):
    def setUp(self) -> None:
        pass
    def test_create(self) -> None:
        self.client.force_authenticate(user=User.objects.filter(pk=1).first())
        response = self.client.get('/api/v1/scan_strategy')
        print(response.content)
        assert response.status_code == 200
