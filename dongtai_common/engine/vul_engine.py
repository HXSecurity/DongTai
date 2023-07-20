#!/usr/bin/env python
# datetime: 2021/7/21 下午7:07
import copy
import logging
from collections import defaultdict

from django.utils.functional import cached_property

from dongtai_common.engine.compatibility import (
    method_pool_3_to_2,
    method_pool_is_3,
    parse_target_value,
)

logger = logging.getLogger("dongtai-engine")


class VulEngine:
    """
    根据策略和方法池查找是否存在漏洞,此类不进行策略和方法池的权限验证
    """

    def __init__(self):
        """
        构造函数,初始化相关数据
        """
        self._method_pool = []
        self.method_pool_asc = []
        self._vul_method_signature = None
        self.hit_vul = False
        self.vul_stack = []
        self.pool_value = None
        self.vul_source_signature = None
        self.graph_data = {"nodes": [], "edges": []}
        self.method_counts = 0
        self.taint_link_size = 0
        self.edge_code = 1
        self.taint_value = ""
        self.vul_type = None
        self.version = 1

    @property
    def method_pool(self):
        """
        方法池数据
        :return:
        """
        return self._method_pool

    @method_pool.setter
    def method_pool(self, method_pool):
        """
        设置方法池数据,根据方法调用ID对数据进行倒序排列,便于后续检索漏洞
        :param method_pool:
        :return:
        """
        self._method_pool = sorted(
            method_pool, key=lambda e: e.__getitem__("invokeId"), reverse=True
        )
        if method_pool and method_pool_is_3(method_pool[0]):
            self._method_pool = list(map(method_pool_3_to_2, self._method_pool))
            self.version = 3
        self._method_pool = sorted(
            self._method_pool, key=lambda e: e.__getitem__("invokeId"), reverse=True
        )
        self._method_pool_invokeid_dict = {
            mp["invokeId"]: ind for ind, mp in enumerate(self._method_pool)
        }
        tempdict = defaultdict(list, {})
        for ind, mp in enumerate(self._method_pool):
            for target_hash in mp["targetHash"]:
                tempdict[target_hash].append(ind)
        self._method_pool_target_hash_dict = dict(tempdict)

    @property
    def vul_method_signature(self):
        return self._vul_method_signature

    @vul_method_signature.setter
    def vul_method_signature(self, vul_method_signature):
        self._vul_method_signature = vul_method_signature

    def prepare(self, method_pool, vul_method_signature):
        """
        对方法池、漏洞方法签名及其他数据进行预处理
        :param method_pool: 方法池,list
        :param vul_method_signature: 漏洞方法签名,str
        :return:
        """
        self.method_pool = method_pool
        self.vul_method_signature = vul_method_signature
        self.hit_vul = False
        self.vul_stack = []
        self.pool_value = -1
        self.vul_source_signature = ""
        self.method_counts = len(self.method_pool)

    def hit_vul_method(self, method):
        if (
            f"{method.get('className')}.{method.get('methodName')}"
            == self.vul_method_signature
        ):
            self.hit_vul = True
            return True
        return None

    def do_propagator(self, method, current_link):
        is_source = method.get("source")
        target_hash = method.get("targetHash")

        for hash in target_hash:
            if hash in self.pool_value:
                if is_source:
                    current_link.append(method)
                    self.vul_source_signature = (
                        f"{method.get('className')}.{method.get('methodName')}"
                    )
                    return True
                current_link.append(method)
                self.pool_value = method.get("sourceHash")
                break
        return None

    @cached_property
    def method_pool_signatures(self):
        signatures = set()

        for method in self.method_pool:
            signatures.add(
                f"{method.get('className').replace('/', '.')}.{method.get('methodName')}"
            )
        return signatures

    def search(self, method_pool, vul_method_signature, vul_type=None):
        self.vul_type = vul_type
        self.prepare(method_pool, vul_method_signature)
        size = len(self.method_pool)
        from collections import defaultdict
        from functools import reduce
        from itertools import product

        import networkit as nk

        # Gather data
        source_hash_dict = defaultdict(set)
        target_hash_dict = defaultdict(set)
        invokeid_dict = {}
        for pool in self.method_pool:
            for s_hash in pool["sourceHash"]:
                source_hash_dict[s_hash].add(pool["invokeId"])
            for t_hash in pool["targetHash"]:
                target_hash_dict[t_hash].add(pool["invokeId"])
            invokeid_dict[pool["invokeId"]] = pool
        vul_methods = [
            x["invokeId"] for x in filter(self.hit_vul_method, self.method_pool)
        ]
        # Ignore `org.springframework.web.util.pattern.PathPattern.getPatternString()` as a non-source method.
        # It is only to indicate that the API pattern.
        source_methods = [
            x["invokeId"]
            for x in filter(
                lambda x: x.get("source", False)
                and x.get("signature")
                != "org.springframework.web.util.pattern.PathPattern.getPatternString()",
                self.method_pool,
            )
        ]
        # Build a graph
        g = nk.Graph(weighted=True, directed=True)
        for pool in self.method_pool:
            vecs = [
                [pool["invokeId"], t]
                for t in reduce(
                    lambda x, y: x | y,
                    [source_hash_dict[i] for i in pool["targetHash"]],
                    set(),
                )
            ]
            for source, target in vecs:
                g.addEdge(source, target, abs(source - target) ** 1.1, addMissing=True)
        # Checkout each pair source/target have a path or not
        # It may lost sth when muliti paths exists.
        for s, t in product(source_methods, vul_methods):
            if not g.hasNode(s) or not g.hasNode(t):
                continue
            dij_obj = nk.distance.BidirectionalDijkstra(g, s, t).run()
            if dij_obj.getDistance() != 1.7976931348623157e308:  # INF here!
                logger.info("find sink here!")
                path = dij_obj.getPath()
                total_path = [s, *path, t]
                final_stack = []
                for path_key in total_path:
                    sub_method = invokeid_dict[path_key]
                    if sub_method.get("source"):
                        self.vul_source_signature = f"{sub_method.get('className')}.{sub_method.get('methodName')}"
                        final_stack.append(self.copy_method(sub_method, source=True))
                    elif sub_method["invokeId"] == t:
                        self.taint_value = sub_method["targetValues"]
                        final_stack.append(self.copy_method(sub_method, sink=True))
                    else:
                        final_stack.append(
                            self.copy_method(sub_method, propagator=True)
                        )
                self.vul_stack = [final_stack]
        if self.vul_source_signature and "sourceType" in self.vul_stack[-1][-1]:
            final_stack = self.vul_stack[-1][-1]
            current_link = []
            current_link.append(final_stack)
            the_second_stack = None
            for source_type in final_stack["sourceType"]:
                if source_type["type"] == "HOST":
                    source_type_hash = source_type["hash"]
                    for ind, method in enumerate(self.method_pool):
                        if method["invokeId"] == final_stack["invokeId"]:
                            index = ind
                    before_stacks = self.method_pool[index:]
                    for stack in before_stacks:
                        if "targetRange" in stack:
                            target_ranges = dict(
                                zip(
                                    [i["hash"] for i in stack["targetRange"]],
                                    stack["targetRange"],
                                    strict=False,
                                )
                            )
                            if (
                                source_type_hash in target_ranges
                                and target_ranges[source_type_hash]["ranges"]
                            ):
                                the_second_stack = stack
                                break
            self.vul_source_signature = None
            self.vul_stack = []
            if not the_second_stack:
                return
            self.pool_value = set(the_second_stack.get("sourceHash"))
            for ind, method in enumerate(self.method_pool):
                if method["invokeId"] == the_second_stack["invokeId"]:
                    index = ind
            if the_second_stack.get("source_type"):
                current_link.append(self.copy_method(the_second_stack, source=True))
            else:
                current_link.append(self.copy_method(the_second_stack, propagator=True))
            logger.info(f"==> current taint hash: {self.pool_value}")
            logger.info("find second")
            self.loop(
                index, size, current_link, set(the_second_stack.get("sourceHash"))
            )
            current_link = current_link[0:2]
            extract_stack = self.find_other_branch_v2(
                index, size, current_link, set(the_second_stack.get("sourceHash"))
            )
            self.vul_stack[0] = extract_stack[::-1]
        elif self.vul_stack:
            final_stack = self.vul_stack[-1][-1]
            for ind, method in enumerate(self.method_pool):
                if method["invokeId"] == final_stack["invokeId"]:
                    index = ind
            before_stacks = self.method_pool[index:]
            the_second_stack = None
            has_vul = False
            for stack in before_stacks:
                if "targetRange" in stack:
                    target_ranges = dict(
                        zip(
                            [i["hash"] for i in stack["targetRange"]],
                            stack["targetRange"],
                            strict=False,
                        )
                    )
                    if set(final_stack["sourceHash"]) & set(stack["targetHash"]):
                        for _k, v in target_ranges.items():
                            if v["ranges"]:
                                has_vul = True
                        the_second_stack = stack
                        break
                elif set(final_stack["sourceHash"]) & set(stack["targetHash"]):
                    the_second_stack = stack
                    has_vul = True
                    break
            if not the_second_stack or not has_vul:
                self.vul_source_signature = None
                self.vul_stack = []
                self.pool_value = ""
                return
            # Disable temporary , will refactor it in next version.
            #
            #    index, size, current_link, set(final_stack.get('sourceHash')))
        else:
            pass
        self.vul_filter()

    def find_other_branch_v2(self, index, size, current_link, source_hash):
        for sub_index in range(index + 1, size):
            sub_method = self.method_pool[sub_index]
            sub_target_hash = set(sub_method.get("targetHash"))
            sub_target_rpc_hash = set(sub_method.get("targetHashForRpc", []))
            if (
                (sub_target_hash and sub_target_hash & source_hash)
                or (sub_target_rpc_hash and sub_target_rpc_hash & source_hash)
            ) and check_service_propagate_method_state(sub_method):
                logger.info(f"stisfied {sub_method}")
                if sub_method.get("source"):
                    current_link.append(self.copy_method(sub_method, source=True))
                else:
                    current_link.append(self.copy_method(sub_method, propagator=True))
                source_hash = source_hash | set(sub_method.get("sourceHash"))
            else:
                logger.debug("not stisfied {sub_method}")
        return current_link

    def vul_filter(self):
        # 分析是否存在过滤条件,排除误报
        # 根据漏洞类型,查询filter方法
        # 检查vul_
        if self.vul_source_signature:
            # mark there has a vul
            # if vul_type has filter, do escape
            stack_count = len(self.vul_stack)
            for index in range(0, stack_count):
                stack = self.vul_stack[index]
                for item in stack:
                    if item["signature"] == "java.net.URL.<init>":
                        url = item["sourceValues"]
                        origin_source = stack[0]["targetValues"]
                        from urllib.parse import urlparse

                        o = urlparse(url)
                        if origin_source not in f"{o.scheme}://{o.netloc}{o.path}":
                            self.vul_stack[index] = []
                            break
            vul_source_signature = self.vul_source_signature
            self.vul_source_signature = None
            for index in range(0, stack_count):
                if self.vul_stack[index]:
                    self.vul_source_signature = vul_source_signature
                else:
                    continue

    @staticmethod
    def copy_method(
        method_detail, sink=False, source=False, propagator=False, filter=False
    ):
        vul_method_detail = copy.deepcopy(method_detail)
        vul_method_detail["originClassName"] = vul_method_detail["originClassName"]
        # todo  根据类型进行拼接
        if source:
            vul_method_detail["tag"] = "source"
            vul_method_detail[
                "code"
            ] = f'<em>{vul_method_detail["targetValues"]}</em> = {vul_method_detail["signature"]}(...)'
        elif propagator:
            vul_method_detail["tag"] = "propagator"
            vul_method_detail[
                "code"
            ] = f'<em>{vul_method_detail["targetValues"]}</em> = {vul_method_detail["signature"]}(..., <em>{vul_method_detail["sourceValues"]}</em>, ...)'
        elif filter:
            vul_method_detail["tag"] = "filter"
            vul_method_detail[
                "code"
            ] = f'<em>{vul_method_detail["targetValues"]}</em> = {vul_method_detail["signature"]}(..., <em>{vul_method_detail["sourceValues"]}</em>, ...)'
        elif sink:
            vul_method_detail["tag"] = "sink"
            vul_method_detail[
                "code"
            ] = f'{vul_method_detail["signature"]}(..., <em>{vul_method_detail["sourceValues"]}</em>, ...)'
        else:
            vul_method_detail["code"] = vul_method_detail["signature"]
        return vul_method_detail

    def loop(self, index, size, current_link, source_hash):
        for sub_index in range(index + 1, size):
            sub_method = self.method_pool[sub_index]
            sub_target_hash = set(sub_method.get("targetHash"))
            sub_target_rpc_hash = set(sub_method.get("targetHashForRpc", []))
            if (
                (sub_target_hash and sub_target_hash & source_hash)
                or (sub_target_rpc_hash and sub_target_rpc_hash & source_hash)
            ) and check_service_propagate_method_state(sub_method):
                logger.info(f"stisfied {sub_method}")
                if sub_method.get("source"):
                    current_link.append(self.copy_method(sub_method, source=True))
                    self.vul_source_signature = (
                        f"{sub_method.get('className')}.{sub_method.get('methodName')}"
                    )
                    self.vul_stack.append(current_link[::-1])
                    self.taint_value = sub_method["targetValues"]
                    current_link.pop()
                    return True
                current_link.append(self.copy_method(sub_method, propagator=True))
                old_pool_value = source_hash
                source_hash = set(sub_method.get("sourceHash"))
                if self.loop(sub_index, size, current_link, source_hash):
                    return True
                source_hash = old_pool_value
                current_link.pop()
            else:
                logger.debug("not stisfied {sub_method}")
        return None

    def search_sink(self, method_pool, vul_method_signature):
        self.prepare(method_pool, vul_method_signature)
        if vul_method_signature in self.method_pool_signatures:
            return True
        return None

    def dfs(self, current_hash, left_node, left_index):
        """
        深度优先搜索,搜索污点流图中的边
        :param current_hash: 当前污点数据,set()
        :param left_node: 上层节点方法的调用ID
        :param left_index: 上层节点方法在方法队列中的编号
        :return:
        """
        not_found = True
        for index in range(left_index + 1, self.method_counts):
            data = self.method_pool_asc[index]
            if current_hash & set(data["sourceHash"]):
                not_found = False
                right_node = str(data["invokeId"])
                self.graph_data["edges"].append(
                    {
                        "id": str(self.edge_code),
                        "source": left_node,
                        "target": right_node,
                    }
                )
                self.edge_code = self.edge_code + 1
                data["sourceHash"] = list(set(data["sourceHash"]) - current_hash)
                self.dfs(set(data["targetHash"]), right_node, index)

        if not_found:
            self.taint_link_size = self.taint_link_size + 1

    def create_node(self):
        """
        创建污点流图中使用的节点数据
        :return:
        """
        for data in self.method_pool_asc:
            source = ",".join([str(_) for _ in data["sourceHash"]])
            target = ",".join([str(_) for _ in data["targetHash"]])
            node = {
                "id": str(data["invokeId"]),
                "name": f"{data['className'].replace('/', '.').split('.')[-1]}.{data['methodName']}({source}) => {target}",
                "dataType": "source" if data["source"] else "sql",
                "conf": [
                    {"label": "source", "value": source},
                    {"label": "target", "value": target},
                    {
                        "label": "caller",
                        "value": f"{data['callerClass']}.{data['callerMethod']}()",
                    },
                ],
            }
            self.graph_data["nodes"].append(node)

    def result(self):
        if self.version == 3:
            self.taint_value = parse_target_value(self.taint_value)
        if self.vul_source_signature:
            return (
                True,
                self.vul_stack,
                self.vul_source_signature,
                self.vul_method_signature,
                self.taint_value,
            )
        return False, None, None, None, None

    def get_taint_links(self):
        return self.graph_data, self.taint_link_size, self.method_counts


def check_service_propagate_method_state(method):
    if (
        method.get("traceId", "")
        and not method.get("servicePropagateMethodState", False)
        and not method.get("source", False)
    ):
        return False
    return True
