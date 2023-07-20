#!/usr/bin/env python
# datetime: 2021/7/21 下午7:07
from copy import deepcopy

from django.utils.functional import cached_property
from dongtai_common.engine.compatibility import method_pool_3_to_2, method_pool_is_3


class VulEngineV2:
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
        self.node_data = {}
        self.nodes = {}
        self.raw_graph_data = {}
        self.raw_node_data = {}
        self.graphy_data = {"nodes": [], "edges": []}
        self.method_counts = 0
        self.taint_link_size = 0
        self.edge_code = 1

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
            filter(lambda x: not ("type" in x and "stack" in x), method_pool),
            key=lambda e: e.__getitem__("invokeId"),
            reverse=True,
        )

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
        if method_pool_is_3(method_pool[0]):
            method_pool = list(map(method_pool_3_to_2, method_pool))
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
            self.pool_value = method.get("sourceHash")
            return True
        return None

    def do_propagator(self, method, current_link):
        is_source = method.get("source")
        target_hash = method.get("targetHash")

        if is_source:
            for hash in target_hash:
                if hash in self.pool_value:
                    current_link.append(method)
                    self.vul_source_signature = (
                        f"{method.get('className')}.{method.get('methodName')}"
                    )
                    return True
            return None
        else:
            for hash in target_hash:
                if hash in self.pool_value:
                    current_link.append(method)
                    self.pool_value = method.get("sourceHash")
                    break
            return None

    @cached_property
    def method_pool_signatures(self):
        signatures = []
        for method in self.method_pool:
            signatures.append(
                f"{method.get('className').replace('/', '.')}.{method.get('methodName')}"
            )
        return signatures

    def search_sink(self, method_pool, vul_method_signature):
        self.prepare(method_pool, vul_method_signature)
        if vul_method_signature in self.method_pool_signatures:
            return True
        return None

    def search_all_link(self):
        """
        从方法池中搜索所有的污点传播链
        :return:
        """
        self.edge_code = 1
        self.method_pool_asc = self.method_pool[::-1]
        self.create_graph()
        self.create_edge()

    def create_edge(self):
        """
        创建污点链的边
        :return:
        """
        edges = []
        node_ids = set()
        for head, subs in self.raw_graph_data.items():
            node_ids.add(head)
            for sub_node in subs:
                node_ids.add(sub_node)
                edges.append(
                    {"id": str(self.edge_code), "source": str(head), "target": sub_node}
                )
                self.edge_code = self.edge_code + 1

        nodes = [self.raw_node_data[int(node_id)] for node_id in node_ids]
        self.graphy_data["nodes"] = nodes
        self.graphy_data["edges"] = edges

    @staticmethod
    def create_node(data):
        """
        创建污点流图中使用的节点数据
        :return:
        """
        source = ",".join([str(_) for _ in data["sourceHash"]])
        target = ",".join([str(_) for _ in data["targetHash"]])
        classname = data["className"].replace("/", ".").split(".")[-1]
        invoke_id = str(data["invokeId"])
        return {
            "id": invoke_id,
            "name": f"{classname}.{data['methodName']}({source}) => {target}",
            "dataType": "source" if data["source"] else "sql",
            "nodeType": classname,
            "conf": [
                {
                    "label": "调用方法",
                    "value": f"{data['callerClass']}.{data['callerMethod']}()",
                },
                {"label": "行号", "value": data["callerLineNumber"]},
                {"label": "污点来源为", "value": source},
                {"label": "污点转换为", "value": target},
                {"label": "初始污点", "value": data["sourceValues"]}
                if "sourceValues" in data
                else {},
                {"label": "传播后污点", "value": data["targetValues"]}
                if "targetValues" in data
                else {},
            ],
        }

    def create_graph(self):
        node_count = len(self.method_pool_asc)
        for index in range(node_count):
            node = self.method_pool_asc[index]
            invoke_id = node["invokeId"]
            self.raw_node_data[invoke_id] = self.create_node(node)
            if invoke_id not in self.raw_graph_data:
                self.raw_graph_data[invoke_id] = []
            for _index in range(index + 1, node_count):
                _node = self.method_pool_asc[_index]
                if set(node["targetHash"]) & set(_node["sourceHash"]):
                    self.raw_graph_data[invoke_id].append(str(_node["invokeId"]))

    def filter_invalid_data(self):
        raw_node_data_copy = deepcopy(self.raw_node_data)

        while True:
            status, self.raw_graph_data, raw_node_data = self.remove_invalid(
                self.raw_graph_data, raw_node_data_copy
            )
            if status is False:
                break

    def remove_invalid(self, raw_graph_data, raw_node_data):
        has_invalid = False
        invalid_node = []
        for head, subs in raw_graph_data.items():
            if not subs:
                invalid_node.append(head)

        for head in invalid_node:
            del raw_graph_data[head]

        sorted_graph_data = sorted(raw_graph_data.keys(), reverse=True)
        for key in sorted_graph_data:
            sub_nodes = raw_graph_data[key]
            leaf_nodes = list(filter(lambda x: int(x) not in raw_graph_data, sub_nodes))
            if leaf_nodes:
                filtered_leaf_nodes = set(filter(self.filter_invalid_node, leaf_nodes))
                raw_graph_data[key] = filtered_leaf_nodes | (
                    set(sub_nodes) - set(leaf_nodes)
                )
                filtered_node_count = len(filtered_leaf_nodes)
                sub_node_count = len(leaf_nodes)
                if sub_node_count != filtered_node_count:
                    has_invalid = True
        return has_invalid, raw_graph_data, raw_node_data

    @staticmethod
    def is_invalid_node(classname):
        return classname in (
            "List",
            "String",
            "StringBuilder",
            "StringReader",
            "Enumeration",
            "Map",
        )

    def filter_invalid_node(self, node_id):
        node = self.raw_node_data[int(node_id)]
        if self.is_invalid_node(node["nodeType"]):
            return False
        return True

    def result(self):
        if self.vul_source_signature:
            return (
                True,
                self.vul_stack,
                self.vul_source_signature,
                self.vul_method_signature,
            )
        return False, None, None, None

    def get_taint_links(self):
        return self.graphy_data, self.taint_link_size, self.method_counts
