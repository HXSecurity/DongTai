######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_method_pool
# @created     : 星期一 12月 13, 2021 17:21:33 CST
#
# @description :
######################################################################


from test.apiserver.test_agent_base import AgentTestCase,gzipdata
from dongtai.models.agent import IastAgent
from dongtai.models.agent_method_pool import MethodPool



class AgentMethodPoolTestCase(AgentTestCase):

    def test_agent_method_pool_upload(self):
        method = {
            "detail": {
                "agentId":
                3490,
                "clientIp":
                "172.19.0.3",
                "language":
                "PHP",
                "method":
                "POST",
                "pool": [{
                    "args": "",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 21,
                    "methodName": "$_POST",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".$_POST",
                    "source": True,
                    "sourceHash": "3506402",
                    "sourceValues": "root,",
                    "targetHash": "3506402",
                    "targetValues": "root"
                }, {
                    "args": "",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 22,
                    "methodName": "$_POST",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".$_POST",
                    "source": True,
                    "sourceHash": "2430751009",
                    "sourceValues": "12312334,",
                    "targetHash": "2430751009",
                    "targetValues": "12312334"
                }, {
                    "args": "",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 23,
                    "methodName": "$_POST",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".$_POST",
                    "source": True,
                    "sourceHash": "2487299128",
                    "sourceValues": "Submit,",
                    "targetHash": "2487299128",
                    "targetValues": "Submit"
                }, {
                    "args": "root",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 24,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "3506402",
                    "sourceValues": "root,",
                    "targetHash": "3264164444,3264164444",
                    "targetValues": "User Name:root,User Name:root"
                }, {
                    "args": "User Name:root,\n",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 25,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "3264164444,10",
                    "sourceValues": "User Name:root,\n,",
                    "targetHash": "2404849966,2404849966",
                    "targetValues": "User Name:root\n,User Name:root\n"
                }, {
                    "args": "User Name:root\n",
                    "callerClass": "",
                    "callerLineNumber": 53,
                    "callerMethod": "main",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 26,
                    "methodName": "fwrite",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".fwrite",
                    "source": False,
                    "sourceHash": "2404849966",
                    "sourceValues": "User Name:root\n,",
                    "targetHash": "",
                    "targetValues": ""
                }, {
                    "args": "12312334",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 27,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "2430751009",
                    "sourceValues": "12312334,",
                    "targetHash": "2573646592,2573646592",
                    "targetValues": "Password:12312334,Password:12312334"
                }, {
                    "args":
                    "Password:12312334,\n",
                    "callerClass":
                    "",
                    "callerLineNumber":
                    0,
                    "callerMethod":
                    "",
                    "className":
                    "",
                    "interfaces":
                    "[]",
                    "invokeId":
                    28,
                    "methodName":
                    "",
                    "originClassName":
                    "",
                    "retClassName":
                    "String",
                    "signature":
                    "",
                    "source":
                    False,
                    "sourceHash":
                    "2573646592,10",
                    "sourceValues":
                    "Password:12312334,\n,",
                    "targetHash":
                    "2473633034,2473633034",
                    "targetValues":
                    "Password:12312334\n,Password:12312334\n"
                }, {
                    "args": "Password:12312334\n",
                    "callerClass": "",
                    "callerLineNumber": 54,
                    "callerMethod": "main",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 29,
                    "methodName": "fwrite",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".fwrite",
                    "source": False,
                    "sourceHash": "2473633034",
                    "sourceValues": "Password:12312334\n,",
                    "targetHash": "",
                    "targetValues": ""
                }, {
                    "args": "root",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 30,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "3506402",
                    "sourceValues": "root,",
                    "targetHash": "34906116,34906116",
                    "targetValues": "\"root,\"root"
                }, {
                    "args": "\"root,\"",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 31,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "34906116,34",
                    "sourceValues": "\"root,\",",
                    "targetHash": "1082089630,1082089630",
                    "targetValues": "\"root\",\"root\""
                }, {
                    "args": "12312334",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 32,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "2430751009",
                    "sourceValues": "12312334,",
                    "targetHash": "1106841411,1106841411",
                    "targetValues": "\"12312334,\"12312334"
                }, {
                    "args": "\"12312334,\"",
                    "callerClass": "",
                    "callerLineNumber": 0,
                    "callerMethod": "",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 33,
                    "methodName": "",
                    "originClassName": "",
                    "retClassName": "String",
                    "signature": "",
                    "source": False,
                    "sourceHash": "1106841411,34",
                    "sourceValues": "\"12312334,\",",
                    "targetHash": "4247312703,4247312703",
                    "targetValues": "\"12312334\",\"12312334\""
                }, {
                    "args":
                    "",
                    "callerClass":
                    "",
                    "callerLineNumber":
                    61,
                    "callerMethod":
                    "",
                    "className":
                    "",
                    "interfaces":
                    "[]",
                    "invokeId":
                    34,
                    "methodName":
                    "ZEND_ROPE_END",
                    "originClassName":
                    "",
                    "retClassName":
                    "String",
                    "signature":
                    ".ZEND_ROPE_END",
                    "source":
                    False,
                    "sourceHash":
                    "3935959953,1082089630,1478523430,4247312703,1876301945",
                    "sourceValues":
                    "SELECT username, password FROM users WHERE username=(,\"root\",) and password=(,\"12312334\",) LIMIT 0,1,",
                    "targetHash":
                    "3553945957",
                    "targetValues":
                    "SELECT username, password FROM users WHERE username=(\"root\") and password=(\"12312334\") LIMIT 0,1"
                }, {
                    "args":
                    "SELECT username, password FROM users WHERE username=(\"root\") and password=(\"12312334\") LIMIT 0,1,\"12312334",
                    "callerClass": "",
                    "callerLineNumber": 62,
                    "callerMethod": "main",
                    "className": "",
                    "interfaces": "[]",
                    "invokeId": 35,
                    "methodName": "mysqli_query",
                    "originClassName": "",
                    "retClassName": "",
                    "signature": ".mysqli_query",
                    "source": False,
                    "sourceHash": "3553945957,1106841411",
                    "sourceValues":
                    "SELECT username, password FROM users WHERE username=(\"root\") and password=(\"12312334\") LIMIT 0,1,\"12312334,",
                    "targetHash": "",
                    "targetValues": ""
                }],
                "protocol":
                "HTTP/1.1",
                "replayRequest":
                False,
                "reqBody":
                "",
                "reqHeader":
                "",
                "resBody":
                "",
                "resHeader":
                "",
                "scheme":
                "http",
                "secure":
                False,
                "uri":
                "/Less-12/",
                "url":
                "http://127.0.0.1:8008"
            },
            "type": 36
        }
        method['detail']['agentId'] = self.agent_id
        data = gzipdata(method)
        response = self.client.post('http://testserver/api/v1/report/upload',
                                    data=data,
                                    HTTP_CONTENT_ENCODING='gzip',
                                    content_type='application/json',
                                    )
        assert response.status_code == 200
        res = MethodPool.objects.filter(agent_id=self.agent_id).all()
        assert len(res) == 1
