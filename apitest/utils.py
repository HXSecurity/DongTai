######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : utils
# @created     : 星期二 1月 11, 2022 15:57:12 CST
#
# @description :
######################################################################

import json
from tempfile import NamedTemporaryFile
import os
import yaml


#with open("webapi.json") as fp:
#    result = json.load(fp)
#
#data = result['data']
#schema = {}
parameter_type_swagger_type_manreadable_dict = {
    'string': ['java.lang.String'],
    'int': [],
    'boolean': [],
    'number': [],
}


def cover_dict(dic):
    res_dic = {}
    for k, v in dic.items():
        for i in v:
            res_dic[i] = k
    return res_dic


def cover_parameter(parameter, parameter_type_dict):
    swagger_parameter = {"schema": {}}
    swagger_parameter['schema']['type'] = parameter_type_dict.get(
        parameter['parameter_type'], None)
    swagger_parameter['name'] = parameter['name']
    swagger_parameter['in'] = swagger_in(parameter)
    return swagger_parameter


def swagger_in(parameter):
    if parameter['annotation'] == 'GET请求参数':
        return 'query'
    elif parameter['annotation'] == 'restful访问参数':
        return 'path'
    return 'body'


def swagger_trans(data):
    parameter_type_dict = cover_dict(
        parameter_type_swagger_type_manreadable_dict)
    for api in [data[0]]:
        obj = {}
        covered_parameter = map(
            lambda x: cover_parameter(x, parameter_type_dict),
            api['parameters'])
        query_and_path_parameter = list(
            filter(lambda x: x['in'] in ['query', 'path'], covered_parameter))
        body_parameters = list(
            filter(lambda x: x['in'] in ['body'], covered_parameter))
        context = {}
        context['parameters'] = query_and_path_parameter
        if body_parameters:
            covered_properties = {}
            for parameter in body_parameters:
                covered_properties[parameter['name']] = {"type": parameter["type"]}
            context['content'] = {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": covered_properties
                        }
                    }
                }
            }
        for method in api['method']['httpmethods']:
            _method = method.lower()
            obj[_method] = context
            obj[_method]['operationId'] = api['path'] + _method
            obj[_method]['responses'] = {
                "200": {
                    "content": {
                        "application/vnd.oai.openapi+json": {
                            "schema": {
                                "type": "object",
                                "additionalProperties": {}
                            }
                        },
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "additionalProperties": {}
                            }
                        }
                    },
                    "description": ""
                }
            }
        schema[api['path']] = obj

    swagger = {
        "openapi": "3.0.3",
        "info": {
            "title": "DongTai WebApi Doc",
            "version": "0.0.1"
        },
        "paths": schema,
        "components": {
            "schemas": {}
        }
    }
    return swagger


def runtest(swagger, headers):
    with NamedTemporaryFile(delete=False) as swaggerjson, NamedTemporaryFile(
            delete=False) as headers_yml:
        headers = {'all': {'Authorization': 'Token 21312331223132'}}
        with open(swaggerjson.name, 'w') as fp:
            json.dump(swagger, fp)
        with open(headers_yml.name, 'w') as fp:
            yaml.dump(headers, fp)
        os.system(
            f'./cats-linux --contract={swaggerjson.name} --headers={headers_yml.name} --server=http://localhost:8000 --fuzzers=HappyFuzzer  --reportFormat=HTML_ONLY &'
        )
