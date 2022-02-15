#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2022/1/17 下午7:25
# project: DongTai-engine
import requests
from dongtai.endpoint import UserEndPoint, R
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool


class ProxyEndPoint(UserEndPoint):
    """
    引擎注册接口
    """
    name = "api-engine-run"
    description = "引擎运行策略"

    @staticmethod
    def send_request(method_pool, proxy_addr):
        url = f'{method_pool["url"]}?{method_pool["req_params"]}' if method_pool['req_params'] else method_pool[
            'url']
        header_items = method_pool['req_header_fs'].split('\n')[1:]
        headers = {}
        for header_item in header_items:
            sub_items = header_item.split(':')
            headers[sub_items[0]] = ':'.join(sub_items[1:])
        resp = requests.request(
            method=method_pool["http_method"],
            data=method_pool['req_data'] if method_pool['req_data'] else '',
            url=url,
            headers=headers,
            proxies={'http': f'http://{proxy_addr}', 'https': f'https://{proxy_addr}'}
        )
        print(resp.text)

    def get(self, request):
        """
        IAST下载 agent接口 http://localhost:8000/api/engine/proxy?projectId=1195&projectVersionId=992&proxy=http://localhost:5555
        :param request:
        :return:
        """
        try:
            project_id = request.query_params.get('projectId')
            project_version_id = request.query_params.get('projectVersionId')
            proxy_addr = request.query_params.get('proxy')
            method_pools = MethodPool.objects.filter(
                agent__in=IastAgent.objects.filter(bind_project_id=project_id, project_version_id=project_version_id, user=request.user)
            ).values('url', 'http_method', 'req_params', 'req_data', 'req_header_fs')
            for method_pool in method_pools:
                ProxyEndPoint.send_request(method_pool, proxy_addr)
            return R.success()
        except Exception as e:
            return R.failure(msg=f"{e}")
