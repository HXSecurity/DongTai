#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:44
# software: PyCharm
# project: lingzhi-engine

RULE_USER = 'user'
RULE_SYSTEM = 'system'
RULE_IS_SYSTEM = 1
RULE_IS_ENABLE = 1

USER_BUGENV = 'dt-range'

# hook rule
ENABLE = 1
DISABLE = 0
DELETE = -1

SYSTEM_USER_ID = 1

RULE_PROPAGATOR = 1
RULE_SOURCE = 2
RULE_FILTER = 3
RULE_SINK = 4
RULE_ENTRY_POINT = 5

# 限制每页的最大数量
MAX_PAGE_SIZE = 50

# 定义重放类型
VUL_REPLAY = 1
REQUEST_REPLAY = 2

# 定义重放数据类型
PENDING = 0
WAITING = 1
SOLVED = 2
SOLVING = 3

# 定义漏洞验证结果
RECHECK_ERROR = 2
RECHECK_TRUE = 1
RECHECK_FALSE = 0
