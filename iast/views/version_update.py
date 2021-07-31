#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/29 下午4:56
# project: dongtai-webapi
from dongtai.endpoint import AnonymousAndUserEndPoint, R
from dongtai.models.agent_method_pool import MethodPool
from dongtai.models.asset import Asset
from dongtai.models.profile import IastProfile
from iast.serializers.sca import ScaSerializer
import base64
import logging

logger = logging.getLogger('dongtai-webapi')


class MethodPoolVersionUpdate(AnonymousAndUserEndPoint):
    def get(self, request):
        updateable = IastProfile.objects.filter(name='updateable')
        if not updateable.value != 'TRUE':
            return R.failure(msg='当前不允许更新')
        method_pools = MethodPool.objects.all()
        for method_pool in method_pools:
            method_pool.req_header_fs = build_request_header(
                method_pool.req_method, method_pool.req_header,
                method_pool.uri, method_pool.req_params,
                method_pool.http_protocol)
            method_pool.res_header = base64_decode(method_pool.res_header)
            method_pool.save(update_fields=['req_header_fs', 'res_header'])
        return R.success(msg='更新成功')


def base64_decode(raw):
    try:
        return base64.b64decode(raw).decode('utf-8').strip()
    except Exception as decode_error:
        logger.error(f'base64 decode error, raw: {raw}\nreason:{decode_error}')
        return ""


def build_request_header(req_method, raw_req_header, uri, query_params,
                         http_protocol):
    decode_req_header = base64_decode(raw_req_header)
    return f"{req_method} {uri + ('?' + query_params if query_params else '')} {http_protocol}\n{decode_req_header}"
