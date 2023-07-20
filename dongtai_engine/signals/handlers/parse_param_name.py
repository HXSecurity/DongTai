from django.http.request import QueryDict
from dongtai_common.engine.compatibility import method_pool_is_3, parse_target_value
from typing import List, Dict


class ParamDict(QueryDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_extend_kv_dict()

    def __init_extend_kv_dict(self):
        self.extend_kv_dict = {}
        self.extend_k_map = {}
        for k, v in self.items():
            if "=" in v:
                origin_string = f"{k}={v}"
                groups = origin_string.split("=")
                for i in range(1, len(groups)):
                    k_ = "=".join(groups[:i])
                    v_ = "=".join(groups[i:])
                    self.extend_kv_dict[k_] = v_
                    self.extend_k_map[k_] = k


def parse_target_values_from_vul_stack(vul_stack: list[list[dict]]) -> list[str]:
    target_values = [i["targetValues"] for i in vul_stack[0]]
    if vul_stack[0] and method_pool_is_3(vul_stack[0][0]):
        target_values = [parse_target_value(x) for x in target_values]
    return target_values
