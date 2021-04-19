#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午3:59
# software: PyCharm
# project: lingzhi-webapi
from base.endpoint import MixinAuthPoxyView


class EngineHookRuleTypesEndPoint(MixinAuthPoxyView):
    source = 'api/engine/hook/rule_types'
