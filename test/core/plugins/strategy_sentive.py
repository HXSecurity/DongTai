import unittest
from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, True)

    def test_search_id_card_leak(self):
        id = 45789
        from dongtai_common.models.agent_method_pool import MethodPool

        method_pool = MethodPool.objects.get(id=id)
        if method_pool:
            from dongtai_engine.plugins.strategy_sensitive import search_id_card_leak

            search_id_card_leak(method_pool)

    def test_check_id_card(self):
        right_numbers = (
            "510103196502083435",
            "510103196608150034",
        )
        wrong_numbers = ("510103296502083435",)
        from dongtai_engine.plugins.strategy_sensitive import check_id_card

        for right_number in right_numbers:
            print("current number is: " + right_number)
            self.assertEqual(True, check_id_card(right_number))

        for wrong_number in wrong_numbers:
            print("current number is: " + wrong_number)
            self.assertEqual(False, check_id_card(wrong_number))

    def test_check_response_content(self):
        id = 45789
        from dongtai_common.models.agent_method_pool import MethodPool

        method_pool = MethodPool.objects.get(id=id)
        if method_pool:
            from dongtai_engine.plugins.strategy_sensitive import check_response_content

            check_response_content(method_pool)


if __name__ == "__main__":
    unittest.main()
