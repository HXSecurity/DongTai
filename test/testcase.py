######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : tesecase
# @created     : Monday Aug 09, 2021 16:50:19 CST
#
# @description :
######################################################################

import django
from rest_framework.test import APITestCase
from dongtai_web.views.documents import DocumentsEndpoint
from django.urls import reverse
from urllib.parse import urlencode
from rest_framework.serializers import SerializerMetaclass
from rest_framework.serializers import CharField, IntegerField
from django.contrib.auth import get_user_model
from ddt import ddt, data, file_data, unpack, idata
from itertools import product


def fuzz_test_data(end_point, httpmethod):
    method = getattr(end_point, httpmethod)
    queryfield = []
    data_tuple = []
    for query in method.querys:
        if isinstance(query, SerializerMetaclass):
            fields = query().get_fields()
            for k, v in fields.items():
                queryfield.append(k)
                if isinstance(v, IntegerField):
                    data_tuple.append([0, -1, "", "1", "-1", 0, "ale"])
                elif isinstance(v, CharField):
                    data_tuple.append([0, -1, "", "1", "-1", 0, "ale"])
        elif isinstance(query, dict):
            queryfield.append(query["name"])
            if query["type"] == int:
                data_tuple.append([0, -1, "", "1", "-1", 0, "alw"])
    li = list(product(*data_tuple))
    return li


# @ddt
# class DocumentsEndpointTests(APITestCase):
#    def setUp(self):
#        self.url = '/api/v1/documents'
#        self.view = DocumentsEndpoint
#        self.method = list(
#            filter(lambda x: x in ['get', 'post'], dir(DocumentsEndpoint)))
#        self.httpmethod = getattr(DocumentsEndpoint, self.method[0])
#        user_model = get_user_model()
#        self.client.force_login(user_model.objects.first())
#
#    def test_documents_retrive(self):
#        response = self.client.get(self.url, {'language': 'python'})
#        self.assertEqual(response.status_code, 200)
#
#    @data('python', 'java')
#    def test_documents_retrive(self, value):
#        response = self.client.get(self.url, {'language': value})
#        self.assertEqual(response.status_code, 200)
#
#    @idata([{'language': 'python'}, {'language': 'java'}])
#    def test_documents_retrive2(self, value):
#        response = self.client.get(self.url, value)
#        self.assertEqual(response.status_code, 200)
#
#    def test_edge_case(self):
#        data = {}
#        for i in self.httpmethod.querys:
#            if isinstance(i, SerializerMetaclass):
#                fields = i().get_fields()
#                for k, v in fields.items():
#                    if isinstance(v, IntegerField):
#                        data[k] = 0
#                    if isinstance(v, CharField):
#                        data[k] = ''
#        getattr(self.client, self.method[0])(self.url, data)
#
#    def test_documents_retrive22(self):
#        response = self.client.get(self.url, {'language': 'python'})
#        self.assertEqual(response.status_code, 200)
# from django.urls import resolve
#
# class DocumentsEndpointTests(APITestCase):
#    def setUp(self):
#        self.urls = ['/api/v1/documents', '/api/v1/api_route/search']
#        url = '/api/v1/documents'
#        view = resolve(url).func.view_class
#        self.method = list(
#            filter(lambda x: x in ['get', 'post'], dir(view)))
#        self.httpmethod = getattr(DocumentsEndpoint, self.method[0])
#        user_model = get_user_model()
#        self.client.force_login(user_model.objects.first())
