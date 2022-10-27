#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/9/28 上午10:51
# project: dongtai-openapi
from drf_spectacular.utils import OpenApiParameter, OpenApiExample


from _typeshed import Incomplete
class DongTaiAuth:
    TOKEN: str = 'TokenAuthentication'


class DongTaiParameter:
    OPENAPI_URL: Incomplete = OpenApiParameter(
        name='url',
        description='OpenAPI Service Addr',
        required=True,
        type=str,
        examples=[
            OpenApiExample(
                'url example',
                summary='default',
                value='https://openapi.iast.io',
            ),
        ],
    )
    PROJECT_NAME: Incomplete = OpenApiParameter(
        name='projectName',
        type=str,
        description='The name of the project where the Agent needs to be installed',
        examples=[
            OpenApiExample(
                'example with https://iast.io',
                summary='default',
                value='Demo Project',
            ),
        ],
    )

    LANGUAGE: Incomplete = OpenApiParameter(
        name='language',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='JAVA or PYTHON',
                value='JAVA',
            ),
        ],
    )

    VERSION: Incomplete = OpenApiParameter(
        name='version',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    AGENT_NAME: Incomplete = OpenApiParameter(
        name='name',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    HOSTNAME: Incomplete = OpenApiParameter(
        name='engineName',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    NETWORK: Incomplete = OpenApiParameter(
        name='engineName',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    CONTAINER_NAME: Incomplete = OpenApiParameter(
        name='containerName',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )


    SERVER_ADDR: Incomplete = OpenApiParameter(
        name='serverAddr',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    SERVER_PORT: Incomplete = OpenApiParameter(
        name='serverPort',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    SERVER_PATH: Incomplete = OpenApiParameter(
        name='serverPath',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    SERVER_ENV: Incomplete = OpenApiParameter(
        name='serverEnv',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    PID: Incomplete = OpenApiParameter(
        name='pid',
        type=str,
        description=
        'The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )

    AUTO_CREATE_PROJECT: Incomplete = OpenApiParameter(
        name='autoCreateProject',
        type=int,
        description=
        'auto create project if project not found when this varibale is 1',
        required=True,
        examples=[
            OpenApiExample(
                'default value',
                value=0,
            ),
            OpenApiExample(
                'enable value',
                value=1,
            ),
        ],
    )
    ENGINE_NAME: Incomplete = OpenApiParameter(
        name='engineName',
        type=str,
        description='The development language of the project that needs to install the Agent',
        required=True,
        examples=[
            OpenApiExample(
                'example language',
                summary='java or python',
                value='java',
            ),
        ],
    )
