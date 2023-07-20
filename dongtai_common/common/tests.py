from dongtai_common.common.agent_command_check import valitate_taint_command

from django.test import TestCase


class TaintCommandValidatorTestCase(TestCase):
    def test_validate_taint_pos(self):
        cases = [
            "APPEND(P2,P3)",
            "APPEND(P2,P3,0)",
            " appEND ( p2 ,  P3 ,  0 ) ",
            "KEEP()",
            "SUBSET(0,P1)",
        ]
        for case in cases:
            res = valitate_taint_command(case)
            self.assertTrue(res, f"case {case} not passed")

    def test_validate_taint_neg(self):
        cases = ["foo", "foo(bar)", "foo()", "1"]
        for case in cases:
            res = valitate_taint_command(case)
            self.assertFalse(res, f"case {case} not passed")
