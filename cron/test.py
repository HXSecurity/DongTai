#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/25 下午6:54
# software: PyCharm
# project: lingzhi-engine
import json
import time

from vuln.models.agent_method_pool import IastAgentMethodPool
from vuln.models.hook_strategy_type import HookStrategyType
from vuln.models.hook_strategy_type_relation import IastHookStrategyTypeRelation
from vuln.models.strategy import IastStrategyModel
from vuln.models.vulnerablity import IastVulnerabilityModel


def queryset_to_iterator(queryset):
    page_size = 10
    page = 1
    while True:
        temp_queryset = queryset[(page - 1) * page_size:page * page_size - 1]
        page += 1
        yield temp_queryset


def load_sink_strategy():
    strategies = list()
    strategy_types = HookStrategyType.objects.filter(type=4)
    relations = IastHookStrategyTypeRelation.objects.filter(
        type__in=(strategy_types if strategy_types else []))
    for relations in queryset_to_iterator(relations):
        if relations:
            for relation in relations:
                strategies.append({
                    'type': relation.strategy_type.value,
                    'value': relation.strategy.value.split('(')[0]
                })
        else:
            break
    return strategies


def find(sorted_pool, sink_signature):
    # todo 搜索时，实时计算
    hit_sink = False
    stack = list()
    pool_value = -1
    vul_source_signature = ''
    for method in sorted_pool:
        if f"{method.get('className')}.{method.get('methodName')}" == sink_signature:
            hit_sink = True
            stack.append(method)
            pool_value = method.get('sourceHash')
            continue
        if hit_sink:
            is_source = method.get('source')
            target_hash = method.get('targetHash')

            if is_source:
                for hash in target_hash:
                    if hash in pool_value:
                        stack.append(method)
                        vul_source_signature = f"{method.get('className')}.{method.get('methodName')}"
                        break
            else:
                for hash in target_hash:
                    if hash in pool_value:
                        stack.append(method)
                        pool_value = method.get('sourceHash')
                        break

    if vul_source_signature:
        return True, stack, vul_source_signature, sink_signature
    else:
        pass
        # print('未找到污点调用链')
    return False, None, None, None


def load_method_pool():
    page_size = 10
    page = 1
    queryset = IastAgentMethodPool.objects.all()
    while True:
        temp_queryset = queryset[(page - 1) * page_size:page * page_size - 1]
        page += 1
        yield temp_queryset


def save_vul(vul_meta, vul_level, vul_stack, top_stack, bottom_stack):
    iast_vuls = IastVulnerabilityModel.objects.filter(
        type='',  # 指定漏洞类型
        url=vul_meta.url,
        http_method=vul_meta.http_method,
        taint_position='',  # 或许补充相关数据
        agent=vul_meta.agent
    )
    if iast_vuls:
        vul = iast_vuls[0]
        vul.req_header = vul_meta.req_header
        vul.req_params = vul_meta.req_params
        # vul.full_stack = json.dumps(self.app_caller, ensure_ascii=False),
        # vul.top_stack = top_stack,
        # vul.bottom_stack = bottom_stack,
        vul.counts = iast_vuls[0].counts + 1
        vul.latest_time = int(time.time())
        vul.status = 'reported'
        vul.save()
    else:
        vul = IastVulnerabilityModel(
            type='',
            level=vul_level,
            url=vul_meta.url,
            uri=vul_meta.uri,
            http_method=vul_meta.http_method,
            http_scheme=vul_meta.http_scheme,
            http_protocol=vul_meta.http_protocol,
            req_header=vul_meta.req_header,
            req_params=vul_meta.req_params,
            req_data=vul_meta.req_data,
            res_header=vul_meta.res_header,
            res_body=vul_meta.res_body,
            full_stack=json.dumps(vul_stack, ensure_ascii=False),
            top_stack=top_stack,
            bottom_stack=bottom_stack,
            taint_value='',  # fixme: 污点数据，后续补充
            taint_position='',  # fixme 增加污点位置
            agent=vul_meta.agent,
            context_path=vul_meta.context_path,
            counts=1,
            status='reported',
            language=vul_meta.language,
            first_time=vul_meta.create_time,
            latest_time=int(time.time()),
            client_ip=vul_meta.clent_ip,  # fixme 数据库字段创建错误
            param_name=''
        )
        vul.save()


def demo_print():
    # 从数据库搜索
    method_pool_size = IastAgentMethodPool.objects.count()
    if method_pool_size > 0:
        strategies = load_sink_strategy()
        for queryset in load_method_pool():
            if queryset:
                for row in queryset:
                    method_pool = json.loads(row.method_pool)
                    sorted_method_pool = sorted(method_pool, key=lambda e: e.__getitem__('invokeId'), reverse=True)
                    for strategy in strategies:
                        status, stack, source_sign, sink_sign = find(sorted_method_pool, strategy['value'])
                        if status:
                            vul_strategy = IastStrategyModel.objects.filter(vul_type=strategy['type']).first()
                            if vul_strategy:
                                save_vul(row, vul_strategy.level, stack, source_sign, sink_sign)
                                print(row.url)
            else:
                break


if __name__ == '__main__':
    demo_print()
