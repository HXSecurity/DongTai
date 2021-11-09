#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/10/22 下午2:29
# project: DongTai-engine
# desc: data rule, response field rule, sql field rule
import re

from core.plugins.strategy_headers import save_vul


def check_response_content(method_pool):
    # todo load sensitive type and rule
    # todo match response content with sensitive rule

    search_phone_number_leak(method_pool)
    search_id_card_leak(method_pool)


def search_phone_number_leak(method_pool):
    status, phone_number = check_phone_number(method_pool.res_body)
    if status:
        # todo: add highlight to phone_number
        save_vul(vul_type='Phone Number Leak', method_pool=method_pool, position='HTTP Response Body',
                 data=phone_number)


def search_id_card_leak(method_pool):
    pattern = re.compile(
        r'([1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx])|([1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3})',
        re.M)
    result = pattern.search(method_pool.res_body)
    if result is None:
        return

    card = result.group(1)
    if check_id_card(card):
        # todo: add highlight to id_card
        save_vul(vul_type='ID Number Leak', method_pool=method_pool, position='HTTP Response Body', data=card)


def check_phone_number(res_body):
    rule = '\D(1[3-9]\d{9})\D'
    pattern = re.compile(rule, re.M)
    result = pattern.search(res_body)
    if result.groups():
        return True, result.group(1)
    return False, None


def check_id_card(id_card):
    try:
        from id_validator import validator
        return validator.is_valid(id_card)
    except:
        return False
