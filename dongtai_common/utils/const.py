#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/12 下午5:52

# report
REPORT_HEART_BEAT: int
STRATEGY_ENABLE: str
CORE_IS_RUNNING: int
VUL_REPLAY: int
PENDING: int
RECHECK_ERROR: int
VUL_WAITING: str
HOOK_TYPE_ENABLE: int
ENABLE: int
RULE_PROPAGATOR: int
RULE_USER: str
MAX_PAGE_SIZE: int
REPORT_HEART_BEAT = 0x01
REPORT_SCA: int = 0x11
REPORT_VULN_NORNAL: int = 0x21
REPORT_VULN_DYNAMIC: int = 0x22
REPORT_VULN_OVER_POWER: int = 0x23
REPORT_VULN_SAAS_POOL: int = 0x24
REPORT_VULN_HARDCODE: int = 0x25

REPORT_AUTH_ADD: int = 0x31
REPORT_AUTH_UPDATE: int = 0x32
REPORT_ERROR_LOG: int = 0x51
REPORT_API_ROUTE: int = 0x61
REPORT_THIRD_PARTY_SERVICE: int = 0x81
REPORT_FILE_PATH: int = 0x82


# strategy
STRATEGY_ENABLE = 'enable'
STRATEGY_DISABLE: str = 'disable'

RUNNING: int = 1

# 定义Agent运行状态
CORE_IS_RUNNING = 1
CORE_NOT_RUNNING: int = 0

# 定义重放类型
VUL_REPLAY = 1
REQUEST_REPLAY: int = 2
API_REPLAY: int = 3 

# 定义重放数据类型
PENDING = 0
WAITING: int = 1
SOLVED: int = 2
SOLVING: int = 3
DISCARD: int = 4

# 定义漏洞验证结果
RECHECK_ERROR = 2
RECHECK_TRUE: int = 1
RECHECK_FALSE: int = 0
RECHECK_DISCARD: int = 3

# 定义漏洞状态
VUL_WAITING = '待验证'
VUL_VERIFY: str = '验证中'
VUL_TRUE: str = '已确认'
VUL_FALSE: str = '已忽略'

# hook strategy type
HOOK_TYPE_ENABLE = 1
HOOK_TYPE_DISABLE: int = 0

USER_BUGENV: str = 'dt-range'

SYSTEM_USER_ID: int = 1

# 定义规则状态
ENABLE = 1
DISABLE: int = 0
DELETE: int = -1

# 定义规则类型
RULE_PROPAGATOR = 1
RULE_SOURCE: int = 2
RULE_FILTER: int = 3
RULE_SINK: int = 4
RULE_ENTRY_POINT: int = 5

# 定义规则对应的用户
RULE_USER = 'user'
RULE_SYSTEM: str = 'system'
RULE_IS_SYSTEM: int = 1
RULE_IS_ENABLE: int = 1

# 限制每页的最大数量
MAX_PAGE_SIZE = 50

VUL_PENDING: int = 1
VUL_VERIFYING: int = 2
VUL_CONFIRMED: int = 3
VUL_IGNORE: int = 4
VUL_SOLVED: int = 5
