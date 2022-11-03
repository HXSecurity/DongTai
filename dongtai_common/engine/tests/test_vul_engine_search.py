from django.test import TestCase
from dongtai_common.engine.tests import MOCKDATA_DIR
import os
from dongtai_common.engine.vul_engine import VulEngine
import json

class VulEngineSearchTestCase(TestCase):

    def test_search_method_pool(self):
        MOCKDATA_FILE = os.path.join(MOCKDATA_DIR,
                                     'method_pool_edge_out_of_index.json')
        with open(MOCKDATA_FILE) as fp:
            mock_method_pool_data = json.load(fp)
        engine = VulEngine()
        engine.method_pool = mock_method_pool_data
        try:
            engine.search(method_pool=mock_method_pool_data,
                          vul_method_signature='java.lang.Class.forName')
        except IndexError as e:
            self.fail(
                "engine.search show check method_pool data instead of raise IndexError."
            )
