######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : tesecase
# @created     : Monday Aug 09, 2021 16:50:19 CST
#
# @description :
######################################################################

from itertools import product

from rest_framework.serializers import CharField, IntegerField, SerializerMetaclass


def fuzz_test_data(end_point, httpmethod):
    method = getattr(end_point, httpmethod)
    queryfield = []
    data_tuple = []
    for query in method.querys:
        if isinstance(query, SerializerMetaclass):
            fields = query().get_fields()
            for k, v in fields.items():
                queryfield.append(k)
                if isinstance(v, IntegerField | CharField):
                    data_tuple.append([0, -1, "", "1", "-1", 0, "ale"])
        elif isinstance(query, dict):
            queryfield.append(query["name"])
            if query["type"] == int:
                data_tuple.append([0, -1, "", "1", "-1", 0, "alw"])
    return list(product(*data_tuple))


# @ddt
# class DocumentsEndpointTests(APITestCase):
#    def setUp(self):
#        self.method = list(
#            filter(lambda x: x in ['get', 'post'], dir(DocumentsEndpoint)))
#
#    def test_documents_retrive(self):
#
#    @data('python', 'java')
#    def test_documents_retrive(self, value):
#
#    @idata([{'language': 'python'}, {'language': 'java'}])
#    def test_documents_retrive2(self, value):
#
#    def test_edge_case(self):
#        for i in self.httpmethod.querys:
#            if isinstance(i, SerializerMetaclass):
#                for k, v in fields.items():
#                    if isinstance(v, IntegerField):
#                    if isinstance(v, CharField):
#
#    def test_documents_retrive22(self):
#
# class DocumentsEndpointTests(APITestCase):
#    def setUp(self):
#        self.method = list(
#            filter(lambda x: x in ['get', 'post'], dir(view)))
