#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 下午7:13
# software: PyCharm
# project: lingzhi-engine
import base64


def reduction_req_headers(req_method, raw_req_header, uri, query_params, req_data, http_protocol):
    decode_req_header = base64.b64decode(raw_req_header).decode('utf-8').strip()
    headers = f"{req_method} {uri + ('?' + query_params if query_params else '')} {http_protocol}\n{decode_req_header}\n\n{req_data if req_data else ''}"
    return headers
