from django.test import TestCase

# Create your tests here.
from copy import deepcopy

from core.engine_v2 import VulEngineV2


class TaintTree:
    def __init__(self):
        self.raw_graph_data = {}

    def create_graph(self):
        pass

    @staticmethod
    def is_invalid_node(classname):
        return classname in (
            'java.util.List',
            'java.lang.String',
            'java.lang.StringBuilder',
            'java.io.StringReader',
            'java.util.Enumeration',
            'java.util.Map',
        )

    @staticmethod
    def filter_invalid_node(node_id):
        global raw_node_data
        node = raw_node_data[int(node_id)]
        if TaintTree.is_invalid_node(node['className']):
            return False
        return True

    @staticmethod
    def remove_invalid(raw_graph_data, raw_node_data):
        has_invalid = False
        invalid_node = list()
        for head, subs in raw_graph_data.items():
            if not subs:
                invalid_node.append(head)

        for head in invalid_node:
            del raw_graph_data[head]

        raw_graph_data_copy = deepcopy(raw_graph_data)

        sorted_graph_data = sorted(raw_graph_data_copy.keys(), reverse=True)
        for key in sorted_graph_data:
            sub_nodes = raw_graph_data_copy[key]
            sub_node_count = len(sub_nodes)
            raw_graph_data[key] = list(filter(TaintTree.filter_invalid_node, sub_nodes))
            new_sub_node_count = len(raw_graph_data[key])
            if sub_node_count != new_sub_node_count:
                has_invalid = True
        return has_invalid, raw_graph_data, raw_node_data


def load_data():
    import json
    with open('/tmp/graph.json', 'r') as f:
        data = json.load(f)
    return data


def create_node_data(node):
    return node


if __name__ == '__main__':
    data = load_data()
    engine = VulEngineV2()
    engine.prepare(data, '')
    engine.search_all_link()
    data, link_size, method_count = engine.get_taint_links()
    print(len(data['edges']))
    print(len(data['nodes']))
    print(data)
