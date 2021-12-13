######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_vul_summary
# @created     : 星期三 12月 08, 2021 14:43:47 CST
#
# @description :
######################################################################


from rest_framework.test import APITestCase
from django.urls import include, path, reverse
from dongtai.models.user import User
from dongtai.models.agent import IastAgent
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.models.hook_type import HookType
import time

class ScanStrategyTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.filter(pk=1).first()
        self.client.force_authenticate(user=self.user)
        agent = IastAgent.objects.create(token='testtoken',
                                         version='121231',
                                         latest_time=int(time.time()),
                                         user=self.user,
                                         is_running=1,
                                         bind_project_id=-1,
                                         project_name='test',
                                         control=0,
                                         is_control=0,
                                         is_core_running=1,
                                         online=1,
                                         project_version_id=1,
                                         language='NGUAGE',
                                         is_audit=1)
        vuln = IastVulnerabilityModel.objects.create(
            level_id=1,
            url='',
            uri='',
            http_method='',
            http_scheme='',
            http_protocol='',
            req_header='',
            req_params='',
            req_data='',
            res_header='',
            res_body='',
            full_stack='',
            top_stack='',
            bottom_stack='',
            taint_value='',
            taint_position='',
            agent=agent,
            context_path='',
            counts=1,
            first_time=int(time.time()),
            latest_time=int(time.time()),
            client_ip='0',
            param_name='',
            method_pool_id=1,
            strategy_id=-1,
            hook_type_id=1,
            status_id=1)
        self.mockdata = [agent, vuln]

    def test_create(self):
        response = self.client.get('/api/v1/vuln/summary')
        assert response.status_code == 200

