import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_vul_recheck(self):
        from core.tasks import vul_recheck
        vul_recheck()


if __name__ == '__main__':
    unittest.main()
