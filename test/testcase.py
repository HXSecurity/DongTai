######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : tesecase
# @created     : Monday Aug 09, 2021 16:50:19 CST
#
# @description :
######################################################################

import django
from rest_framework.test import APITestCase
from dongtai.models.department import DepartmentEndPoint
from django.urls import reserse
from urllib.parse import urlencode
class DepartmentTests(APITestCase):
    def test_create_account(self):
        url = reserse(DepartmentEndPoint.as_view())
        self.client.login(username='lauren', password='secret')
        response = self.client.post(urlassamble(url, {'name': 'random'}))
        response = self.client.put(urlassamble(url), {
            'name': "str",
            "parent": "number(0-n)"
        })
        self.assertEqual(response.status_code,200)
        self.assertSetEqual(DepartmentEndPoint.objects)



def urlassamble(url, query={}):
    return url + urlencode(query)
