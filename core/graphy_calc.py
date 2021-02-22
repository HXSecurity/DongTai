#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/20 下午8:19
# software: PyCharm
# project: lingzhi-engine

import json

raw_data = [
    {
        "args": "",
        "source": False,
        "invokeId": 1341,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            918648385
        ],
        "targetHash": [
            527672964
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 319
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1340,
        "className": "java.lang.String",
        "signature": "(I)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            918648385
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 319
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1339,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            1690262188
        ],
        "targetHash": [
            -1498490962
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1338,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            1690262188
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1337,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            859356366
        ],
        "targetHash": [
            1822942858
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1336,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            859356366
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1335,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            32233407
        ],
        "targetHash": [
            938077714
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1334,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            32233407
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1333,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            802143350
        ],
        "targetHash": [
            -1030149762
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1332,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            802143350
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1331,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            1527879733
        ],
        "targetHash": [
            1677326280
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1330,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            1527879733
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1329,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            791915094
        ],
        "targetHash": [
            1414048452
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1328,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            791915094
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1327,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            1770239284
        ],
        "targetHash": [
            -1082243220
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1326,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            1770239284
        ],
        "callerClass": "org.springframework.util.MimeTypeUtils",
        "callerMethod": "tokenize",
        "retClassName": "",
        "callerLineNumber": 309
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1325,
        "className": "java.util.List",
        "signature": "([Ljava/lang/Object;)[Ljava/lang/Object;",
        "interfaces": [],
        "methodName": "toArray",
        "sourceHash": [
            1207614116
        ],
        "targetHash": [
            450740580
        ],
        "callerClass": "org.springframework.util.StringUtils",
        "callerMethod": "toStringArray",
        "retClassName": "",
        "callerLineNumber": 910
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1324,
        "className": "java.util.List",
        "signature": "(Ljava/lang/Object;)Z",
        "interfaces": [],
        "methodName": "add",
        "sourceHash": [
            2142983734
        ],
        "targetHash": [
            1207614116
        ],
        "callerClass": "java.util.Collections",
        "callerMethod": "list",
        "retClassName": "",
        "callerLineNumber": 5247
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1323,
        "className": "java.util.Enumeration",
        "signature": "()Ljava/lang/Object;",
        "interfaces": [],
        "methodName": "nextElement",
        "sourceHash": [
            691753681
        ],
        "targetHash": [
            2142983734
        ],
        "callerClass": "java.util.Collections",
        "callerMethod": "list",
        "retClassName": "",
        "callerLineNumber": 5247
    },
    {
        "args": "",
        "source": True,
        "invokeId": 1322,
        "className": "javax/servlet/http/HttpServletRequestWrapper",
        "signature": "(Ljava/lang/String;)Ljava/util/Enumeration;",
        "interfaces": [],
        "methodName": "getHeaders",
        "sourceHash": [],
        "targetHash": [
            691753681
        ],
        "callerClass": "org.springframework.web.context.request.ServletWebRequest",
        "callerMethod": "getHeaderValues",
        "retClassName": "",
        "callerLineNumber": 135
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1321,
        "className": "java.lang.String",
        "signature": "()[B",
        "interfaces": [],
        "methodName": "getBytes",
        "sourceHash": [
            1938662970
        ],
        "targetHash": [
            2081936307
        ],
        "callerClass": "java.lang.ProcessImpl",
        "callerMethod": "toCString",
        "retClassName": "",
        "callerLineNumber": 50
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1320,
        "className": "java.lang.ProcessBuilder",
        "signature": "([Ljava/lang/String;)V",
        "interfaces": [],
        "methodName": "<init>",
        "sourceHash": [
            1938662970,
            618514829
        ],
        "targetHash": [
            2131750578
        ],
        "callerClass": "java.lang.Runtime",
        "callerMethod": "exec",
        "retClassName": "",
        "callerLineNumber": 617
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1319,
        "className": "java.lang.String",
        "signature": "(II)Ljava/lang/String;",
        "interfaces": [],
        "methodName": "substring",
        "sourceHash": [
            1938662970
        ],
        "targetHash": [
            1938662970
        ],
        "callerClass": "java.util.StringTokenizer",
        "callerMethod": "nextToken",
        "retClassName": "",
        "callerLineNumber": 352
    },
    {
        "args": "",
        "source": False,
        "invokeId": 1318,
        "className": "java.lang.Runtime",
        "signature": "(Ljava/lang/String;)Ljava/lang/Process;",
        "interfaces": [],
        "methodName": "exec",
        "sourceHash": [
            1938662970
        ],
        "targetHash": [],
        "callerClass": "org.iast.springsec.common.CmdExec",
        "callerMethod": "runtimeExec",
        "retClassName": "",
        "callerLineNumber": 37
    },
    {
        "args": "",
        "source": True,
        "invokeId": 1317,
        "className": "org/springframework/web/method/support/HandlerMethodArgumentResolverComposite",
        "signature": "(Lorg/springframework/core/MethodParameter;Lorg/springframework/web/method/support/ModelAndViewContainer;Lorg/springframework/web/context/request/NativeWebRequest;Lorg/springframework/web/bind/support/WebDataBinderFactory;)Ljava/lang/Object;",
        "interfaces": [],
        "methodName": "resolveArgument",
        "sourceHash": [],
        "targetHash": [
            1938662970
        ],
        "callerClass": "org.springframework.web.method.support.InvocableHandlerMethod",
        "callerMethod": "getMethodArgumentValues",
        "retClassName": "",
        "callerLineNumber": 167
    }
]
