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


class VulDetailTestCase(APITestCase):
    def login(self):
        self.user = User.objects.filter(pk=1).first()
        assert self.user is not None
        self.client.force_authenticate(user=self.user)

    def setUp(self):
        self.login()
        self.mockdata()

    def mockdata(self):
        self.server = IastServer.objects.create(
            hostname='DESKTOP-JLVFSOV-test',
            ip='0.0.0.0',
            port=22,
            container=None)

    def test_get_server(self):
        obj = VulDetail()
        obj.server = self.server
        assert obj.get_server()
