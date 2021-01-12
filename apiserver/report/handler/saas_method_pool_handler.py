#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/5 下午12:36
# software: PyCharm
# project: lingzhi-webapi

from hashlib import sha1

from apiserver.report.handler.report_handler_interface import IReportHandler


class SaasMethodPoolHandler(IReportHandler):
    def parse(self):
        self.method_pool = self.report.get('detail', {}).get('pool', None)
        if self.method_pool:
            self.method_pool = sorted(self.method_pool, key=lambda e: e.__getitem__('invokeId'), reverse=True)

    def save(self):
        # 数据存储
        # 计算唯一签名，确保数据唯一
        # 数据存储
        sign = self.calc_hash()
        #
        print(f"{sign}")

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
