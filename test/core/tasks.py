import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_vul_recheck(self):
        from core.tasks import vul_recheck
        vul_recheck()

    def test_search_vul_from_replay_method_pool(self):
        from core.tasks import search_vul_from_replay_method_pool
        method_id = 110
        search_vul_from_replay_method_pool(method_id)


if __name__ == '__main__':
    unittest.main()
