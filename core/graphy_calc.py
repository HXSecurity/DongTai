#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/20 下午8:19
# software: PyCharm
# project: lingzhi-engine

import json
from copy import deepcopy

raw_data = [{"args": "", "source": False, "invokeId": 1289, "className": "java.lang.StringBuilder",
             "signature": "()Ljava/lang/String;", "interfaces": [], "methodName": "toString", "sourceHash": [990473952],
             "targetHash": [460870371], "callerClass": "org.springframework.util.StringUtils",
             "callerMethod": "cleanPath", "retClassName": "", "callerLineNumber": 709}]

graphy_data = {
    'nodes': [],
    'edges': []
}
raw_data = raw_data[::-1]
# 遍历，寻找点
for data in raw_data:
    node = {
        'id': str(data['invokeId']),
        'name': f"{data['className']}.{data['methodName']}()",
        'dataType': 'source' if data['source'] else 'sql',
        'conf': [
            {'label': 'source', 'value': ','.join([str(_) for _ in data['sourceHash']])},
            {'label': 'target', 'value': ','.join([str(_) for _ in data['targetHash']])},
            {'label': 'caller', 'value': f"{data['callerClass']}.{data['callerMethod']}()"}
        ]
    }
    graphy_data['nodes'].append(node)

current_hash = None
left_node = None
right_node = None

# fixme: 解决节点关系计算的方法

max_size = len(raw_data)
taint_link_size = 0
link = list()


def dfs(current_hash, left_node, left_index):
    global taint_link_size, link
    not_found = True
    for index in range(left_index + 1, max_size):
        data = raw_data[index]
        if current_hash & set(data['sourceHash']):
            not_found = False
            right_node = str(data['invokeId'])
            graphy_data['edges'].append({
                'source': left_node,
                'target': right_node,
            })
            link.append(right_node)
            # 将匹配到的hash值从source中删除，避免重复判断
            data['sourceHash'] = list(set(data['sourceHash']) - current_hash)
            dfs(set(data['targetHash']), right_node, index)
            link = link[:-1]

    if not_found:
        taint_link_size = taint_link_size + 1
        _link = deepcopy(link)
        str_link = ''
        for _ in _link:
            str_link += f' -> {_}'
        print(str_link[4:])
        pass


for index in range(max_size):
    data = raw_data[index]
    if data['source']:
        current_hash = set(data['targetHash'])
        left_node = str(data['invokeId'])
        link.append(left_node)
        dfs(current_hash, left_node, index)

json_graphy_data = json.dumps(graphy_data)

print(f'共发现{taint_link_size}条调用链')
