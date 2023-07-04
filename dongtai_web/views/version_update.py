#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
import base64
import logging

from dongtai_common.endpoint import R, TalentAdminEndPoint
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.profile import IastProfile
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema

logger = logging.getLogger('dongtai-webapi')


class MethodPoolVersionUpdate(TalentAdminEndPoint):
    @extend_schema(
        summary="版本更新",
        tags=["Version Update"],
    )
    def get(self, request):
        profile_model = IastProfile.objects.filter(key='enable_update').first()
        if profile_model is None or profile_model.value != 'TRUE':
            return R.failure(msg=_('Updated is currently not allowed'))
        method_pools = MethodPool.objects.all()
        length = 5
        index = 0
        while True:
            start = index * length
            end = (index + 1) * length
            print(start)
            print(end)
            sub_method_pools = method_pools.values('id', 'http_method', 'req_header', 'uri', 'req_params',
                                                   'http_protocol', 'res_header')[start:end]
            for method_pool in sub_method_pools:
                id = method_pool['id']
                http_method = method_pool['http_method']
                req_header = method_pool['req_header']
                uri = method_pool['uri']
                req_params = method_pool['req_params']
                http_protocol = method_pool['http_protocol']
                res_header = method_pool['res_header']
                MethodPool.objects.filter(id=id).update(
                    req_header_fs=build_request_header(http_method, req_header, uri, req_params, http_protocol),
                    res_header=base64_decode(res_header)
                )
            if len(sub_method_pools) == length:
                index = index + 1
            else:
                break
        profile_model.value = 'FALSE'
        profile_model.save(update_fields=['value'])
        return R.success(msg=_('Update completed'))


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
