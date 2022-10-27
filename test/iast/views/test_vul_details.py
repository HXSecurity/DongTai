######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_vul_details
# @created     : 星期三 12月 08, 2021 15:44:10 CST
#
# @description :
######################################################################


from rest_framework.test import APITestCase
from dongtai_common.models.server import IastServer
from dongtai_common.models.user import User
from dongtai_web.views.vul_details import VulDetail


from _typeshed import Incomplete
class VulDetailTestCase(APITestCase):
    user: Incomplete
    server: Incomplete
    def login(self) -> None:
        self.user = User.objects.filter(pk=1).first()
        self.client.force_authenticate(user=self.user)

    def setUp(self) -> None:
        self.login()
        self.mockdata()

    def mockdata(self) -> None:
        self.server = IastServer.objects.create(
            hostname='DESKTOP-JLVFSOV-test',
            ip='0.0.0.0',
            port=22,
            container=None)


    def test_get_server(self) -> None:
        obj = VulDetail()
        obj.server = self.server
        assert obj.get_server()
