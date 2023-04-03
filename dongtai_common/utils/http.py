#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/21 下午6:21
# project: dongtai-engine
import base64
import logging

logger = logging.getLogger('dongtai-core')


def build_request(req_method, raw_req_header, uri, query_params, req_data, http_protocol):
    decode_req_header = base64.b64decode(raw_req_header).decode('utf-8').strip()
    headers = f"{req_method} {uri + ('?' + query_params if query_params else '')} {http_protocol}\n{decode_req_header}\n\n{req_data if req_data else ''}"
    return headers


def build_response(header, body):
    try:
        _data = base64.b64decode(header.encode("utf-8")).decode("utf-8")
    except Exception as e:
        _data = ''
        logger.warning(f'Response Header解析出错，错误原因：{e}', exc_info=e)
    return '{header}\n\n{body}'.format(header=_data, body=body)
