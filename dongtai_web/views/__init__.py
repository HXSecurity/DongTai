#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:shengnanwu
# datetime:2020/5/21 15:50
# software: PyCharm
# project: webapi


from _typeshed import Incomplete
AGENT_STATUS: Incomplete = {
    0: {
        "key": "无下发指令",
        "value": "notcmd",
    },
    2: {
        "key": "注册启动引擎",
        "value": "coreRegisterStart",
    },
    3: {
        "key": "开启引擎核心",
        "value": "coreStart",
    },
    4: {
        "key": "关闭引擎核心",
        "value": "coreStop",
    },
    5: {
        "key": "卸载引擎核心",
        "value": "coreUninstall",
    },
    6: {
        "key": "强制开启引擎核心性能熔断",
        "value": "corePerformanceForceOpen",
    },
    7: {
        "key": "强制关闭引擎核心性能熔断",
        "value": "corePerformanceForceClose",
    },
    8: {
        "key": "Agent升级",
        "value": "update",
    },
}
