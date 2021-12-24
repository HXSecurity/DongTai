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
            'reqHeader'] = "Q29udGVudC1UeXBlPWFwcGxpY2F0aW9uL2pzb24KWC1GcmFtZS1PcHRpb25zPURFTlkKQ29udGVudC1MZW5ndGg9NjYKQ29udGVudC1lbmNvZGluZz1nemlwClgtQ29udGVudC1UeXBlLU9wdGlvbnM9bm9zbmlmZgpSZWZlcnJlci1Qb2xpY3k9c2FtZS1vcmlnaW4="
        data['detail']['resBody'] = gzip_test_data = str(
            gzip.compress(bytes(testdata, encoding='utf-8')))
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
        assert MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231test",
            agent_id=self.agent_id,
            res_body=gzip_test_data).exists()
        assert not MethodPool.objects.filter(
            url="http://localhost:9999/sqli123132123313132321123231test",
            agent_id=self.agent_id,
            res_body=testdata).exists()
