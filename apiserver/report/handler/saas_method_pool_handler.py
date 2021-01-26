#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/5 下午12:36
# software: PyCharm
# project: lingzhi-webapi
import time, json
from hashlib import sha1

from apiserver.models.agent import IastAgent
from apiserver.models.agent_method_pool import IastAgentMethodPool
from apiserver.report.handler.report_handler_interface import IReportHandler


class SaasMethodPoolHandler(IReportHandler):
    def parse(self):
        self.http_uri = self.detail.get('http_uri')
        self.http_url = self.detail.get('http_url')
        self.http_query_string = self.detail.get('http_query_string')
        self.http_req_data = self.detail.get('http_req_data')
        self.http_req_header = self.detail.get('http_req_header')
        self.http_method = self.detail.get('http_method')
        self.http_scheme = self.detail.get('http_scheme')
        self.http_secure = self.detail.get('http_secure')
        self.http_protocol = self.detail.get('http_protocol')
        self.http_res_header = self.detail.get('http_res_header')
        self.http_res_body = self.detail.get('http_res_body')
        self.context_path = self.detail.get('context_path')
        self.vuln_type = self.detail.get('vuln_type')
        self.language = self.detail.get('language', 'Java')
        self.agent_name = self.detail.get('agent_name')
        self.taint_value = self.detail.get('taint_value')
        self.taint_position = self.detail.get('taint_position')
        self.client_ip = self.detail.get('http_client_ip')
        self.param_name = self.detail.get('param_name')
        self.method_pool = self.report.get('detail', {}).get('pool', None)
        if self.method_pool:
            self.method_pool = sorted(self.method_pool, key=lambda e: e.__getitem__('invokeId'), reverse=True)

    def save(self):
        # 数据存储
        # 计算唯一签名，确保数据唯一
        # 数据存储
        agent = IastAgent.objects.filter(token=self.agent_name, user=self.user_id).first()
        if agent:
            pool_sign = self.calc_hash()
            method_pool = IastAgentMethodPool.objects.filter(pool_sign=pool_sign, agent=agent).first()
            if method_pool:
                method_pool.update_time = int(time.time())
                method_pool.save()
            else:
                # 获取agent
                timestamp = int(time.time())
                IastAgentMethodPool(
                    agent=agent,
                    url=self.http_url,
                    uri=self.http_uri,
                    http_method=self.http_method,
                    http_scheme=self.http_scheme,
                    http_protocol=self.http_protocol,
                    req_header=self.http_req_header,
                    req_params=self.http_query_string,
                    req_data=self.http_req_data,  # fixme 增加客户端获取响应体
                    res_header=self.http_res_header,
                    res_body=self.http_res_body,
                    context_path=self.context_path,
                    language=self.language,
                    method_pool=json.dumps(self.method_pool),
                    pool_sign=pool_sign,
                    clent_ip=self.client_ip,
                    create_time=timestamp,
                    update_time=timestamp
                ).save()

    def calc_hash(self):
        sign_raw = ''
        for method in self.method_pool:
            sign_raw += f"{method.get('className')}.{method.get('methodName')}()->"
        sign_sha1 = self.sha1(sign_raw)
        return sign_sha1

    @staticmethod
    def sha1(raw):
        h = sha1()
        h.update(raw.encode('utf-8'))
        return h.hexdigest()

    def demo_print(self, class_name, method_name):
        # todo 搜索时，实时计算
        hit_sink = False
        stack = list()
        pool_value = -1
        for method in sorted_pool:
            if method.get('className') == class_name and method.get('methodName') == method_name:
                print('发现sink点')
                hit_sink = True
                stack.append(method)
                pool_value = method.get('sourceHash')[0]
                continue
            if hit_sink:
                is_source = method.get('source')
                target_hash = method.get('targetHash')

                if is_source:
                    for hash in target_hash:
                        if hash == pool_value:
                            stack.append(method)
                            print('发现source点')
                            # break
                else:
                    for hash in target_hash:
                        if hash == pool_value:
                            stack.append(method)
                            pool_value = method.get('sourceHash')[0]
                            break

        tree = stack[::-1]
        for method in tree:
            print(
                f"{method.get('className')}.{method.get('methodName')}() 污点：{method.get('sourceHash')}->{method.get('targetHash')}")


if __name__ == '__main__':
    import json

    with open('../../../doc/example.json', 'r') as f:
        pool = json.load(f).get('detail', {}).get('pool', None)
    print(pool if pool is None else len(pool))

    sorted_pool = sorted(pool, key=lambda e: e.__getitem__('invokeId'), reverse=True)

    # todo 搜索时，实时计算
    class_name = 'java.sql.Statement'
    method_name = 'executeQuery'
    handler = SaasMethodPoolHandler()
    handler.method_pool = sorted_pool
    handler.demo_print(class_name, method_name)
