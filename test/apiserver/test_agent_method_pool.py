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
import gzip
import base64

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

    def test_agent_method_pool_from_go_agent(self):
        data = {
            "type": 36,
            "detail": {
                "agentId":
                4025,
                "disk":
                "",
                "memory":
                "",
                "cpu":
                "",
                "methodQueue":
                0,
                "replayQueue":
                0,
                "reqCount":
                0,
                "reportQueue":
                0,
                "packagePath":
                "",
                "packageSignature":
                "",
                "packageName":
                "",
                "packageAlgorithm":
                "",
                "uri":
                "/sqli1",
                "url":
                "http://localhost:9999/sqli123132123313132321123231",
                "protocol":
                "HTTP/1.1",
                "contextPath":
                "",
                "pool": [{
                    "invokeId":
                    40252101640145388,
                    "interfaces": [],
                    "targetHash":
                    ["824634910755", "824634910761", "0", "0", "0", "0"],
                    "targetValues":
                    "Level low     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8420f8, 0x5})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "Level ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    49,
                    "callerClass":
                    "github.com/govwa/util",
                    "args":
                    "[\"Level\"]",
                    "callerMethod":
                    "GetCookie(0xc00014e100, {0x8420f8, 0x5})\n",
                    "sourceHash": ["8659192"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId":
                    40252101640145389,
                    "interfaces": [],
                    "targetHash": [
                        "824634288360", "824634288368", "824634288378",
                        "824634288384", "824634288396", "824634288400",
                        "824634288416", "0"
                    ],
                    "targetValues":
                    "root Aa@6447985 govwa localhost 3306 http://localhost 9999  ",
                    "signature":
                    "go-agent/core/jsonUnmarshal.Unmarshal({0xc000324200, 0xd9, 0x200}, {0x79e520, 0xc0001da580})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    True,
                    "callerLineNumber":
                    29,
                    "callerClass":
                    "github.com/govwa/util/config",
                    "args":
                    "[\"ewogICAgInVzZXIiOiAicm9vdCIsCiAgICAicGFzc3dvcmQiOiAiQWFANjQ0Nzk4NSIsCiAgICAiZGJuYW1lIjogImdvdndhIiwKICAgICJzcWxob3N0IjogImxvY2FsaG9zdCIsCiAgICAic3FscG9ydCI6ICIzMzA2IiwKICAgICJ3ZWJzZXJ2ZXIiOiAiaHR0cDovL2xvY2FsaG9zdCIsCiAgICAid2VicG9ydCI6ICI5OTk5IiwKCiAgICAic2Vzc2lvbmtleToiOiAiRzBWdzQ0NCIKfQ==\"]",
                    "callerMethod":
                    "LoadConfig()\n",
                    "sourceHash":
                    None,
                    "retClassName":
                    "*config.Config "
                }, {
                    "invokeId":
                    40252101640145390,
                    "interfaces": [],
                    "targetHash": ["824636572896"],
                    "targetValues":
                    "root:Aa@6447985@tcp(localhost:3306)/ ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x84afe4, 0x11}, {0xc00032c4b8, 0x4, 0x4})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "%s:%s@tcp(%s:%s)/ root Aa@6447985 localhost 3306 ",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    False,
                    "callerLineNumber":
                    18,
                    "callerClass":
                    "github.com/govwa/util/database",
                    "args":
                    "[\"%s:%s@tcp(%s:%s)/\",[\"root\",\"Aa@6447985\",\"localhost\",\"3306\"]]",
                    "callerMethod":
                    "Connect()\n",
                    "sourceHash": [
                        "8695780", "824634288360", "824634288368",
                        "824634288384", "824634288396"
                    ],
                    "retClassName":
                    "string "
                }, {
                    "invokeId":
                    40252101640145391,
                    "interfaces": [],
                    "targetHash": ["824636573472"],
                    "targetValues":
                    "root:Aa@6447985@tcp(localhost:3306)/govwa ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x84c9df, 0x13}, {0xc00032c4f8, 0x5, 0x5})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "%s:%s@tcp(%s:%s)/%s root Aa@6447985 localhost 3306 govwa ",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    False,
                    "callerLineNumber":
                    30,
                    "callerClass":
                    "github.com/govwa/util/database",
                    "args":
                    "[\"%s:%s@tcp(%s:%s)/%s\",[\"root\",\"Aa@6447985\",\"localhost\",\"3306\",\"govwa\"]]",
                    "callerMethod":
                    "Connect()\n",
                    "sourceHash": [
                        "8702431", "824634288360", "824634288368",
                        "824634288384", "824634288396", "824634288378"
                    ],
                    "retClassName":
                    "string "
                }, {
                    "invokeId":
                    40252101640145390,
                    "interfaces": [],
                    "targetHash":
                    ["824634910484", "824634910490", "0", "0", "0", "0"],
                    "targetValues":
                    "govwa MTY0MDE0NDg3NHxEdi1CQkFFQ180SUFBUkFCRUFBQVh2LUNBQU1HYzNSeWFXNW5EQThBRFdkdmRuZGhYM05sYzNOcGIyNEVZbTl2YkFJQ0FBRUdjM1J5YVc1bkRBY0FCWFZ1WVcxbEJuTjBjbWx1Wnd3SEFBVmhaRzFwYmdaemRISnBibWNNQkFBQ2FXUUdjM1J5YVc1bkRBTUFBVEU9fPfvm5eU0A5drQKDLDOgC_ffWcZue0sMf7EbJ7H5XzIj     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8424b8, 0x5})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "govwa ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    91,
                    "callerClass":
                    "github.com/gorilla/sessions.(*CookieStore)",
                    "args":
                    "[\"govwa\"]",
                    "callerMethod":
                    "New(0xc0000b6ce0, 0xc00014e100, {0x8424b8, 0x5})\n",
                    "sourceHash": ["8660152"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId":
                    40252101640145391,
                    "interfaces": [],
                    "targetHash":
                    ["824634910748", "824634910752", "0", "0", "0", "0"],
                    "targetValues":
                    "Uid 1     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8413f6, 0x3})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "Uid ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    49,
                    "callerClass":
                    "github.com/govwa/util",
                    "args":
                    "[\"Uid\"]",
                    "callerMethod":
                    "GetCookie(0xc00014e100, {0x8413f6, 0x3})\n",
                    "sourceHash": ["8655862"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId": 40252101640145392,
                    "interfaces": [],
                    "targetHash": ["824635081280"],
                    "targetValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=1 ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x86883b, 0x90}, {0xc00032c6c0, 0x1, 0x1})\n",
                    "originClassName": "fmt",
                    "sourceValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=%s 1 ",
                    "methodName": "Sprintf",
                    "className": "fmt",
                    "source": False,
                    "callerLineNumber": 38,
                    "callerClass":
                    "github.com/govwa/vulnerability/sqli.(*Profile)",
                    "args":
                    "[\"SELECT p.user_id, p.full_name, p.city, p.phone_number \\n\\t\\t\\t\\t\\t\\t\\t\\tFROM Profile as p,Users as u \\n\\t\\t\\t\\t\\t\\t\\t\\twhere p.user_id = u.id \\n\\t\\t\\t\\t\\t\\t\\t\\tand u.id=%s\",[\"1\"]]",
                    "callerMethod":
                    "UnsafeQueryGetData(0xc0002925c0, {0xc000122820, 0x1})\n",
                    "sourceHash": ["8816699", "824634910752"],
                    "retClassName": "string "
                }, {
                    "invokeId": 40252101640145393,
                    "interfaces": [],
                    "targetHash": None,
                    "targetValues": "",
                    "signature":
                    "go-agent/core/sqlDBQuery.Query(0xc0001c0a90, {0xc00014c240, 0x8f}, {0x0, 0x0, 0x0})\n",
                    "originClassName": "sql.(*DB)",
                    "sourceValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=1 ",
                    "methodName": "Query",
                    "className": "sql.(*DB)",
                    "source": False,
                    "callerLineNumber": 42,
                    "callerClass":
                    "github.com/govwa/vulnerability/sqli.(*Profile)",
                    "args":
                    "[\"SELECT p.user_id, p.full_name, p.city, p.phone_number \\n\\t\\t\\t\\t\\t\\t\\t\\tFROM Profile as p,Users as u \\n\\t\\t\\t\\t\\t\\t\\t\\twhere p.user_id = u.id \\n\\t\\t\\t\\t\\t\\t\\t\\tand u.id=1\",None]",
                    "callerMethod":
                    "UnsafeQueryGetData(0xc0002925c0, {0xc000122820, 0x1})\n",
                    "sourceHash": ["824635081280"],
                    "retClassName": "*sql.Rows *errors.errorString "
                }],
                "language":
                "GO",
                "clientIp":
                "[::1]:53457",
                "secure":
                False,
                "queryString":
                "",
                "replayRequest":
                False,
                "method":
                "GET",
                "reqHeader":
                "eyJBY2NlcHQiOlsidGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOSJdLCJBY2NlcHQtRW5jb2RpbmciOlsiZ3ppcCwgZGVmbGF0ZSwgYnIiXSwiQWNjZXB0LUxhbmd1YWdlIjpbInpoLUNOLHpoO3E9MC45LGVuLUdCO3E9MC44LGVuO3E9MC43LGVuLVVTO3E9MC42Il0sIkNvbm5lY3Rpb24iOlsia2VlcC1hbGl2ZSJdLCJDb29raWUiOlsiSG1fbHZ0XzY5YmUxNTIzNTFlNDc5YjhiNjRmNzdhOTM0NzAzYTU1PTE2Mzk3MjcwNjA7IGdvdndhPU1UWTBNREUwTkRnM05IeEVkaTFDUWtGRlExODBTVUZCVWtGQ1JVRkJRVmgyTFVOQlFVMUhZek5TZVdGWE5XNUVRVGhCUkZka2RtUnVaR2hZTTA1c1l6Tk9jR0l5TkVWWmJUbDJZa0ZKUTBGQlJVZGpNMUo1WVZjMWJrUkJZMEZDV0ZaMVdWY3hiRUp1VGpCamJXeDFXbmQzU0VGQlZtaGFSekZ3WW1kYWVtUklTbkJpYldOTlFrRkJRMkZYVVVkak0xSjVZVmMxYmtSQlRVRkJWRVU5ZlBmdm01ZVUwQTVkclFLRExET2dDX2ZmV2NadWUwc01mN0ViSjdINVh6SWo7IFVpZD0xOyBMZXZlbD1sb3ciXSwiUmVmZXJlciI6WyJodHRwOi8vbG9jYWxob3N0Ojk5OTkvc3FsaTEiXSwiU2VjLUNoLVVhIjpbIlwiIE5vdCBBO0JyYW5kXCI7dj1cIjk5XCIsIFwiQ2hyb21pdW1cIjt2PVwiOTZcIiwgXCJNaWNyb3NvZnQgRWRnZVwiO3Y9XCI5NlwiIl0sIlNlYy1DaC1VYS1Nb2JpbGUiOlsiPzAiXSwiU2VjLUNoLVVhLVBsYXRmb3JtIjpbIlwiV2luZG93c1wiIl0sIlNlYy1GZXRjaC1EZXN0IjpbImRvY3VtZW50Il0sIlNlYy1GZXRjaC1Nb2RlIjpbIm5hdmlnYXRlIl0sIlNlYy1GZXRjaC1TaXRlIjpbInNhbWUtb3JpZ2luIl0sIlNlYy1GZXRjaC1Vc2VyIjpbIj8xIl0sIlVwZ3JhZGUtSW5zZWN1cmUtUmVxdWVzdHMiOlsiMSJdLCJVc2VyLUFnZW50IjpbIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85Ni4wLjQ2NjQuMTEwIFNhZmFyaS81MzcuMzYgRWRnLzk2LjAuMTA1NC42MiJdfQ==",
                "reqBody":
                "",
                "resBody":
                "               \u003cp\u003eYour Profile :\u003c/p\u003e\n                    sql: converting argument $1 type: unsupported type []interface {}, a slice of interface \n\u003cpre\u003e\nUid     : 1\nName    : \nCity    :  \nNumber  :  \n\u003c/pre\u003e\n                \u003cdiv class=\"more-info\"\u003e\n                    \u003cspan\u003eMore Info :\u003c/span\u003e\n                    \u003ca target=\"_blank\" href=\"http://www.sqlinjection.net/union/\"\u003ehttp://www.sqlinjection.net/union/\u003c/a\u003e\n                    \u003ca target=\"_blank\" href=\"https://www.owasp.org/index.php/SQL_Injection\"\u003ehttps://www.owasp.org/index.php/SQL_Injection\u003c/a\u003e\n                \u003c/div\u003e\n            \u003c/div\u003e\n        \u003c/div\u003e\n    \u003c/div\u003e\n\u003c/div\u003e\n\n\u003c/div\u003e\n\n\n    \u003cfooter class=\"footer\"\u003e\n        \u003cdiv class=\"container\"\u003e\n          \u003cspan\u003e\u003ci class=\"fa fa-copyright\"\u003e\u003c/i\u003eNemosecurity\u003c/span\u003e\n        \u003c/div\u003e\n      \u003c/footer\u003e\n\u003c/div\u003e\n\n\u003c/body\u003e\n\n\u003c/html\u003e\n           \u003cli\u003e\u003ca href=\"idor1\"\u003eIDOR 1\u003c/a\u003e\u003c/li\u003e\n                            \u003cli\u003e\u003ca href=\"idor2\"\u003eIDOR 2\u003c/a\u003e\u003c/li\u003e\n                        \u003c/ul\u003e\n\n                   \n                    \u003cli\u003e\n                            \u003ca href=\"csa\"\u003e\n                                \u003ci class=\"fa fa-bug fa-lg\"\u003e\u003c/i\u003e Client Side Auth\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                    \u003cli style=\"height:35px\"\u003e\n                    \u003c/li\u003e\n                    \u003cli\u003e\n                            \u003ca href=\"setting\"\u003e\n                                \u003ci class=\"glyphicon glyphicon-cog fa-lg\"\u003e\u003c/i\u003e Setting\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                    \u003cli\u003e\n                            \u003ca href=\"logout\"\u003e\n                                \u003ci class=\"fa fa-sign-out fa-lg\"\u003e\u003c/i\u003e Logout\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                        \n                \u003c/ul\u003e\n            \u003c/div\u003e\n        \u003c/div\u003e\n    \u003c/div\u003e\n    \n\u003cdiv class=\"col-md-9\"\u003e\n    \u003cdiv class=\"panel panel-primary\"\u003e\n        \u003cdiv class=\"panel-heading\"\u003eSQL Injection Vulnerability\u003c/div\u003e\n        \u003cdiv class=\"panel-body\"\u003e\n            \u003cdiv class=\"pnl\"\u003e\n                \n                \u003cp\u003eThis should be safe\u003c/p\u003e\n ",
                "scheme":
                "",
                "resHeader":
                "e30=",
                "invokeId":
                0,
                "interfaces":
                None,
                "targetHash":
                None,
                "targetValues":
                "",
                "signature":
                "",
                "originClassName":
                "",
                "sourceValues":
                "",
                "methodName":
                "",
                "className":
                "",
                "source":
                False,
                "callerLineNumber":
                0,
                "callerClass":
                "",
                "args":
                "",
                "callerMethod":
                "",
                "sourceHash":
                None,
                "retClassName":
                "",
                "log":
                "",
                "apiData":
                None
            },
            "invoke_id": 40252101640145387
        }
        data['detail']['agentId'] = self.agent_id
        data = gzipdata(data)
        response = self.client.post('http://testserver/api/v1/report/upload',
                                    data=data,
                                    HTTP_CONTENT_ENCODING='gzip',
                                    content_type='application/json',
                                    )
        assert response.status_code == 200
        assert MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231",
            agent_id=self.agent_id).exists()
    def test_agent_method_pool_gzip_test(self):
        data = {
            "type": 36,
            "detail": {
                "agentId":
                4025,
                "disk":
                "",
                "memory":
                "",
                "cpu":
                "",
                "methodQueue":
                0,
                "replayQueue":
                0,
                "reqCount":
                0,
                "reportQueue":
                0,
                "packagePath":
                "",
                "packageSignature":
                "",
                "packageName":
                "",
                "packageAlgorithm":
                "",
                "uri":
                "/sqli1",
                "url":
                "http://localhost:9999/sqli123132123313132321123231test",
                "protocol":
                "HTTP/1.1",
                "contextPath":
                "",
                "pool": [{
                    "invokeId":
                    40252101640145388,
                    "interfaces": [],
                    "targetHash":
                    ["824634910755", "824634910761", "0", "0", "0", "0"],
                    "targetValues":
                    "Level low     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8420f8, 0x5})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "Level ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    49,
                    "callerClass":
                    "github.com/govwa/util",
                    "args":
                    "[\"Level\"]",
                    "callerMethod":
                    "GetCookie(0xc00014e100, {0x8420f8, 0x5})\n",
                    "sourceHash": ["8659192"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId":
                    40252101640145389,
                    "interfaces": [],
                    "targetHash": [
                        "824634288360", "824634288368", "824634288378",
                        "824634288384", "824634288396", "824634288400",
                        "824634288416", "0"
                    ],
                    "targetValues":
                    "root Aa@6447985 govwa localhost 3306 http://localhost 9999  ",
                    "signature":
                    "go-agent/core/jsonUnmarshal.Unmarshal({0xc000324200, 0xd9, 0x200}, {0x79e520, 0xc0001da580})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    True,
                    "callerLineNumber":
                    29,
                    "callerClass":
                    "github.com/govwa/util/config",
                    "args":
                    "[\"ewogICAgInVzZXIiOiAicm9vdCIsCiAgICAicGFzc3dvcmQiOiAiQWFANjQ0Nzk4NSIsCiAgICAiZGJuYW1lIjogImdvdndhIiwKICAgICJzcWxob3N0IjogImxvY2FsaG9zdCIsCiAgICAic3FscG9ydCI6ICIzMzA2IiwKICAgICJ3ZWJzZXJ2ZXIiOiAiaHR0cDovL2xvY2FsaG9zdCIsCiAgICAid2VicG9ydCI6ICI5OTk5IiwKCiAgICAic2Vzc2lvbmtleToiOiAiRzBWdzQ0NCIKfQ==\"]",
                    "callerMethod":
                    "LoadConfig()\n",
                    "sourceHash":
                    None,
                    "retClassName":
                    "*config.Config "
                }, {
                    "invokeId":
                    40252101640145390,
                    "interfaces": [],
                    "targetHash": ["824636572896"],
                    "targetValues":
                    "root:Aa@6447985@tcp(localhost:3306)/ ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x84afe4, 0x11}, {0xc00032c4b8, 0x4, 0x4})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "%s:%s@tcp(%s:%s)/ root Aa@6447985 localhost 3306 ",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    False,
                    "callerLineNumber":
                    18,
                    "callerClass":
                    "github.com/govwa/util/database",
                    "args":
                    "[\"%s:%s@tcp(%s:%s)/\",[\"root\",\"Aa@6447985\",\"localhost\",\"3306\"]]",
                    "callerMethod":
                    "Connect()\n",
                    "sourceHash": [
                        "8695780", "824634288360", "824634288368",
                        "824634288384", "824634288396"
                    ],
                    "retClassName":
                    "string "
                }, {
                    "invokeId":
                    40252101640145391,
                    "interfaces": [],
                    "targetHash": ["824636573472"],
                    "targetValues":
                    "root:Aa@6447985@tcp(localhost:3306)/govwa ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x84c9df, 0x13}, {0xc00032c4f8, 0x5, 0x5})\n",
                    "originClassName":
                    "fmt",
                    "sourceValues":
                    "%s:%s@tcp(%s:%s)/%s root Aa@6447985 localhost 3306 govwa ",
                    "methodName":
                    "Sprintf",
                    "className":
                    "fmt",
                    "source":
                    False,
                    "callerLineNumber":
                    30,
                    "callerClass":
                    "github.com/govwa/util/database",
                    "args":
                    "[\"%s:%s@tcp(%s:%s)/%s\",[\"root\",\"Aa@6447985\",\"localhost\",\"3306\",\"govwa\"]]",
                    "callerMethod":
                    "Connect()\n",
                    "sourceHash": [
                        "8702431", "824634288360", "824634288368",
                        "824634288384", "824634288396", "824634288378"
                    ],
                    "retClassName":
                    "string "
                }, {
                    "invokeId":
                    40252101640145390,
                    "interfaces": [],
                    "targetHash":
                    ["824634910484", "824634910490", "0", "0", "0", "0"],
                    "targetValues":
                    "govwa MTY0MDE0NDg3NHxEdi1CQkFFQ180SUFBUkFCRUFBQVh2LUNBQU1HYzNSeWFXNW5EQThBRFdkdmRuZGhYM05sYzNOcGIyNEVZbTl2YkFJQ0FBRUdjM1J5YVc1bkRBY0FCWFZ1WVcxbEJuTjBjbWx1Wnd3SEFBVmhaRzFwYmdaemRISnBibWNNQkFBQ2FXUUdjM1J5YVc1bkRBTUFBVEU9fPfvm5eU0A5drQKDLDOgC_ffWcZue0sMf7EbJ7H5XzIj     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8424b8, 0x5})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "govwa ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    91,
                    "callerClass":
                    "github.com/gorilla/sessions.(*CookieStore)",
                    "args":
                    "[\"govwa\"]",
                    "callerMethod":
                    "New(0xc0000b6ce0, 0xc00014e100, {0x8424b8, 0x5})\n",
                    "sourceHash": ["8660152"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId":
                    40252101640145391,
                    "interfaces": [],
                    "targetHash":
                    ["824634910748", "824634910752", "0", "0", "0", "0"],
                    "targetValues":
                    "Uid 1     ",
                    "signature":
                    "go-agent/core/httpRequestCookie.Cookie(0xc00014e100, {0x8413f6, 0x3})\n",
                    "originClassName":
                    "http.(*Request)",
                    "sourceValues":
                    "Uid ",
                    "methodName":
                    "Cookie",
                    "className":
                    "http.(*Request)",
                    "source":
                    True,
                    "callerLineNumber":
                    49,
                    "callerClass":
                    "github.com/govwa/util",
                    "args":
                    "[\"Uid\"]",
                    "callerMethod":
                    "GetCookie(0xc00014e100, {0x8413f6, 0x3})\n",
                    "sourceHash": ["8655862"],
                    "retClassName":
                    "*http.Cookie "
                }, {
                    "invokeId": 40252101640145392,
                    "interfaces": [],
                    "targetHash": ["824635081280"],
                    "targetValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=1 ",
                    "signature":
                    "go-agent/core/fmtSprintf.Sprintf({0x86883b, 0x90}, {0xc00032c6c0, 0x1, 0x1})\n",
                    "originClassName": "fmt",
                    "sourceValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=%s 1 ",
                    "methodName": "Sprintf",
                    "className": "fmt",
                    "source": False,
                    "callerLineNumber": 38,
                    "callerClass":
                    "github.com/govwa/vulnerability/sqli.(*Profile)",
                    "args":
                    "[\"SELECT p.user_id, p.full_name, p.city, p.phone_number \\n\\t\\t\\t\\t\\t\\t\\t\\tFROM Profile as p,Users as u \\n\\t\\t\\t\\t\\t\\t\\t\\twhere p.user_id = u.id \\n\\t\\t\\t\\t\\t\\t\\t\\tand u.id=%s\",[\"1\"]]",
                    "callerMethod":
                    "UnsafeQueryGetData(0xc0002925c0, {0xc000122820, 0x1})\n",
                    "sourceHash": ["8816699", "824634910752"],
                    "retClassName": "string "
                }, {
                    "invokeId": 40252101640145393,
                    "interfaces": [],
                    "targetHash": None,
                    "targetValues": "",
                    "signature":
                    "go-agent/core/sqlDBQuery.Query(0xc0001c0a90, {0xc00014c240, 0x8f}, {0x0, 0x0, 0x0})\n",
                    "originClassName": "sql.(*DB)",
                    "sourceValues":
                    "SELECT p.user_id, p.full_name, p.city, p.phone_number \n\t\t\t\t\t\t\t\tFROM Profile as p,Users as u \n\t\t\t\t\t\t\t\twhere p.user_id = u.id \n\t\t\t\t\t\t\t\tand u.id=1 ",
                    "methodName": "Query",
                    "className": "sql.(*DB)",
                    "source": False,
                    "callerLineNumber": 42,
                    "callerClass":
                    "github.com/govwa/vulnerability/sqli.(*Profile)",
                    "args":
                    "[\"SELECT p.user_id, p.full_name, p.city, p.phone_number \\n\\t\\t\\t\\t\\t\\t\\t\\tFROM Profile as p,Users as u \\n\\t\\t\\t\\t\\t\\t\\t\\twhere p.user_id = u.id \\n\\t\\t\\t\\t\\t\\t\\t\\tand u.id=1\",None]",
                    "callerMethod":
                    "UnsafeQueryGetData(0xc0002925c0, {0xc000122820, 0x1})\n",
                    "sourceHash": ["824635081280"],
                    "retClassName": "*sql.Rows *errors.errorString "
                }],
                "language":
                "GO",
                "clientIp":
                "[::1]:53457",
                "secure":
                False,
                "queryString":
                "",
                "replayRequest":
                False,
                "method":
                "GET",
                "reqHeader":
                "eyJBY2NlcHQiOlsidGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2Uvd2VicCxpbWFnZS9hcG5nLCovKjtxPTAuOCxhcHBsaWNhdGlvbi9zaWduZWQtZXhjaGFuZ2U7dj1iMztxPTAuOSJdLCJBY2NlcHQtRW5jb2RpbmciOlsiZ3ppcCwgZGVmbGF0ZSwgYnIiXSwiQWNjZXB0LUxhbmd1YWdlIjpbInpoLUNOLHpoO3E9MC45LGVuLUdCO3E9MC44LGVuO3E9MC43LGVuLVVTO3E9MC42Il0sIkNvbm5lY3Rpb24iOlsia2VlcC1hbGl2ZSJdLCJDb29raWUiOlsiSG1fbHZ0XzY5YmUxNTIzNTFlNDc5YjhiNjRmNzdhOTM0NzAzYTU1PTE2Mzk3MjcwNjA7IGdvdndhPU1UWTBNREUwTkRnM05IeEVkaTFDUWtGRlExODBTVUZCVWtGQ1JVRkJRVmgyTFVOQlFVMUhZek5TZVdGWE5XNUVRVGhCUkZka2RtUnVaR2hZTTA1c1l6Tk9jR0l5TkVWWmJUbDJZa0ZKUTBGQlJVZGpNMUo1WVZjMWJrUkJZMEZDV0ZaMVdWY3hiRUp1VGpCamJXeDFXbmQzU0VGQlZtaGFSekZ3WW1kYWVtUklTbkJpYldOTlFrRkJRMkZYVVVkak0xSjVZVmMxYmtSQlRVRkJWRVU5ZlBmdm01ZVUwQTVkclFLRExET2dDX2ZmV2NadWUwc01mN0ViSjdINVh6SWo7IFVpZD0xOyBMZXZlbD1sb3ciXSwiUmVmZXJlciI6WyJodHRwOi8vbG9jYWxob3N0Ojk5OTkvc3FsaTEiXSwiU2VjLUNoLVVhIjpbIlwiIE5vdCBBO0JyYW5kXCI7dj1cIjk5XCIsIFwiQ2hyb21pdW1cIjt2PVwiOTZcIiwgXCJNaWNyb3NvZnQgRWRnZVwiO3Y9XCI5NlwiIl0sIlNlYy1DaC1VYS1Nb2JpbGUiOlsiPzAiXSwiU2VjLUNoLVVhLVBsYXRmb3JtIjpbIlwiV2luZG93c1wiIl0sIlNlYy1GZXRjaC1EZXN0IjpbImRvY3VtZW50Il0sIlNlYy1GZXRjaC1Nb2RlIjpbIm5hdmlnYXRlIl0sIlNlYy1GZXRjaC1TaXRlIjpbInNhbWUtb3JpZ2luIl0sIlNlYy1GZXRjaC1Vc2VyIjpbIj8xIl0sIlVwZ3JhZGUtSW5zZWN1cmUtUmVxdWVzdHMiOlsiMSJdLCJVc2VyLUFnZW50IjpbIk1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS85Ni4wLjQ2NjQuMTEwIFNhZmFyaS81MzcuMzYgRWRnLzk2LjAuMTA1NC42MiJdfQ==",
                "reqBody":
                "",
                "resBody":
                "               \u003cp\u003eYour Profile :\u003c/p\u003e\n                    sql: converting argument $1 type: unsupported type []interface {}, a slice of interface \n\u003cpre\u003e\nUid     : 1\nName    : \nCity    :  \nNumber  :  \n\u003c/pre\u003e\n                \u003cdiv class=\"more-info\"\u003e\n                    \u003cspan\u003eMore Info :\u003c/span\u003e\n                    \u003ca target=\"_blank\" href=\"http://www.sqlinjection.net/union/\"\u003ehttp://www.sqlinjection.net/union/\u003c/a\u003e\n                    \u003ca target=\"_blank\" href=\"https://www.owasp.org/index.php/SQL_Injection\"\u003ehttps://www.owasp.org/index.php/SQL_Injection\u003c/a\u003e\n                \u003c/div\u003e\n            \u003c/div\u003e\n        \u003c/div\u003e\n    \u003c/div\u003e\n\u003c/div\u003e\n\n\u003c/div\u003e\n\n\n    \u003cfooter class=\"footer\"\u003e\n        \u003cdiv class=\"container\"\u003e\n          \u003cspan\u003e\u003ci class=\"fa fa-copyright\"\u003e\u003c/i\u003eNemosecurity\u003c/span\u003e\n        \u003c/div\u003e\n      \u003c/footer\u003e\n\u003c/div\u003e\n\n\u003c/body\u003e\n\n\u003c/html\u003e\n           \u003cli\u003e\u003ca href=\"idor1\"\u003eIDOR 1\u003c/a\u003e\u003c/li\u003e\n                            \u003cli\u003e\u003ca href=\"idor2\"\u003eIDOR 2\u003c/a\u003e\u003c/li\u003e\n                        \u003c/ul\u003e\n\n                   \n                    \u003cli\u003e\n                            \u003ca href=\"csa\"\u003e\n                                \u003ci class=\"fa fa-bug fa-lg\"\u003e\u003c/i\u003e Client Side Auth\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                    \u003cli style=\"height:35px\"\u003e\n                    \u003c/li\u003e\n                    \u003cli\u003e\n                            \u003ca href=\"setting\"\u003e\n                                \u003ci class=\"glyphicon glyphicon-cog fa-lg\"\u003e\u003c/i\u003e Setting\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                    \u003cli\u003e\n                            \u003ca href=\"logout\"\u003e\n                                \u003ci class=\"fa fa-sign-out fa-lg\"\u003e\u003c/i\u003e Logout\n                            \u003c/a\u003e\n                        \u003c/li\u003e\n                        \n                \u003c/ul\u003e\n            \u003c/div\u003e\n        \u003c/div\u003e\n    \u003c/div\u003e\n    \n\u003cdiv class=\"col-md-9\"\u003e\n    \u003cdiv class=\"panel panel-primary\"\u003e\n        \u003cdiv class=\"panel-heading\"\u003eSQL Injection Vulnerability\u003c/div\u003e\n        \u003cdiv class=\"panel-body\"\u003e\n            \u003cdiv class=\"pnl\"\u003e\n                \n                \u003cp\u003eThis should be safe\u003c/p\u003e\n ",
                "scheme":
                "",
                "resHeader":
                "e30=",
                "invokeId":
                0,
                "interfaces":
                None,
                "targetHash":
                None,
                "targetValues":
                "",
                "signature":
                "",
                "originClassName":
                "",
                "sourceValues":
                "",
                "methodName":
                "",
                "className":
                "",
                "source":
                False,
                "callerLineNumber":
                0,
                "callerClass":
                "",
                "args":
                "",
                "callerMethod":
                "",
                "sourceHash":
                None,
                "retClassName":
                "",
                "log":
                "",
                "apiData":
                None
            },
            "invoke_id": 40252101640145387
        }
        data['detail']['agentId'] = self.agent_id
        testdata = '11231231321331232131231312233hwqeqqwe'
        data['detail'][
            'resHeader'] = "Q29udGVudC1UeXBlOmFwcGxpY2F0aW9uL2pzb24KWC1GcmFtZS1PcHRpb25zOkRFTlkKQ29udGVudC1MZW5ndGg6NjYKQ29udGVudC1lbmNvZGluZzpnemlwClgtQ29udGVudC1UeXBlLU9wdGlvbnM6bm9zbmlmZgpSZWZlcnJlci1Qb2xpY3k6c2FtZS1vcmlnaW4="
        data['version'] = 'v2'
        data['detail']['resBody'] = gzip_test_data = base64.b64encode(
            gzip.compress(bytes(
                testdata, encoding='utf-8'))).decode('raw_unicode_escape')
        data = gzipdata(data)
        response = self.client.post(
            'http://testserver/api/v1/report/upload',
            data=data,
            HTTP_CONTENT_ENCODING='gzip',
            content_type='application/json',
        )
        assert response.status_code == 200
        assert MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231test",
            agent_id=self.agent_id).exists()
        assert not MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231test",
            agent_id=self.agent_id,
            res_body=gzip_test_data).exists()

        assert MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231test",
            agent_id=self.agent_id,
            res_body=testdata).exists()

    def test_agent_method_pool_achoc(self):
        data = {
            'detail': {
                'language':
                'PYTHON',
                'replayRequest':
                False,
                'agentId':
                self.agent_id,
                'uri':
                '/demo/request_ssrf',
                'url':
                'http://127.0.0.1:8004/demo/request_ssrf?_r=1711908589&url=https://www.huoxian.cn/?testinopenapi',
                'queryString':
                '_r=1711908589&url=https://www.huoxian.cn/',
                'protocol':
                'HTTP/1.0',
                'contextPath':
                '/demo/request_ssrf',
                'clientIp':
                '127.0.0.1',
                'method':
                'GET',
                'reqHeader':
                'Q29udGVudC1UeXBlOiANCkNvbnRlbnQtTGVuZ3RoOiANCkhvc3Q6IDEyNy4wLjAuMTo4MDA0DQpDb25uZWN0aW9uOiBjbG9zZQ0KVXNlci1BZ2VudDogY3VybC83LjY4LjANCkFjY2VwdDogKi8q',
                'reqBody':
                '',
                'scheme':
                'http',
                'resHeader':
                'SFRUUC8xLjAgMjAwIE9LDQpDb250ZW50LVR5cGU6IGFwcGxpY2F0aW9uL2pzb24NClZhcnk6IEFjY2VwdCwgQ29va2llDQpBbGxvdzogR0VULCBPUFRJT05TDQpYLUZyYW1lLU9wdGlvbnM6IERFTlkNCkNvbnRlbnQtTGVuZ3RoOiAzMTY3Nw0KWC1Db250ZW50LVR5cGUtT3B0aW9uczogbm9zbmlmZg0KUmVmZXJyZXItUG9saWN5OiBzYW1lLW9yaWdpbg0KYWdlbnRJZDogNTk0MQ==',
                'resBody':
                'eyJkYXRhIjogWyI8IWRvY3R5cGUgaHRtbD5cbjxodG1sIGRhdGEtbi1oZWFkLXNzciBsYW5nPVwiZW5cIiBkYXRhLW4taGVhZD1cIiU3QiUyMmxhbmclMjI6JTdCJTIyc3NyJTIyOiUyMmVuJTIyJTdEJTdEXCI+XG4gIDxoZWFkID5cbiAgICA8dGl0bGU+XHU3MDZiXHU3ZWJmXHU1Yjg5XHU1MTY4XHU1ZTczXHU1M2YwPC90aXRsZT48bWV0YSBkYXRhLW4taGVhZD1cInNzclwiIGNoYXJzZXQ9XCJ1dGYtOFwiPjxtZXRhIGRhdGEtbi1oZWFkPVwic3NyXCIgbmFtZT1cInZpZXdwb3J0XCIgY29udGVudD1cIndpZHRoPWRldmljZS13aWR0aFwiPjxtZXRhIGRhdGEtbi1oZWFkPVwic3NyXCIgbmFtZT1cInZpZXdwb3J0XCIgY29udGVudD1cIndpZHRoPWRldmljZS13aWR0aCwgaW5pdGlhbC1zY2FsZT0xLjAsIG1pbmltdW0tc2NhbGU9MS4wLCBtYXhpbXVtLXNjYWxlPTEuMCx1c2VyLXNjYWxhYmxlPW5vXCI+PG1ldGEgZGF0YS1uLWhlYWQ9XCJzc3JcIiBuYW1lPVwia2V5d29yZHNcIiBjb250ZW50PVwiXHU3NjdkXHU1ZTNkXHU1YjUwXHU1ZjAwXHU1M2QxXHU4MDA1LFx1NWYwMFx1NTNkMVx1ODAwNVx1NzkzZVx1NTMzYSxcdTcwNmJcdTdlYmYsXHU3MDZiXHU3ZWJmXHU1Yjg5XHU1MTY4LFx1NzA2Ylx1N2ViZlx1NWU3M1x1NTNmMCxcdTcwNmJcdTdlYmZcdTViODlcdTUxNjhcdTVlNzNcdTUzZjAsXHU2ZTE3XHU5MDBmXHU2ZDRiXHU4YmQ1LFx1NWI4OVx1NTE2OFx1NmQ0Ylx1OGJkNSxcdTViODlcdTUxNjhcdTRmMTdcdTZkNGIsXHU0ZjE3XHU2ZDRiLFx1NWI4OVx1NTE2OFx1NjcwZFx1NTJhMSxcdTRlNGNcdTRlOTEsXHU3NjdkXHU1ZTNkXHU1YjUwXCI+PG1ldGEgZGF0YS1uLWhlYWQ9XCJzc3JcIiBkYXRhLWhpZD1cImRlc2NyaXB0aW9uXCIgbmFtZT1cImRlc2NyaXB0aW9uXCIgY29udGVudD1cIlx1NzA2Ylx1N2ViZlx1NjYyZlx1NTE2OFx1NzQwM1x1OTk5Nlx1NGUyYVx1NzY3ZFx1NWUzZFx1NWI1MFx1NWYwMFx1NTNkMVx1ODAwNVx1NWU3M1x1NTNmMFx1MjAxNFx1MjAxNFx1NGUwZVx1NTZmZFx1NTE4NVx1OTg3Nlx1N2VhN1x1NzY4NFx1NzY3ZFx1NWUzZFx1NWI1MFx1NGVlY1x1NGUwMFx1OGQ3N1x1NWYwMFx1NTNkMVx1NGVhN1x1NTRjMVx1ZmYwY1x1NWU3Nlx1OTAxYVx1OGZjN1x1NGVhN1x1NTRjMVx1NGUzYVx1NGYwMVx1NGUxYVx1NWJhMlx1NjIzN1x1NjNkMFx1NGY5Ylx1NWI4OVx1NTE2OFx1NTNlZlx1NGZlMVx1NzY4NFx1NGYxN1x1NmQ0Ylx1MzAwMVx1NmUxN1x1OTAwZlx1NmQ0Ylx1OGJkNVx1MzAwMVx1N2VhMlx1ODRkZFx1NWJmOVx1NjI5N1x1N2I0OVx1OWFkOFx1N2VhN1x1NWI4OVx1NTE2OFx1NjcwZFx1NTJhMVx1MzAwMlwiPjxtZXRhIGRhdGEtbi1oZWFkPVwic3NyXCIgbmFtZT1cImZvcm1hdC1kZXRlY3Rpb25cIiBjb250ZW50PVwidGVsZXBob25lPW5vXCI+PG1ldGEgZGF0YS1uLWhlYWQ9XCJzc3JcIiBuYW1lPVwiY29weXJpZ2h0XCIgY29udGVudD1cIkNvcHlyaWdodCBcdTAwYTkgMjAyMCB8IFx1NGVhY0lDUFx1NTkwNzIwMDEzNjU5XHU1M2Y3LTEgfCBodW94aWFuIEFsbCBSaWdodHMgUmVzZXJ2ZWQuXCI+PGxpbmsgZGF0YS1uLWhlYWQ9XCJzc3JcIiByZWw9XCJpY29uXCIgdHlwZT1cImltYWdlL3gtaWNvblwiIGhyZWY9XCIvZmF2aWNvbi5pY29cIj48c2NyaXB0IGRhdGEtbi1oZWFkPVwic3NyXCIgc3JjPVwiaHR0cHM6Ly9obS5iYWlkdS5jb20vaG0uanM/YmRmZjFjMWRjY2U5NzFjM2Q5ODZmOWJlMDkyMWEwZWVcIj48L3NjcmlwdD48c2NyaXB0IGRhdGEtbi1oZWFkPVwic3NyXCIgc3JjPVwiaHR0cHM6Ly9zc2wuY2FwdGNoYS5xcS5jb20vVENhcHRjaGEuanNcIj48L3NjcmlwdD48bGluayByZWw9XCJwcmVsb2FkXCIgaHJlZj1cIi9fbnV4dC82NWJlNWM5LmpzXCIgYXM9XCJzY3JpcHRcIj48bGluayByZWw9XCJwcmVsb2FkXCIgaHJlZj1cIi9fbnV4dC81MDQ2Y2Y4LmpzXCIgYXM9XCJzY3JpcHRcIj48bGluayByZWw9XCJwcmVsb2FkXCIgaHJlZj1cIi9fbnV4dC9jc3MvMGQ1MGE5Yy5jc3NcIiBhcz1cInN0eWxlXCI+PGxpbmsgcmVsPVwicHJlbG9hZFwiIGhyZWY9XCIvX251eHQvMDc3MjIyZC5qc1wiIGFzPVwic2NyaXB0XCI+PGxpbmsgcmVsPVwicHJlbG9hZFwiIGhyZWY9XCIvX251eHQvY3NzLzAxZTlhMmYuY3NzXCIgYXM9XCJzdHlsZVwiPjxsaW5rIHJlbD1cInByZWxvYWRcIiBocmVmPVwiL19udXh0LzI4MWViMDAuanNcIiBhcz1cInNjcmlwdFwiPjxsaW5rIHJlbD1cInN0eWxlc2hlZXRcIiBocmVmPVwiL19udXh0L2Nzcy8wZDUwYTljLmNzc1wiPjxsaW5rIHJlbD1cInN0eWxlc2hlZXRcIiBocmVmPVwiL19udXh0L2Nzcy8wMWU5YTJmLmNzc1wiPlxuICA8L2hlYWQ+XG4gIDxib2R5ID5cbiAgICA8ZGl2IGRhdGEtc2VydmVyLXJlbmRlcmVkPVwidHJ1ZVwiIGlkPVwiX19udXh0XCI+PCEtLS0tPjxkaXYgaWQ9XCJfX2xheW91dFwiPjxkaXYgZGF0YS12LTc5ZWI4YzNlPjxkaXYgY2xhc3M9XCJoZWFkZXItd2FycFwiIHN0eWxlPVwiZGlzcGxheTpub25lO1wiIGRhdGEtdi03NzgxMjU2MSBkYXRhLXYtNzllYjhjM2U+PGEgaHJlZj1cImh0dHBzOi8vbXAud2VpeGluLnFxLmNvbS9zL2REdkRvNjl3ZktmMUVjblFSZTg5NHdcIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cImFkdmVydFwiIGRhdGEtdi03NzgxMjU2MT48L2E+IDxoZWFkZXIgY2xhc3M9XCJoZWFkZXJcIiBkYXRhLXYtNzc4MTI1NjE+PGEgaHJlZj1cIi9cIiBhcmlhLWN1cnJlbnQ9XCJwYWdlXCIgY2xhc3M9XCJsb2dvV2FycCBudXh0LWxpbmstZXhhY3QtYWN0aXZlIG51eHQtbGluay1hY3RpdmVcIiBzdHlsZT1cIndpZHRoOjE2MHB4O1wiIGRhdGEtdi03NzgxMjU2MT48aW1nIHNyYz1cIi9fbnV4dC9pbWcvbmV3X2xvZ28uN2E5MDc5Yi5wbmdcIiBhbHQ9XCJsb2dvXCIgY2xhc3M9XCJsb2dvXCIgZGF0YS12LTc3ODEyNTYxPiA8c3BhbiBkYXRhLXYtNzc4MTI1NjE+XG4gICAgICAgIFx1NzA2Ylx1N2ViZlx1NWI4OVx1NTE2OFx1NWU3M1x1NTNmMFxuICAgICAgPC9zcGFuPjwvYT4gPGRpdiBjbGFzcz1cInRhYldhcnBcIiBkYXRhLXYtNzc4MTI1NjE+PGkgY2xhc3M9XCJpY29uZm9udCBpY29uc2hvdXFpXCIgZGF0YS12LTc3ODEyNTYxPjwvaT4gPGRpdiBjbGFzcz1cInRhYjdVc2VyXCIgZGF0YS12LTc3ODEyNTYxPjwhLS0tLT4gPGRpdiBzdHlsZT1cImRpc3BsYXk6bm9uZTthbGlnbi1pdGVtczpjZW50ZXI7XCIgZGF0YS12LTc3ODEyNTYxPjxkaXYgZGF0YS12LTc3ODEyNTYxPjwhLS0tLT48IS0tLS0+PCEtLS0tPjwvZGl2PiA8IS0tLS0+PC9kaXY+PC9kaXY+PC9kaXY+PC9oZWFkZXI+PC9kaXY+IDxkaXYgY2xhc3M9XCJoZWFkZXItd2FycFwiIHN0eWxlPVwiZGlzcGxheTpub25lO1wiIGRhdGEtdi02MDBmODlmNyBkYXRhLXYtNzllYjhjM2U+PGEgaHJlZj1cImh0dHBzOi8vbXAud2VpeGluLnFxLmNvbS9zL2REdkRvNjl3ZktmMUVjblFSZTg5NHdcIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cImFkdmVydFwiIGRhdGEtdi02MDBmODlmNz48L2E+IDxoZWFkZXIgZGF0YS12LTYwMGY4OWY3PjxkaXYgY2xhc3M9XCJ1cmwtd2FycFwiIGRhdGEtdi02MDBmODlmNz48YSBocmVmPVwiL1wiIGFyaWEtY3VycmVudD1cInBhZ2VcIiBjbGFzcz1cImxvZ29XYXJwIG51eHQtbGluay1leGFjdC1hY3RpdmUgbnV4dC1saW5rLWFjdGl2ZVwiIGRhdGEtdi02MDBmODlmNz48aW1nIHNyYz1cIi9fbnV4dC9pbWcvbG9nby5hYmI2N2U4LnBuZ1wiIGFsdD1cImxvZ29cIiBjbGFzcz1cImxvZ29cIiBkYXRhLXYtNjAwZjg5Zjc+PC9hPiA8c3BhbiBkYXRhLXYtNjAwZjg5Zjc+PGRpdiByb2xlPVwidG9vbHRpcFwiIGlkPVwiZWwtcG9wb3Zlci04ODY4XCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi02MDBmODlmNz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NWI4OVx1NTE2OFx1NGYxN1x1NmQ0Ylx1NjcwZFx1NTJhMVxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NGYwMVx1NGUxYVNSQ1x1NjcwZFx1NTJhMVxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly9kb25ndGFpLmlvL1wiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NmQxZVx1NjAwMUlBU1RcbiAgICAgICAgICA8L2E+PC9kaXY+PC9kaXY+PHNwYW4gY2xhc3M9XCJlbC1wb3BvdmVyX19yZWZlcmVuY2Utd3JhcHBlclwiPjxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTYwMGY4OWY3PlxuICAgICAgICAgIFx1NGVhN1x1NTRjMVx1NGUwZVx1NjcwZFx1NTJhMVxuICAgICAgICA8L2Rpdj48L3NwYW4+PC9zcGFuPiA8c3BhbiBkYXRhLXYtNjAwZjg5Zjc+PGRpdiByb2xlPVwidG9vbHRpcFwiIGlkPVwiZWwtcG9wb3Zlci02NDE0XCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi02MDBmODlmNz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NjM5Mlx1ODg0Y1x1Njk5Y1xuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NzkzY1x1NTRjMVx1NTU0Nlx1NTdjZVxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly96b25lLmh1b3hpYW4uY25cIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cInVybC10YWJcIiBkYXRhLXYtNjAwZjg5Zjc+XG4gICAgICAgICAgICBcdTcwNmJcdTdlYmZab25lXG4gICAgICAgICAgPC9hPiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1OTg3OVx1NzZlZVx1NTIxN1x1ODg2OFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NTQyY1x1NzA2Yi9cdTg5YzJcdTcwNmJcdTZjOTlcdTlmOTlcbiAgICAgICAgICA8L2Rpdj4gPGEgaHJlZj1cImh0dHBzOi8vY29vcC5odW94aWFuLmNuXCIgdGFyZ2V0PVwiX2JsYW5rXCIgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTYwMGY4OWY3PlxuICAgICAgICAgICAgXHU5ODc5XHU3NmVlXHU1MzRmXHU1NDBjXHU1ZTczXHU1M2YwXG4gICAgICAgICAgPC9hPiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1N2I1Nlx1NzU2NVx1OTZjNlxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NzA2Ylx1NTY2OFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NmYwZlx1NmQxZVx1N2JhMVx1NzQwNlxuICAgICAgICAgIDwvZGl2PjwvZGl2PjwvZGl2PjxzcGFuIGNsYXNzPVwiZWwtcG9wb3Zlcl9fcmVmZXJlbmNlLXdyYXBwZXJcIj48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICBcdTc2N2RcdTVlM2RcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+PC9zcGFuPjwvc3Bhbj4gPGRpdiBjbGFzcz1cInVybC10YWJcIiBkYXRhLXYtNjAwZjg5Zjc+XG4gICAgICAgIFx1OTg3OVx1NzZlZVx1NTIxN1x1ODg2OFxuICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTYwMGY4OWY3PlxuICAgICAgICBcdTYzOTJcdTg4NGNcdTY5OWNcbiAgICAgIDwvZGl2PiA8c3BhbiBkYXRhLXYtNjAwZjg5Zjc+PGRpdiByb2xlPVwidG9vbHRpcFwiIGlkPVwiZWwtcG9wb3Zlci0xNzIxXCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi02MDBmODlmNz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NTE2Y1x1NTNmOFx1NGVjYlx1N2VjZFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgICAgIFx1NWJhMlx1NjIzN1x1Njg0OFx1NGY4YlxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly93d3cuemhpcGluLmNvbS9nb25nc2lyLzY2MzEyYjA1MTc0ZTA2MjYzblI5MHRXX0ZRfn4uaHRtbFwiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi02MDBmODlmNz5cdTUyYTBcdTUxNjVcdTYyMTFcdTRlZWM8L2E+PC9kaXY+PC9kaXY+PHNwYW4gY2xhc3M9XCJlbC1wb3BvdmVyX19yZWZlcmVuY2Utd3JhcHBlclwiPjxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTYwMGY4OWY3PlxuICAgICAgICAgIFx1NTE3M1x1NGU4ZVx1NjIxMVx1NGVlY1xuICAgICAgICA8L2Rpdj48L3NwYW4+PC9zcGFuPjwvZGl2PiA8ZGl2IGNsYXNzPVwidXNlci13YXJwXCIgc3R5bGU9XCJkaXNwbGF5Om5vbmU7XCIgZGF0YS12LTYwMGY4OWY3PjxkaXYgZGF0YS12LTYwMGY4OWY3PjxkaXYgY2xhc3M9XCJlbC1iYWRnZVwiIHN0eWxlPVwiZGlzcGxheTpub25lO21hcmdpbi1yaWdodDoyNHB4O1wiIGRhdGEtdi02MDBmODlmNz48aSBjbGFzcz1cImljb25mb250IGljb25ub3RpY2VsXCIgc3R5bGU9XCJmb250LXNpemU6MjRweDtjb2xvcjojZmZmO1wiIGRhdGEtdi02MDBmODlmNz48L2k+PHN1cCBjbGFzcz1cImVsLWJhZGdlX19jb250ZW50IGVsLWJhZGdlX19jb250ZW50LS11bmRlZmluZWQgaXMtZml4ZWRcIj4wPC9zdXA+PC9kaXY+IDxpIGNsYXNzPVwiaWNvbmZvbnQgaWNvbm5vdGljZWxcIiBzdHlsZT1cImZvbnQtc2l6ZToyNHB4O2NvbG9yOiNmZmY7bWFyZ2luLXJpZ2h0OjI0cHg7ZGlzcGxheTo7XCIgZGF0YS12LTYwMGY4OWY3PjwvaT48L2Rpdj4gPCEtLS0tPjwvZGl2PiA8ZGl2IGNsYXNzPVwicmVnLXdhcnBcIiBzdHlsZT1cImRpc3BsYXk6O1wiIGRhdGEtdi02MDBmODlmNz48YnV0dG9uIGNsYXNzPVwibG9naW5cIiBkYXRhLXYtNjAwZjg5Zjc+XG4gICAgICAgIFx1NzY3Ylx1NWY1NVxuICAgICAgPC9idXR0b24+IDxidXR0b24gY2xhc3M9XCJyZWdcIiBkYXRhLXYtNjAwZjg5Zjc+XG4gICAgICAgIFx1NmNlOFx1NTE4Y1xuICAgICAgPC9idXR0b24+IDxidXR0b24gY2xhc3M9XCJjb21wYW55LXJlZ1wiIGRhdGEtdi02MDBmODlmNz5cbiAgICAgICAgXHU3NTMzXHU4YmY3XHU2NzBkXHU1MmExXG4gICAgICA8L2J1dHRvbj48L2Rpdj4gPCEtLS0tPjwvaGVhZGVyPjwvZGl2PiA8ZGl2IGNsYXNzPVwiaGVhZGVyLXdhcnBcIiBkYXRhLXYtMDgxMzhiMjMgZGF0YS12LTc5ZWI4YzNlPjxhIGhyZWY9XCJodHRwczovL21wLndlaXhpbi5xcS5jb20vcy9kRHZEbzY5d2ZLZjFFY25RUmU4OTR3XCIgdGFyZ2V0PVwiX2JsYW5rXCIgY2xhc3M9XCJhZHZlcnRcIiBkYXRhLXYtMDgxMzhiMjM+PC9hPiA8aGVhZGVyIGRhdGEtdi0wODEzOGIyMz48ZGl2IGNsYXNzPVwidXJsLXdhcnBcIiBkYXRhLXYtMDgxMzhiMjM+PGEgaHJlZj1cIi9cIiBhcmlhLWN1cnJlbnQ9XCJwYWdlXCIgY2xhc3M9XCJsb2dvV2FycCBudXh0LWxpbmstZXhhY3QtYWN0aXZlIG51eHQtbGluay1hY3RpdmVcIiBkYXRhLXYtMDgxMzhiMjM+PGltZyBzcmM9XCIvX251eHQvaW1nL2xvZ28uYWJiNjdlOC5wbmdcIiBhbHQ9XCJsb2dvXCIgY2xhc3M9XCJsb2dvXCIgZGF0YS12LTA4MTM4YjIzPjwvYT4gPHNwYW4gZGF0YS12LTA4MTM4YjIzPjxkaXYgcm9sZT1cInRvb2x0aXBcIiBpZD1cImVsLXBvcG92ZXItMjIzXCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi0wODEzOGIyMz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NWI4OVx1NTE2OFx1NGYxN1x1NmQ0Ylx1NjcwZFx1NTJhMVxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NGYwMVx1NGUxYVNSQ1x1NjcwZFx1NTJhMVxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly9kb25ndGFpLmlvL1wiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NmQxZVx1NjAwMUlBU1RcbiAgICAgICAgICA8L2E+PC9kaXY+PC9kaXY+PHNwYW4gY2xhc3M9XCJlbC1wb3BvdmVyX19yZWZlcmVuY2Utd3JhcHBlclwiPjxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTA4MTM4YjIzPlxuICAgICAgICAgIFx1NGVhN1x1NTRjMVx1NGUwZVx1NjcwZFx1NTJhMVxuICAgICAgICA8L2Rpdj48L3NwYW4+PC9zcGFuPiA8c3BhbiBkYXRhLXYtMDgxMzhiMjM+PGRpdiByb2xlPVwidG9vbHRpcFwiIGlkPVwiZWwtcG9wb3Zlci00NTUwXCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi0wODEzOGIyMz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NjM5Mlx1ODg0Y1x1Njk5Y1xuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NzkzY1x1NTRjMVx1NTU0Nlx1NTdjZVxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly96b25lLmh1b3hpYW4uY25cIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cInVybC10YWJcIiBkYXRhLXYtMDgxMzhiMjM+XG4gICAgICAgICAgICBcdTcwNmJcdTdlYmZab25lXG4gICAgICAgICAgPC9hPiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1OTg3OVx1NzZlZVx1NTIxN1x1ODg2OFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NTQyY1x1NzA2Yi9cdTg5YzJcdTcwNmJcdTZjOTlcdTlmOTlcbiAgICAgICAgICA8L2Rpdj4gPGEgaHJlZj1cImh0dHBzOi8vY29vcC5odW94aWFuLmNuXCIgdGFyZ2V0PVwiX2JsYW5rXCIgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTA4MTM4YjIzPlxuICAgICAgICAgICAgXHU5ODc5XHU3NmVlXHU1MzRmXHU1NDBjXHU1ZTczXHU1M2YwXG4gICAgICAgICAgPC9hPiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1N2I1Nlx1NzU2NVx1OTZjNlxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NzA2Ylx1NTY2OFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NmYwZlx1NmQxZVx1N2JhMVx1NzQwNlxuICAgICAgICAgIDwvZGl2PjwvZGl2PjwvZGl2PjxzcGFuIGNsYXNzPVwiZWwtcG9wb3Zlcl9fcmVmZXJlbmNlLXdyYXBwZXJcIj48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICBcdTc2N2RcdTVlM2RcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+PC9zcGFuPjwvc3Bhbj4gPGRpdiBjbGFzcz1cInVybC10YWJcIiBkYXRhLXYtMDgxMzhiMjM+XG4gICAgICAgIFx1OTg3OVx1NzZlZVx1NTIxN1x1ODg2OFxuICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTA4MTM4YjIzPlxuICAgICAgICBcdTYzOTJcdTg4NGNcdTY5OWNcbiAgICAgIDwvZGl2PiA8c3BhbiBkYXRhLXYtMDgxMzhiMjM+PGRpdiByb2xlPVwidG9vbHRpcFwiIGlkPVwiZWwtcG9wb3Zlci04Mjg5XCIgYXJpYS1oaWRkZW49XCJ0cnVlXCIgY2xhc3M9XCJlbC1wb3BvdmVyIGVsLXBvcHBlciBoZWFkZXItZHJvcC1wb3BvdmVyXCIgc3R5bGU9XCJ3aWR0aDoxMDBweDtkaXNwbGF5Om5vbmU7XCI+PCEtLS0tPiA8ZGl2IHN0eWxlPVwiZGlzcGxheTpmbGV4O1wiIGRhdGEtdi0wODEzOGIyMz48ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NTE2Y1x1NTNmOFx1NGVjYlx1N2VjZFxuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgICAgIFx1NWJhMlx1NjIzN1x1Njg0OFx1NGY4YlxuICAgICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly93d3cuemhpcGluLmNvbS9nb25nc2lyLzY2MzEyYjA1MTc0ZTA2MjYzblI5MHRXX0ZRfn4uaHRtbFwiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsLXRhYlwiIGRhdGEtdi0wODEzOGIyMz5cdTUyYTBcdTUxNjVcdTYyMTFcdTRlZWM8L2E+PC9kaXY+PC9kaXY+PHNwYW4gY2xhc3M9XCJlbC1wb3BvdmVyX19yZWZlcmVuY2Utd3JhcHBlclwiPjxkaXYgY2xhc3M9XCJ1cmwtdGFiXCIgZGF0YS12LTA4MTM4YjIzPlxuICAgICAgICAgIFx1NTE3M1x1NGU4ZVx1NjIxMVx1NGVlY1xuICAgICAgICA8L2Rpdj48L3NwYW4+PC9zcGFuPjwvZGl2PiA8ZGl2IGNsYXNzPVwidXNlci13YXJwXCIgc3R5bGU9XCJkaXNwbGF5Om5vbmU7XCIgZGF0YS12LTA4MTM4YjIzPjxkaXYgZGF0YS12LTA4MTM4YjIzPjxkaXYgY2xhc3M9XCJlbC1iYWRnZVwiIHN0eWxlPVwiZGlzcGxheTpub25lO21hcmdpbi1yaWdodDoyNHB4O1wiIGRhdGEtdi0wODEzOGIyMz48aSBjbGFzcz1cImljb25mb250IGljb25ub3RpY2VsXCIgc3R5bGU9XCJmb250LXNpemU6MjRweDtjb2xvcjojZmZmO1wiIGRhdGEtdi0wODEzOGIyMz48L2k+PHN1cCBjbGFzcz1cImVsLWJhZGdlX19jb250ZW50IGVsLWJhZGdlX19jb250ZW50LS11bmRlZmluZWQgaXMtZml4ZWRcIj4wPC9zdXA+PC9kaXY+IDxpIGNsYXNzPVwiaWNvbmZvbnQgaWNvbm5vdGljZWxcIiBzdHlsZT1cImZvbnQtc2l6ZToyNHB4O2NvbG9yOiNmZmY7bWFyZ2luLXJpZ2h0OjI0cHg7ZGlzcGxheTo7XCIgZGF0YS12LTA4MTM4YjIzPjwvaT48L2Rpdj4gPCEtLS0tPjwvZGl2PiA8ZGl2IGNsYXNzPVwicmVnLXdhcnBcIiBzdHlsZT1cImRpc3BsYXk6O1wiIGRhdGEtdi0wODEzOGIyMz48YnV0dG9uIGNsYXNzPVwibG9naW5cIiBkYXRhLXYtMDgxMzhiMjM+XG4gICAgICAgIFx1NzY3Ylx1NWY1NVxuICAgICAgPC9idXR0b24+IDxidXR0b24gY2xhc3M9XCJyZWdcIiBkYXRhLXYtMDgxMzhiMjM+XG4gICAgICAgIFx1NmNlOFx1NTE4Y1xuICAgICAgPC9idXR0b24+IDxidXR0b24gY2xhc3M9XCJjb21wYW55LXJlZ1wiIGRhdGEtdi0wODEzOGIyMz5cbiAgICAgICAgXHU3NTMzXHU4YmY3XHU2NzBkXHU1MmExXG4gICAgICA8L2J1dHRvbj48L2Rpdj4gPCEtLS0tPjwvaGVhZGVyPjwvZGl2PiA8ZGl2IGNsYXNzPVwibGF5b3V0LWNvbnRhaW5lclwiIGRhdGEtdi03OWViOGMzZT48IS0tLS0+IDxtYWluIGRhdGEtdi03OWViOGMzZT48bWFpbiBkYXRhLXYtNjQyNDI0MjQgZGF0YS12LTc5ZWI4YzNlPjxzZWN0aW9uIGNsYXNzPVwiYmFubmVyLXdhcnBcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cImNvbnRhaW5lclwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwidGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgIFx1NWUyZVx1NjBhOFx1NjI3ZVx1NTIzMFx1NjcyYVx1NzdlNVx1NmYwZlx1NmQxZVxuICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICBcdTc1MzFcdTc5M2VcdTUzM2FcdTRmMTdcdTU5MWFcdTViOWVcdTU0MGRcdTViODlcdTUxNjhcdTRlMTNcdTViYjZcdTRlMGVcdTgxZWFcdTUyYThcdTUzMTZcdTY3M2FcdTU2NjhcdTRlYmFcdTUzNGZcdTRmNWNcdTRlYTRcdTRlZDhcdTY2ZjRcdTlhZDhcdThkMjhcdTkxY2ZcdTc2ODRcdTZmMGZcdTZkMWVcdTZkNGJcdThiZDVcdTYyYTVcdTU0NGFcbiAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVtby1saW5lXCIgZGF0YS12LTY0MjQyNDI0PjxpbnB1dCB0eXBlPVwidGV4dFwiIHBsYWNlaG9sZGVyPVwiXHU4YmY3XHU4ZjkzXHU1MTY1XHU2MGE4XHU3Njg0XHU0ZjAxXHU0ZTFhXHU5MGFlXHU3YmIxXCIgdmFsdWU9XCJcIiBkYXRhLXYtNjQyNDI0MjQ+IDxidXR0b24gZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgIFx1OGJmN1x1NmM0Mlx1NmYxNFx1NzkzYVxuICAgICAgICA8L2J1dHRvbj48L2Rpdj48L2Rpdj4gPCEtLS0tPjwvc2VjdGlvbj4gPHNlY3Rpb24gY2xhc3M9XCJjb250YWluZXIgbmV3cy13YXJwXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJsZWZ0LXdhcnBcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cIm1vZHVsZS10aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgXHU3OTNlXHU1MzNhXHU1MmE4XHU2MDAxXG4gICAgICA8L2Rpdj4gPGRpdiBjbGFzcz1cInpvbmUtd2FycFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwib3ZlcnZpZXdcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cImltZy1iZ1wiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwianVtcFwiIGRhdGEtdi02NDI0MjQyND48YnV0dG9uIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgICBcdThmZGJcdTUxNjVcdTRlMTNcdTk4OThcbiAgICAgICAgICAgICAgPC9idXR0b24+PC9kaXY+IDxkaXYgY2xhc3M9XCJ0aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgXHU3MDZiXHU3ZWJmIFpvbmVcbiAgICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgXHU1YjllXHU2MjE4XHU2NTNiXHU5NjMyXHU2MjgwXHU2NzJmXHU3OTNlXHU1MzNhXG4gICAgICAgICAgICA8L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImFydGljbGUtd2FycFwiIGRhdGEtdi02NDI0MjQyND48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImJpbGliaWxpLXdhcnBcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cIm92ZXJ2aWV3XCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJpbWctYmdcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cImp1bXBcIiBkYXRhLXYtNjQyNDI0MjQ+PGJ1dHRvbiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgICAgXHU4ZmRiXHU1MTY1XHU0ZTEzXHU5ODk4XG4gICAgICAgICAgICAgIDwvYnV0dG9uPjwvZGl2PiA8ZGl2IGNsYXNzPVwidGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgIFx1NTQyY1x1NzA2Yi9cdTg5YzJcdTcwNmJcbiAgICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgXHU2MjgwXHU2NzJmXHU2Yzk5XHU5Zjk5XG4gICAgICAgICAgICA8L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cInZpZGVvLXdhcnBcIiBkYXRhLXYtNjQyNDI0MjQ+PC9kaXY+PC9kaXY+PC9kaXY+IDxkaXYgY2xhc3M9XCJtb2JpbGUtd2FycFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwibW9kdWxlLXRpdGxlXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICBcdTc5M2VcdTUzM2FcdTUyYThcdTYwMDFcbiAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidGFiLWxpbmVcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cInRhYiBzZWxlY3RUYWJcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgXHU3MDZiXHU3ZWJmIFpvbmVcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ0YWJcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgXHU1NDJjXHU3MDZiL1x1ODljMlx1NzA2YlxuICAgICAgICA8L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImJpbGliaWxpLXdhcnBcIiBzdHlsZT1cImRpc3BsYXk6bm9uZTtcIiBkYXRhLXYtNjQyNDI0MjQ+IDxhIGhyZWY9XCJodHRwczovL3NwYWNlLmJpbGliaWxpLmNvbS81MDMzMzA0MTlcIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cImp1bXBcIiBkYXRhLXYtNjQyNDI0MjQ+XHU4ZmRiXHU1MTY1XHU0ZTEzXHU5ODk4ICZndDs8L2E+PC9kaXY+IDxkaXYgY2xhc3M9XCJ6b25lLXdhcnBcIiBzdHlsZT1cImRpc3BsYXk6O1wiIGRhdGEtdi02NDI0MjQyND4gPGEgaHJlZj1cImh0dHBzOi8vem9uZS5odW94aWFuLmNuXCIgdGFyZ2V0PVwiX2JsYW5rXCIgY2xhc3M9XCJqdW1wXCIgZGF0YS12LTY0MjQyNDI0Plx1OGZkYlx1NTE2NVx1NGUxM1x1OTg5OCAmZ3Q7PC9hPjwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwicmlnaHQtd2FycFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwibW9kdWxlLXRpdGxlXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICBcdTYzOTJcdTg4NGNcdTY5OWNcbiAgICAgIDwvZGl2PiA8IS0tLS0+IDxhIGhyZWY9XCIvd2hpdGVoYXQvUmFua0xpc3RcIiBjbGFzcz1cInJhbmstbGlzdC1idG5cIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgIFx1OGZkYlx1NTE2NVx1NjM5Mlx1ODg0Y1x1Njk5YyAmZ3Q7XG4gICAgICA8L2E+IDxkaXYgY2xhc3M9XCJtb2R1bGUtdGl0bGVcIiBzdHlsZT1cIm1hcmdpbi10b3A6IDMxcHhcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgIFx1OTg3OVx1NzZlZVx1NTJhOFx1NjAwMVxuICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ0cmVuZHMtd2FycFwiIGRhdGEtdi02NDI0MjQyND48L2Rpdj48L2Rpdj48L3NlY3Rpb24+IDxzZWN0aW9uIGNsYXNzPVwic2VydmljZS13YXJwXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJjb250YWluZXJcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cIm1vZHVsZS10aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgXHU0ZTEzXHU0ZTFhXHU2NzBkXHU1MmExXG4gICAgICA8L2Rpdj4gPGRpdiBjbGFzcz1cImNvbnRlbnQtd2FycFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwibGVmdC13YXJwXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJkZXNjLWxpbmUgc2VydmljZS1pY29uLWVudGVyXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJzZXJ2aWNlLWljb24gaWNvbjFcIiBkYXRhLXYtNjQyNDI0MjQ+PC9kaXY+IDxkaXYgc3R5bGU9XCJmbGV4OiAxO21hcmdpbi1sZWZ0OiAxOHB4XCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJ0aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgICBcdTViOWVcdTU0MGRcdTUyMzZcdTUzZWZcdTRmZTFcdThkNTZcdTc2ODRcdTc2N2RcdTVlM2RcdTViNTBcdTc5M2VcdTUzM2FcdThkNDRcdTZlOTBcbiAgICAgICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJzdWJUaXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgICBcdTRmN2ZcdTc1MjhcdTUxNjhcdTU2ZmRcdTY3MDBcdTRmMThcdThkMjhcdTc2ODRcdTUzZWZcdTRmZTFcdThkNTZcdTViODlcdTUxNjhcdTc2N2RcdTVlM2RcdTViNTBcdThkNDRcdTZlOTBcdWZmMGNcdTRlYmFcdTU0NThcdTU5MWFcdTkxY2RcdThiYTRcdThiYzFcdTdiN2VcdTdlYTZcdWZmMGNcdTUzZWZcdTRmZTFcdTcyYjZcdTYwMDFcdTRlMGJcdTY3MDBcdTU5MjdcdTk2NTBcdTVlYTZcdTc2ODRcdTUzZDFcdTczYjBcdTY3MmFcdTc3ZTVcdTZmMGZcdTZkMWVcbiAgICAgICAgICAgICAgPC9kaXY+PC9kaXY+PC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjLWxpbmUgc2VydmljZS1pY29uLWxlYXZlXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJzZXJ2aWNlLWljb24gaWNvbjJcIiBkYXRhLXYtNjQyNDI0MjQ+PC9kaXY+IDxkaXYgc3R5bGU9XCJmbGV4OiAxO21hcmdpbi1sZWZ0OiAxOHB4XCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJ0aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgICBcdTRlYmFcdTY3M2FcdTUzNGZcdTU0MGNcdTc2ODRcdTRlOTFcdTdhZWZcdTUzZWZcdTYzYTdcdTViODlcdTUxNjhcdTY3MGRcdTUyYTFcdTZhMjFcdTVmMGZcbiAgICAgICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJzdWJUaXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgICAgICBcdTRlYmFcdTY3M2FcdTUzNGZcdTU0MGNcdTc2ODRcdTk4NzlcdTc2ZWVcdTY3MGRcdTUyYTFcdTZhMjFcdTVmMGZcdWZmMGM3KjI0XHU1YzBmXHU2NWY2XHU2NzAwXHU1OTI3XHU5NjUwXHU1ZWE2XHU3Njg0XHU5YWQ4XHU2NTQ4XHU3Mzg3XHU4OTg2XHU3NmQ2XHU2MjQwXHU2NzA5XHU4ZDQ0XHU0ZWE3XHU3Njg0XHU1Yjg5XHU1MTY4XHU2ZDRiXHU4YmQ1XG4gICAgICAgICAgICAgIDwvZGl2PjwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzYy1saW5lIHNlcnZpY2UtaWNvbi1sZWF2ZVwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwic2VydmljZS1pY29uIGljb24zXCIgZGF0YS12LTY0MjQyNDI0PjwvZGl2PiA8ZGl2IHN0eWxlPVwiZmxleDogMTttYXJnaW4tbGVmdDogMThweFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwidGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgICAgXHU0ZTkyXHU4MDU0XHU3ZjUxXHU5OGNlXHU5NjY5XHU5NzYyXHU3YmExXHU3NDA2XG4gICAgICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwic3ViVGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgICAgXHU2NTcwXHU0ZWJmXHU2NTcwXHU2MzZlXHU1MTczXHU4MDU0XHU3Njg0XHU5OGNlXHU5NjY5XHU5NzYyXHU3NmQxXHU2M2E3XHVmZjBjXHU1YjllXHU2NWY2XHU3NmQxXHU2M2E3XHU0ZjAxXHU0ZTFhXHU1Yjg5XHU1MTY4XHU5OGNlXHU5NjY5XHVmZjBjXHU5MDFhXHU4ZmM3XHU2NTcwXHU2MzZlXHU3ZWE2XHU2NzVmXHU2ZDRiXHU4YmQ1XHU4ZmI5XHU3NTRjXG4gICAgICAgICAgICAgIDwvZGl2PjwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzYy1saW5lIHNlcnZpY2UtaWNvbi1sZWF2ZVwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwic2VydmljZS1pY29uIGljb240XCIgZGF0YS12LTY0MjQyNDI0PjwvZGl2PiA8ZGl2IHN0eWxlPVwiZmxleDogMTttYXJnaW4tbGVmdDogMThweFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwidGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgICAgXHU2ZDRiXHU4YmQ1XHU4ZmM3XHU3YTBiXHU1MTY4XHU3YTBiXHU1M2VmXHU4OWM2XG4gICAgICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwic3ViVGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICAgICAgXHU1N2ZhXHU0ZThlXHU0ZTkxXHU3YWVmXHU3Njg0XHU0ZWJhXHU2NzNhXHU1MzRmXHU1NDBjXHU2ZDRiXHU4YmQ1XHVmZjBjXHU1Yjg5XHU1MTY4XHU2ZDRiXHU4YmQ1XHU2NTcwXHU2MzZlXHU1MTY4XHU3YTBiXHU1M2VmXHU4OWMxXG4gICAgICAgICAgICAgIDwvZGl2PjwvZGl2PjwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwicmlnaHQtd2FycFwiIGRhdGEtdi02NDI0MjQyND48aW1nIHNyYz1cIi9fbnV4dC9pbWcvMS43MTAwYzE3LnBuZ1wiIGFsdCBzdHlsZT1cImRpc3BsYXk6O1wiIGRhdGEtdi02NDI0MjQyND4gPGltZyBzcmM9XCIvX251eHQvaW1nLzIuNGUyNmQyOS5wbmdcIiBhbHQgc3R5bGU9XCJkaXNwbGF5Om5vbmU7XCIgZGF0YS12LTY0MjQyNDI0PiA8aW1nIHNyYz1cIi9fbnV4dC9pbWcvMy41MTlkZWMxLnBuZ1wiIGFsdCBzdHlsZT1cImRpc3BsYXk6bm9uZTtcIiBkYXRhLXYtNjQyNDI0MjQ+IDxpbWcgc3JjPVwiL19udXh0L2ltZy80LmZlNmYyN2YucG5nXCIgYWx0IHN0eWxlPVwiZGlzcGxheTpub25lO1wiIGRhdGEtdi02NDI0MjQyND48L2Rpdj48L2Rpdj48L2Rpdj48L3NlY3Rpb24+IDxzZWN0aW9uIGNsYXNzPVwiY3VzdG9tZXItd2FycFwiIGRhdGEtdi02NDI0MjQyND48ZGl2IGNsYXNzPVwiY29udGFpbmVyXCIgZGF0YS12LTY0MjQyNDI0PjxkaXYgY2xhc3M9XCJtb2R1bGUtdGl0bGVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgIFx1NWJhMlx1NjIzN1x1OGJhNFx1NTNlZlxuICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJjb250ZW50LXdhcnBcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cImNhcmRcIiBkYXRhLXYtNjQyNDI0MjQ+PCEtLS0tPiA8ZGl2IGNsYXNzPVwibmFtZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgIFx1OGQxZFx1NThmM1xuICAgICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgIFx1NzA2Ylx1N2ViZlx1NWI4OVx1NTE2OFx1NWU3M1x1NTNmMFx1NTcyOFx1NmJjZlx1NGUwMFx1NmIyMVx1NGYxN1x1NmQ0Ylx1NmQzYlx1NTJhOFx1NGUyZFx1OTBmZFx1ODBmZFx1NTNkMVx1NzNiMFx1NjIxMVx1NGVlY1x1NWY4OFx1NTkxYVx1OWFkOFx1NTM3MVx1NGUyNVx1OTFjZFx1NzY4NFx1OTVlZVx1OTg5OFx1ZmYwY1x1N2VkOVx1NjIxMVx1NGVlY1x1NWUyNlx1Njc2NVx1NGU4Nlx1NWY4OFx1NTkxYVx1NGUxYVx1NTJhMVx1NzY4NFx1NGVmN1x1NTAzY1x1MzAwMlxuICAgICAgICAgIDwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiY2FyZFwiIGRhdGEtdi02NDI0MjQyND48IS0tLS0+IDxkaXYgY2xhc3M9XCJuYW1lXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU0ZWFjXHU0ZTFjXG4gICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU3MDZiXHU3ZWJmXHU1Yjg5XHU1MTY4XHU1ZTczXHU1M2YwXHU1NDhjXHU2MjExXHU0ZWVjXHU3Njg0XHU1NDA4XHU0ZjVjXHU5NzVlXHU1ZTM4XHU3ZDI3XHU1YmM2XHVmZjBjXHU2NTQ4XHU2NzljXHU1N2ZhXHU2NzJjXHU0ZjE4XHU0ZThlXHU1NDBjXHU2NzFmXHU2ZDNiXHU1MmE4XHU3Njg0MzAlXHU0ZWU1XHU0ZTBhXHVmZjBjXHU2NjJmXHU2MjExXHU0ZWVjXHU1NDA4XHU0ZjVjXHU4ZmM3XHU3Njg0XHU2NzAwXHU3NTI4XHU1ZmMzXHU3Njg0XHU1MzgyXHU1NTQ2XHVmZjBjXHU1ZTczXHU1M2YwXHU3Njg0XHU4ZmQwXHU4NDI1XHU1NDBjXHU1YjY2XHU5NzVlXHU1ZTM4XHU3NTI4XHU1ZmMzXHVmZjBjXHU1NDA4XHU0ZjVjXHU4ZmM3XHU3YTBiXHU5NzVlXHU1ZTM4XHU2MTA5XHU1ZmViXHUzMDAyXG4gICAgICAgICAgPC9kaXY+PC9kaXY+IDxkaXYgY2xhc3M9XCJjYXJkXCIgZGF0YS12LTY0MjQyNDI0PjwhLS0tLT4gPGRpdiBjbGFzcz1cIm5hbWVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICBcdTY1ZjdcdTg5YzZcbiAgICAgICAgICA8L2Rpdj4gPGRpdiBjbGFzcz1cImRlc2NcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICBcdTcwNmJcdTdlYmZcdTc2ODRcdThkNDRcdTRlYTdcdTY1M2JcdTUxZmJcdTk3NjJcdTY3MGRcdTUyYTFcdTgwZmRcdTU5MWZcdTUyYThcdTYwMDFcdTMwMDFcdTU0NjhcdTY3MWZcdTYwMjdcdTc2ODRcdThmZGJcdTg4NGNcdThkNDRcdTRlYTdcdTY4YzBcdTZkNGJcdWZmMGNcdTgwZmRcdTU5MWZcdTYzYTJcdTZkNGJcdTRlMGVcdTUzZDFcdTczYjBcdTUxNmNcdTUzZjhcdTUxODVcdTkwZThcdThmYjlcdTdmMThcdThkNDRcdTRlYTdcdTU0OGNcdTY3MmFcdTc3ZTVcdThkNDRcdTRlYTdcdWZmMGNcdThiYTlcdTRmMDFcdTRlMWFcdTc1MjhcdTYyMzdcdTgwZmRcdTU5MWZcdTViZjlcdTVlOTRcdTc1MjhcdTRlMGFcdTRlMGJcdTZlMzhcdTUxNzNcdTdjZmJcdThmZGJcdTg4NGNcdTY4YjNcdTc0MDZcdWZmMGNcdTVjMDZcdTRlOTJcdTgwNTRcdTdmNTFcdTk4Y2VcdTk2NjlcdTY2YjRcdTk3MzJcdTk3NjJcdThmZGJcdTg4NGNcdTYzMDFcdTdlZWRcdTY1MzZcdTY1NWJcdTMwMDJcbiAgICAgICAgICA8L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImNvbnRlbnQtd2FycFwiIHN0eWxlPVwibWFyZ2luLXRvcDogMTZweDtcIiBkYXRhLXYtNjQyNDI0MjQ+PGRpdiBjbGFzcz1cImNhcmRcIiBkYXRhLXYtNjQyNDI0MjQ+PCEtLS0tPiA8ZGl2IGNsYXNzPVwibmFtZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgIFx1OWIzY1x1OWVhNlx1NWI1MC9yYXNjYTFcbiAgICAgICAgICA8L2Rpdj4gPGRpdiBjbGFzcz1cInRpdGxlXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU4ZDQ0XHU2ZGYxXHU3NjdkXHU1ZTNkXHU1YjUwXHU0ZTEzXHU1YmI2XG4gICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU3MDZiXHU3ZWJmXHU3Njg0XHU4ZDQ0XHU0ZWE3XHU2NTNiXHU1MWZiXHU5NzYyXHU2NzBkXHU1MmExXHU2NjJmXHU3NmVlXHU1MjRkXHU0ZTNhXHU2YjYyXHU0ZTNhXHU2NzAwXHU1YjllXHU3NTI4XHUzMDAxXHU5YWQ4XHU2NTQ4XHU3Njg0XHU4ZDQ0XHU0ZWE3XHU3YmExXHU3NDA2XHU1ZTczXHU1M2YwXHVmZjBjXHU0ZWQ2XHU3Njg0XHU1ZjAwXHU1M2QxXHU1NmUyXHU5NjFmXHU3NDA2XHU4OWUzXHU3NTMyXHU2NWI5XHU0ZTFhXHU1MmExXHU1Yjg5XHU1MTY4XHU3Njg0XHU1NDBjXHU2NWY2XHU0ZTVmXHU3NDA2XHU4OWUzXHU2NTNiXHU1MWZiXHU2NWI5XHU3Njg0XHU1Yjg5XHU1MTY4XHU2ZDRiXHU4YmQ1XHU2MjRiXHU2Y2Q1XHVmZjBjXHU1N2ZhXHU0ZThlXHU3MDZiXHU3ZWJmXHU1ZTczXHU1M2YwXHU0ZTBhXHU3Njg0XHU3NjdkXHU1ZTNkXHU1YjUwXHU0ZWVjXHVmZjBjXHU4MGZkXHU1OTFmXHU2NmY0XHU1ZmViXHU5MDFmXHU2NzA5XHU2NTQ4XHU3Njg0XHU1M2QxXHU3M2IwXHU3NTMyXHU2NWI5XHU1Yjg5XHU1MTY4XHU2ZjBmXHU2ZDFlXHVmZjBjXHU4OWUzXHU1MWIzXHU0ZTFhXHU1MmExXHU1Yjg5XHU1MTY4XHU5NWVlXHU5ODk4XHUzMDAyXG4gICAgICAgICAgPC9kaXY+PC9kaXY+IDxkaXYgY2xhc3M9XCJjYXJkXCIgZGF0YS12LTY0MjQyNDI0PjwhLS0tLT4gPGRpdiBjbGFzcz1cIm5hbWVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICBEXG4gICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ0aXRsZVwiIGRhdGEtdi02NDI0MjQyND5cbiAgICAgICAgICAgIFx1NzA2Ylx1N2ViZlx1NWU3M1x1NTNmMDIwMjBcdTVlNzRUT1AxXHU3NjdkXHU1ZTNkXHU0ZTEzXHU1YmI2XG4gICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU0ZmUxXHU2MDZmXHU2NDFjXHU5NmM2XHU2NjJmXHU2ZjBmXHU2ZDFlXHU2MzE2XHU2Mzk4XHU0ZTJkXHU3Njg0XHU5MWNkXHU4OTgxXHU0ZTAwXHU3M2FmXHVmZjBjXHU3MDZiXHU1NjY4XHU2NjJmXHU1ZjNhXHU1OTI3XHU4MDBjXHU1MTQ4XHU4ZmRiXHU3Njg0XHU4Zjg1XHU1MmE5XHU1ZGU1XHU1MTc3XHVmZjBjXHU1ZTczXHU1M2YwXHU2M2QwXHU0ZjliXHU4ZDQ0XHU2ZTkwXHUzMDAxXHU1ZTI2XHU1YmJkXHUzMDAxXHU1ZjAwXHU1M2QxXHU0ZWJhXHU1MjliXHU3YjQ5XHU2NzA5XHU2NTQ4XHU1MzRmXHU1MmE5XHU3NjdkXHU1ZTNkXHU1YjUwXHU2NmY0XHU5YWQ4XHU2NTQ4XHU3Njg0XHU4ZmRiXHU4ODRjXHU2ZjBmXHU2ZDFlXHU2MzE2XHU2Mzk4XHUzMDAyXG4gICAgICAgICAgPC9kaXY+PC9kaXY+IDxkaXYgY2xhc3M9XCJjYXJkXCIgZGF0YS12LTY0MjQyNDI0PjwhLS0tLT4gPGRpdiBjbGFzcz1cIm5hbWVcIiBkYXRhLXYtNjQyNDI0MjQ+XG4gICAgICAgICAgICBcdTVjMGZcdTdiM2NcdTUzMDVcbiAgICAgICAgICA8L2Rpdj4gPGRpdiBjbGFzcz1cInRpdGxlXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU3N2U1XHU1NDBkXHU3NjdkXHU1ZTNkXHU1YjUwXHU0ZTEzXHU1YmI2XG4gICAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJkZXNjXCIgZGF0YS12LTY0MjQyNDI0PlxuICAgICAgICAgICAgXHU3MDZiXHU1NjY4XHU2NjJmXHU0ZTAwXHU0ZTJhXHU5NzVlXHU1ZTM4XHU1OTdkXHU3Njg0XHU4ZDQ0XHU0ZWE3XHU0ZmUxXHU2MDZmXHU2NTM2XHU5NmM2XHU1ZGU1XHU1MTc3XHVmZjBjXHU0ZmUxXHU2MDZmXHU2NTM2XHU5NmM2XHU2NjJmXHU2ZTE3XHU5MDBmXHU3Njg0XHU2NzJjXHU4ZDI4XHVmZjBjXHU1NzI4XHU1ZTczXHU2NWY2XHU2ZTE3XHU5MDBmXHU2ZDRiXHU4YmQ1XHU4ZmM3XHU3YTBiXHU0ZTJkXHU3MDZiXHU1NjY4XHU0ZTNhXHU2MjExXHU0ZWVjXHU4MjgyXHU3NzAxXHU0ZTg2XHU1OTI3XHU5MWNmXHU2NWY2XHU5NWY0XHU2MjEwXHU2NzJjXHVmZjBjXHU1ZTc2XHU0ZTE0XHU3MDZiXHU1NjY4XHU2MmU1XHU2NzA5XHU3NzQwXHU3MDZiXHU3ZWJmXHU1ZTczXHU1M2YwXHU0ZTEzXHU0ZTFhXHU0ZWJhXHU1NDU4XHU3Njg0XHU3ZWY0XHU2MmE0XHVmZjBjXHU1ZTBjXHU2NzFiXHU3MDZiXHU1NjY4XHU4ZDhhXHU2NzY1XHU4ZDhhXHU5YWQ4XHU2NTQ4XHU4ZDhhXHU2NzY1XHU4ZDhhXHU1Mzg5XHU1YmIzXHUzMDAyXG4gICAgICAgICAgPC9kaXY+PC9kaXY+PC9kaXY+PC9kaXY+PC9zZWN0aW9uPjwvbWFpbj48L21haW4+PC9kaXY+IDxmb290ZXIgc3R5bGU9XCJkaXNwbGF5Om5vbmU7XCIgZGF0YS12LTUxMmI3NDI1IGRhdGEtdi03OWViOGMzZT48ZGl2IGNsYXNzPVwiZGVtby13YXJwXCIgZGF0YS12LTUxMmI3NDI1PjxkaXYgY2xhc3M9XCJjb250YWluZXIgZGVtby1jb250ZW50XCIgZGF0YS12LTUxMmI3NDI1PjxzcGFuIGRhdGEtdi01MTJiNzQyNT5cdTc1MzFcdTc5M2VcdTUzM2FcdTRmMTdcdTU5MWFcdTViOWVcdTU0MGRcdTViODlcdTUxNjhcdTRlMTNcdTViYjZcdTRlMGVcdTgxZWFcdTUyYThcdTUzMTZcdTY3M2FcdTU2NjhcdTRlYmFcdTUzNGZcdTRmNWNcdTRlYTRcdTRlZDhcdTY2ZjRcdTlhZDhcdThkMjhcdTkxY2ZcdTc2ODRcdTZmMGZcdTZkMWVcdTZkNGJcdThiZDVcdTYyYTVcdTU0NGFcdWZmMDE8L3NwYW4+IDxkaXYgZGF0YS12LTUxMmI3NDI1PjxpbnB1dCB0eXBlPVwidGV4dFwiIHBsYWNlaG9sZGVyPVwiXHU4YmY3XHU4ZjkzXHU1MTY1XHU2MGE4XHU3Njg0XHU0ZjAxXHU0ZTFhXHU5MGFlXHU3YmIxXCIgdmFsdWU9XCJcIiBkYXRhLXYtNTEyYjc0MjU+IDxidXR0b24gZGF0YS12LTUxMmI3NDI1PlxuICAgICAgICAgIFx1OGJmN1x1NmM0Mlx1NmYxNFx1NzkzYVxuICAgICAgICA8L2J1dHRvbj48L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImNvbnRhaW5lclwiIGRhdGEtdi01MTJiNzQyNT48ZGl2IGNsYXNzPVwidXJsLXdhcnBcIiBkYXRhLXYtNTEyYjc0MjU+PGRpdiBjbGFzcz1cImNvbHVtbiBsb2NhdGlvblwiIGRhdGEtdi01MTJiNzQyNT48YSBocmVmPVwiL1wiIGFyaWEtY3VycmVudD1cInBhZ2VcIiBjbGFzcz1cIm51eHQtbGluay1leGFjdC1hY3RpdmUgbnV4dC1saW5rLWFjdGl2ZVwiIGRhdGEtdi01MTJiNzQyNT48aW1nIHNyYz1cIi9fbnV4dC9pbWcvbG9nby5hYmI2N2U4LnBuZ1wiIGFsdD1cImxvZ29cIiBjbGFzcz1cImxvZ29cIiBkYXRhLXYtNTEyYjc0MjU+PC9hPiA8ZGl2IGNsYXNzPVwiZGVzY1wiIHN0eWxlPVwibWFyZ2luLXRvcDogOHB4O1wiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTkwYWVcdTdiYjFcdWZmMWFoaUBodW94aWFuLmNuXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTc1MzVcdThiZGRcdWZmMWE8YSBocmVmPVwidGVsOjAxMC04Mjc3MjY2MFwiIGRhdGEtdi01MTJiNzQyNT4wMTAtODI3NzI2NjA8L2E+PGEgaHJlZj1cInRlbDoxOTkxMDM4Njc5N1wiIGRhdGEtdi01MTJiNzQyNT4xOTkgMTAzOCA2Nzk3PC9hPjwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTYwM2JcdTkwZThcdWZmMWFcdTUzMTdcdTRlYWNcdTVlMDJcdTZkNzdcdTZkYzBcdTUzM2FcdTRlMGFcdTU3MzBcdTRlMWNcdThkZWYzNVx1NTNmN1x1OTg5MFx1NmNjOVx1NmM0N0NcdTVlYTczXHU1YzQyXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTUyMDZcdTY1MmZcdTY3M2FcdTY3ODRcdWZmMWFcdTRlMGFcdTZkNzcgXHU2ZGYxXHU1NzMzXG4gICAgICAgIDwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTUxMmI3NDI1PjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTRlYTdcdTU0YzFcdTRlMGVcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTViODlcdTUxNjhcdTRmMTdcdTZkNGJcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgXHU0ZjAxXHU0ZTFhU1JDXHU2NzBkXHU1MmExXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly9kb25ndGFpLmlvL1wiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsXCIgZGF0YS12LTUxMmI3NDI1PlxuICAgICAgICAgIFx1NmQxZVx1NjAwMUlBU1RcbiAgICAgICAgPC9hPjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTUxMmI3NDI1PjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTc2N2RcdTVlM2RcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTk4NzlcdTc2ZWVcdTUyMTdcdTg4NjhcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgXHU2MzkyXHU4ODRjXHU2OTljXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsXCIgc3R5bGU9XCJkaXNwbGF5OjtcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgXHU3OTNjXHU1NGMxXHU1NTQ2XHU1N2NlXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly96b25lLmh1b3hpYW4uY25cIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cInVybFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTcwNmJcdTdlYmZab25lXHU2MjgwXHU2NzJmXHU3OTNlXHU1MzNhXG4gICAgICAgIDwvYT4gPGRpdiBjbGFzcz1cInVybFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTU0MmNcdTcwNmIvXHU4OWMyXHU3MDZiXHU2MjgwXHU2NzJmXHU2Yzk5XHU5Zjk5XG4gICAgICAgIDwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTUxMmI3NDI1PjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTUxNzNcdTRlOGVcdTYyMTFcdTRlZWNcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgICAgICBcdTUxNmNcdTUzZjhcdTRlY2JcdTdlY2RcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgXHU1YmEyXHU2MjM3XHU2ODQ4XHU0ZjhiXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly93d3cuemhpcGluLmNvbS9nb25nc2lyLzY2MzEyYjA1MTc0ZTA2MjYzblI5MHRXX0ZRfn4uaHRtbFwiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsXCIgZGF0YS12LTUxMmI3NDI1Plx1NTJhMFx1NTE2NVx1NjIxMVx1NGVlYzwvYT48L2Rpdj4gPGRpdiBjbGFzcz1cImNvbHVtblwiIGRhdGEtdi01MTJiNzQyNT48ZGl2IGNsYXNzPVwibGFiZWxcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgXHU1MTczXHU2Y2U4XHU2MjExXHU0ZWVjXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwicXJDb2RlXCIgZGF0YS12LTUxMmI3NDI1PjxpbWcgc3JjPVwiL19udXh0L2ltZy9nb25nemhvbmdoYW8uMjgwOGFkMS5qcGdcIiBhbHQ9XCJcdTUxNmNcdTRmMTdcdTUzZjdcIiBjbGFzcz1cImdvbmd6aG9uZ2hhb1wiIGRhdGEtdi01MTJiNzQyNT4gPGRpdiBjbGFzcz1cImRlc2NcIiBkYXRhLXYtNTEyYjc0MjU+XG4gICAgICAgICAgICBcdTcwNmJcdTdlYmZcdTViODlcdTUxNjhcdTVlNzNcdTUzZjBcbiAgICAgICAgICA8L2Rpdj48L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImNvcHlyaWdodFwiIGRhdGEtdi01MTJiNzQyNT5cbiAgICAgIENvcHlyaWdodFx1MDBhOSAyMDIxIEh1b3hpYW4gQWxsIHJpZ2h0cyByZXNlcnZlZC4gPHNwYW4gZGF0YS12LTUxMmI3NDI1Plx1NGUyODwvc3Bhbj4gPGEgaHJlZj1cImh0dHBzOi8vYmVpYW4ubWlpdC5nb3YuY24vXCIgdGFyZ2V0PVwiX2JsYW5rXCIgZGF0YS12LTUxMmI3NDI1Plx1NGVhY0lDUFx1NTkwNzIwMDEzNjU5XHU1M2Y3LTI8L2E+IDxzcGFuIGRhdGEtdi01MTJiNzQyNT5cdTRlMjg8L3NwYW4+XHU1MzE3XHU0ZWFjXHU1Yjg5XHU1MTY4XHU1MTcxXHU4YmM2XHU3OWQxXHU2MjgwXHU2NzA5XHU5NjUwXHU1MTZjXHU1M2Y4XG4gICAgPC9kaXY+PC9kaXY+PC9mb290ZXI+IDxmb290ZXIgZGF0YS12LTEyNDIzOWFhIGRhdGEtdi03OWViOGMzZT48ZGl2IGNsYXNzPVwiZGVtby13YXJwXCIgZGF0YS12LTEyNDIzOWFhPjxkaXYgY2xhc3M9XCJjb250YWluZXIgZGVtby1jb250ZW50XCIgZGF0YS12LTEyNDIzOWFhPjxzcGFuIGRhdGEtdi0xMjQyMzlhYT5cdTc1MzFcdTc5M2VcdTUzM2FcdTRmMTdcdTU5MWFcdTViOWVcdTU0MGRcdTViODlcdTUxNjhcdTRlMTNcdTViYjZcdTRlMGVcdTgxZWFcdTUyYThcdTUzMTZcdTY3M2FcdTU2NjhcdTRlYmFcdTUzNGZcdTRmNWNcdTRlYTRcdTRlZDhcdTY2ZjRcdTlhZDhcdThkMjhcdTkxY2ZcdTc2ODRcdTZmMGZcdTZkMWVcdTZkNGJcdThiZDVcdTYyYTVcdTU0NGFcdWZmMDE8L3NwYW4+IDxkaXYgZGF0YS12LTEyNDIzOWFhPjxpbnB1dCB0eXBlPVwidGV4dFwiIHBsYWNlaG9sZGVyPVwiXHU4YmY3XHU4ZjkzXHU1MTY1XHU2MGE4XHU3Njg0XHU0ZjAxXHU0ZTFhXHU5MGFlXHU3YmIxXCIgdmFsdWU9XCJcIiBkYXRhLXYtMTI0MjM5YWE+IDxidXR0b24gZGF0YS12LTEyNDIzOWFhPlxuICAgICAgICAgIFx1OGJmN1x1NmM0Mlx1NmYxNFx1NzkzYVxuICAgICAgICA8L2J1dHRvbj48L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImNvbnRhaW5lclwiIGRhdGEtdi0xMjQyMzlhYT48ZGl2IGNsYXNzPVwidXJsLXdhcnBcIiBkYXRhLXYtMTI0MjM5YWE+PGRpdiBjbGFzcz1cImNvbHVtbiBsb2NhdGlvblwiIGRhdGEtdi0xMjQyMzlhYT48YSBocmVmPVwiL1wiIGFyaWEtY3VycmVudD1cInBhZ2VcIiBjbGFzcz1cIm51eHQtbGluay1leGFjdC1hY3RpdmUgbnV4dC1saW5rLWFjdGl2ZVwiIGRhdGEtdi0xMjQyMzlhYT48aW1nIHNyYz1cIi9fbnV4dC9pbWcvbG9nby5hYmI2N2U4LnBuZ1wiIGFsdD1cImxvZ29cIiBjbGFzcz1cImxvZ29cIiBkYXRhLXYtMTI0MjM5YWE+PC9hPiA8ZGl2IGNsYXNzPVwiZGVzY1wiIHN0eWxlPVwibWFyZ2luLXRvcDogOHB4O1wiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTkwYWVcdTdiYjFcdWZmMWFoaUBodW94aWFuLmNuXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTc1MzVcdThiZGRcdWZmMWE8YSBocmVmPVwidGVsOjAxMC04Mjc3MjY2MFwiIGRhdGEtdi0xMjQyMzlhYT4wMTAtODI3NzI2NjA8L2E+PGEgaHJlZj1cInRlbDoxOTkxMDM4Njc5N1wiIGRhdGEtdi0xMjQyMzlhYT4xOTkgMTAzOCA2Nzk3PC9hPjwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTYwM2JcdTkwZThcdWZmMWFcdTUzMTdcdTRlYWNcdTVlMDJcdTZkNzdcdTZkYzBcdTUzM2FcdTRlMGFcdTU3MzBcdTRlMWNcdThkZWYzNVx1NTNmN1x1OTg5MFx1NmNjOVx1NmM0N0NcdTVlYTczXHU1YzQyXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwiZGVzY1wiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTUyMDZcdTY1MmZcdTY3M2FcdTY3ODRcdWZmMWFcdTRlMGFcdTZkNzcgXHU2ZGYxXHU1NzMzXG4gICAgICAgIDwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTEyNDIzOWFhPjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTRlYTdcdTU0YzFcdTRlMGVcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTViODlcdTUxNjhcdTRmMTdcdTZkNGJcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgXHU0ZjAxXHU0ZTFhU1JDXHU2NzBkXHU1MmExXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly9kb25ndGFpLmlvL1wiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsXCIgZGF0YS12LTEyNDIzOWFhPlxuICAgICAgICAgIFx1NmQxZVx1NjAwMUlBU1RcbiAgICAgICAgPC9hPjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTEyNDIzOWFhPjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTc2N2RcdTVlM2RcdTY3MGRcdTUyYTFcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTk4NzlcdTc2ZWVcdTUyMTdcdTg4NjhcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgXHU2MzkyXHU4ODRjXHU2OTljXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwidXJsXCIgc3R5bGU9XCJkaXNwbGF5OjtcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgXHU3OTNjXHU1NGMxXHU1NTQ2XHU1N2NlXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly96b25lLmh1b3hpYW4uY25cIiB0YXJnZXQ9XCJfYmxhbmtcIiBjbGFzcz1cInVybFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTcwNmJcdTdlYmZab25lXHU2MjgwXHU2NzJmXHU3OTNlXHU1MzNhXG4gICAgICAgIDwvYT4gPGRpdiBjbGFzcz1cInVybFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTU0MmNcdTcwNmIvXHU4OWMyXHU3MDZiXHU2MjgwXHU2NzJmXHU2Yzk5XHU5Zjk5XG4gICAgICAgIDwvZGl2PjwvZGl2PiA8ZGl2IGNsYXNzPVwiY29sdW1uXCIgZGF0YS12LTEyNDIzOWFhPjxkaXYgY2xhc3M9XCJsYWJlbFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTUxNzNcdTRlOGVcdTYyMTFcdTRlZWNcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmwgdG9wLXVybFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgICAgICBcdTUxNmNcdTUzZjhcdTRlY2JcdTdlY2RcbiAgICAgICAgPC9kaXY+IDxkaXYgY2xhc3M9XCJ1cmxcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgXHU1YmEyXHU2MjM3XHU2ODQ4XHU0ZjhiXG4gICAgICAgIDwvZGl2PiA8YSBocmVmPVwiaHR0cHM6Ly93d3cuemhpcGluLmNvbS9nb25nc2lyLzY2MzEyYjA1MTc0ZTA2MjYzblI5MHRXX0ZRfn4uaHRtbFwiIHRhcmdldD1cIl9ibGFua1wiIGNsYXNzPVwidXJsXCIgZGF0YS12LTEyNDIzOWFhPlx1NTJhMFx1NTE2NVx1NjIxMVx1NGVlYzwvYT48L2Rpdj4gPGRpdiBjbGFzcz1cImNvbHVtblwiIGRhdGEtdi0xMjQyMzlhYT48ZGl2IGNsYXNzPVwibGFiZWxcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgXHU1MTczXHU2Y2U4XHU2MjExXHU0ZWVjXG4gICAgICAgIDwvZGl2PiA8ZGl2IGNsYXNzPVwicXJDb2RlXCIgZGF0YS12LTEyNDIzOWFhPjxpbWcgc3JjPVwiL19udXh0L2ltZy9nb25nemhvbmdoYW8uMjgwOGFkMS5qcGdcIiBhbHQ9XCJcdTUxNmNcdTRmMTdcdTUzZjdcIiBjbGFzcz1cImdvbmd6aG9uZ2hhb1wiIGRhdGEtdi0xMjQyMzlhYT4gPGRpdiBjbGFzcz1cImRlc2NcIiBkYXRhLXYtMTI0MjM5YWE+XG4gICAgICAgICAgICBcdTcwNmJcdTdlYmZcdTViODlcdTUxNjhcdTVlNzNcdTUzZjBcbiAgICAgICAgICA8L2Rpdj48L2Rpdj48L2Rpdj48L2Rpdj4gPGRpdiBjbGFzcz1cImNvcHlyaWdodFwiIGRhdGEtdi0xMjQyMzlhYT5cbiAgICAgIENvcHlyaWdodFx1MDBhOSAyMDIxIEh1b3hpYW4gQWxsIHJpZ2h0cyByZXNlcnZlZC4gPHNwYW4gZGF0YS12LTEyNDIzOWFhPlx1NGUyODwvc3Bhbj4gPGEgaHJlZj1cImh0dHBzOi8vYmVpYW4ubWlpdC5nb3YuY24vXCIgdGFyZ2V0PVwiX2JsYW5rXCIgZGF0YS12LTEyNDIzOWFhPlx1NGVhY0lDUFx1NTkwNzIwMDEzNjU5XHU1M2Y3LTI8L2E+IDxzcGFuIGRhdGEtdi0xMjQyMzlhYT5cdTRlMjg8L3NwYW4+XHU1MzE3XHU0ZWFjXHU1Yjg5XHU1MTY4XHU1MTcxXHU4YmM2XHU3OWQxXHU2MjgwXHU2NzA5XHU5NjUwXHU1MTZjXHU1M2Y4XG4gICAgPC9kaXY+PC9kaXY+PC9mb290ZXI+PC9kaXY+PC9kaXY+PC9kaXY+PHNjcmlwdD53aW5kb3cuX19OVVhUX189KGZ1bmN0aW9uKGEsYixjLGQpe3JldHVybiB7bGF5b3V0OlwiZGVmYXVsdFwiLGRhdGE6W3t9XSxmZXRjaDp7fSxlcnJvcjphLHN0YXRlOnthc3NldHM6e3JhbmdlT2JqOntyaWQ6YixyYW5nZU5hbWU6Yixhc3NldExpc3Q6W119LG15UmFuZ2VMaXN0OltdLGdyb3VwX2lkOmIsc2VsZWN0Q2hhcmFjdGVyaXN0aWNzOltdLGVkaXRNb2RlOmN9LGdsb2JhbDp7bWVudUV4cGFuZDpjfSxtZXNzYWdlOnt1bnJlYWRfY291bnQ6MH0scHJvamVjdDp7dHJlYXR5RGF0YTphLHByZWplY3RBdXRoRGF0YTphLHByZWplY3REZXZJbmZvOmF9LHRhY3RpYzp7dGFjdGljSWQ6YX0sdXNlcjp7dXNlcl9pbmZvOmEscm9sZTphLHVpZDphfSxjb25zdGFudHM6e30sbW9kdWxlczp7YXNzZXRzOnt9LGdsb2JhbDp7fSxtZXNzYWdlOnt9LHByb2plY3Q6e30sdGFjdGljOnt9LHVzZXI6e319fSxzZXJ2ZXJSZW5kZXJlZDpjLHJvdXRlUGF0aDpkLGNvbmZpZzp7X2FwcDp7YmFzZVBhdGg6ZCxhc3NldHNQYXRoOlwiXFx1MDAyRl9udXh0XFx1MDAyRlwiLGNkblVSTDphfX19fShudWxsLFwiXCIsdHJ1ZSxcIlxcdTAwMkZcIikpOzwvc2NyaXB0PjxzY3JpcHQgc3JjPVwiL19udXh0LzY1YmU1YzkuanNcIiBkZWZlcj48L3NjcmlwdD48c2NyaXB0IHNyYz1cIi9fbnV4dC81MDQ2Y2Y4LmpzXCIgZGVmZXI+PC9zY3JpcHQ+PHNjcmlwdCBzcmM9XCIvX251eHQvMDc3MjIyZC5qc1wiIGRlZmVyPjwvc2NyaXB0PjxzY3JpcHQgc3JjPVwiL19udXh0LzI4MWViMDAuanNcIiBkZWZlcj48L3NjcmlwdD5cbiAgPC9ib2R5PlxuPC9odG1sPlxuIl0sICJzdGF0dXMiOiAyMDEsICJtc2ciOiAic3VjY2VzcyJ9',
                'pool': [{
                    'invokeId':
                    1,
                    'interfaces': [],
                    'targetHash': [
                        '81fde3dd219fc46819a96215a8b9314d',
                        'f1e89d96383e80157092e587cd668ff7'
                    ],
                    'targetValues':
                    "('request_ssrf', (), {})",
                    'signature':
                    'django.urls.resolvers.RoutePattern.match',
                    'originClassName':
                    'django.urls.resolvers.RoutePattern',
                    'sourceValues':
                    "['demo/request_ssrf']",
                    'methodName':
                    'match',
                    'className':
                    'django.urls.resolvers.RoutePattern',
                    'source':
                    True,
                    'callerLineNumber':
                    52,
                    'callerClass':
                    '/usr/local/lib/python3.6/contextlib.py',
                    'args':
                    '',
                    'callerMethod':
                    'inner',
                    'sourceHash': ['eb29dbb23ed04efe9a1ee4a46b3091f9'],
                    'retClassName':
                    ''
                }, {
                    'invokeId': 2,
                    'interfaces': [],
                    'targetHash': ['1e4f4f034bc7db9189a287a08e7aeb9f'],
                    'targetValues': "('', (), {})",
                    'signature': 'django.urls.resolvers.RoutePattern.match',
                    'originClassName': 'django.urls.resolvers.RoutePattern',
                    'sourceValues': "['request_ssrf']",
                    'methodName': 'match',
                    'className': 'django.urls.resolvers.RoutePattern',
                    'source': True,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['f1e89d96383e80157092e587cd668ff7'],
                    'retClassName': ''
                }, {
                    'invokeId':
                    3,
                    'interfaces': [],
                    'targetHash': [
                        '81fde3dd219fc46819a96215a8b9314d',
                        '544c2f49e5bbec7222bac8d94c80a903'
                    ],
                    'targetValues':
                    "('request_ssrf', (), {})",
                    'signature':
                    'django.urls.resolvers.RoutePattern.match',
                    'originClassName':
                    'django.urls.resolvers.RoutePattern',
                    'sourceValues':
                    "['demo/request_ssrf']",
                    'methodName':
                    'match',
                    'className':
                    'django.urls.resolvers.RoutePattern',
                    'source':
                    True,
                    'callerLineNumber':
                    52,
                    'callerClass':
                    '/usr/local/lib/python3.6/contextlib.py',
                    'args':
                    '',
                    'callerMethod':
                    'inner',
                    'sourceHash': ['13a33bc615213cc78f27d4f8b549cab1'],
                    'retClassName':
                    ''
                }, {
                    'invokeId': 4,
                    'interfaces': [],
                    'targetHash': ['1e4f4f034bc7db9189a287a08e7aeb9f'],
                    'targetValues': "('', (), {})",
                    'signature': 'django.urls.resolvers.RoutePattern.match',
                    'originClassName': 'django.urls.resolvers.RoutePattern',
                    'sourceValues': "['request_ssrf']",
                    'methodName': 'match',
                    'className': 'django.urls.resolvers.RoutePattern',
                    'source': True,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['544c2f49e5bbec7222bac8d94c80a903'],
                    'retClassName': ''
                }, {
                    'invokeId':
                    5,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues':
                    'https://www.huoxian.cn/',
                    'signature':
                    'django.utils.datastructures.MultiValueDict.__getitem__',
                    'originClassName':
                    'django.utils.datastructures.MultiValueDict',
                    'sourceValues':
                    "[<QueryDict: {'_r': ['1711908589'], 'url': ['https://www.huoxian.cn/']}>, 'url']",
                    'methodName':
                    '__getitem__',
                    'className':
                    'django.utils.datastructures.MultiValueDict',
                    'source':
                    True,
                    'callerLineNumber':
                    52,
                    'callerClass':
                    '/usr/local/lib/python3.6/contextlib.py',
                    'args':
                    '',
                    'callerMethod':
                    'inner',
                    'sourceHash': [
                        '051621557d16a6a42691132712b3830c',
                        '39adfec6ad67f31ddc4cdfc2f5fd65e3',
                        '5940f283a115b256d9b6b62eef988eaa',
                        '54c5ce506b0d57c75ff9c815990b8469'
                    ],
                    'retClassName':
                    ''
                }, {
                    'invokeId': 6,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.__new__',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': '__new__',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 7,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.strip',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': 'strip',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 8,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.__new__',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': '__new__',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 9,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.strip',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': 'strip',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 10,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.__new__',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': '__new__',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 11,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.__new__',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': '__new__',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 12,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.__new__',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': '__new__',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 13,
                    'interfaces': [],
                    'targetHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.lstrip',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': 'lstrip',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 14,
                    'interfaces': [],
                    'targetHash': ['6309dbd7d72a9659e3ef7ac2a9e646c3'],
                    'targetValues': 'https://www.huoxian.cn/',
                    'signature': 'builtins.str.lower',
                    'originClassName': 'builtins.str',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': 'lower',
                    'className': 'builtins.str',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }, {
                    'invokeId': 15,
                    'interfaces': [],
                    'targetHash': ['6bb64f7d172107d28f38db1a23220217'],
                    'targetValues': '<Response [200]>',
                    'signature': 'requests.sessions.Session.request',
                    'originClassName': 'requests.sessions.Session',
                    'sourceValues': "['https://www.huoxian.cn/']",
                    'methodName': 'request',
                    'className': 'requests.sessions.Session',
                    'source': False,
                    'callerLineNumber': 52,
                    'callerClass': '/usr/local/lib/python3.6/contextlib.py',
                    'args': '',
                    'callerMethod': 'inner',
                    'sourceHash': ['5940f283a115b256d9b6b62eef988eaa'],
                    'retClassName': ''
                }]
            },
            'type': 36,
            'version': 'v2'
        }

        data = gzipdata(data)
        response = self.client.post(
            'http://testserver/api/v1/report/upload',
            data=data,
            HTTP_CONTENT_ENCODING='gzip',
            content_type='application/json',
        )
        assert MethodPool.objects.filter(
            url=
            'http://127.0.0.1:8004/demo/request_ssrf?_r=1711908589&url=https://www.huoxian.cn/?testinopenapi',
            agent_id=self.agent_id,
        ).exists() == True
        method_pool = MethodPool.objects.filter(
            url=
            'http://127.0.0.1:8004/demo/request_ssrf?_r=1711908589&url=https://www.huoxian.cn/?testinopenapi',
            agent_id=self.agent_id,
        ).first()
        assert method_pool.url == 'http://127.0.0.1:8004/demo/request_ssrf?_r=1711908589&url=https://www.huoxian.cn/?testinopenapi'
        assert response.status_code == 200
