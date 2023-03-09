from rest_framework.test import APITestCase
from io import StringIO
from unittest.mock import patch
from dongtai_web.xray.webhook import (
    parse_xray_uuid,
    parse_agent_id,
)

class AgentTestCase(APITestCase):

    def setUp(self):
        pass

    def test_web_vuln(self):
        data = {
            "data": {
                "create_time": 1678090808860,
                "detail": {
                    "addr":
                    "http://testphp.vulnweb.com/userinfo.php",
                    "extra": {
                        "avg_time": "193",
                        "n_time": "2190",
                        "p_time": "210",
                        "param": {
                            "key":
                            "pass",
                            "position":
                            "body",
                            "value":
                            "123'and(select*from(select+sleep(2))a/**/union/**/select+1)='"
                        },
                        "sleep_time": "2000",
                        "stat":
                        "{\"normal\":{\"samples\":[191,192,214,191,187,188],\"avg\":193.83333333333334,\"std_dev\":9.190877119308157,\"sleep_time\":2},\"sleep_0_time\":210,\"quick_check\":{\"samples\":[2190],\"sleep\":2},\"verify\":{\"samples\":[3201,3195,3224],\"sleep\":3}}",
                        "std_dev": "9",
                        "title": "Generic MySQL time based case ['string']",
                        "type": "time_based"
                    },
                    "payload":
                    "123'and(select*from(select+sleep(2))a/**/union/**/select+1)='",
                    "snapshot":
                    [[
                        "POST /userinfo.php HTTP/1.1\r\nHost: testphp.vulnweb.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0\r\nContent-Length: 116\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nContent-Type: application/x-www-form-urlencoded\r\nOrigin: http://testphp.vulnweb.com\r\nReferer: http://testphp.vulnweb.com/login.php\r\nUpgrade-Insecure-Requests: 1\r\nAccept-Encoding: gzip\r\n\r\npass=123%27and%28select%2Afrom%28select%2Bsleep%280%29%29a%2F%2A%2A%2Funion%2F%2A%2A%2Fselect%2B1%29%3D%27&uname=123",
                        "HTTP/1.1 302 Found\r\nConnection: keep-alive\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 06 Mar 2023 08:20:06 GMT\r\nLocation: login.php\r\nServer: nginx/1.19.0\r\nX-Powered-By: PHP/5.6.40-38+ubuntu20.04.1+deb.sury.org+1\r\n\r\n"
                    ],
                     [
                         "POST /userinfo.php HTTP/1.1\r\nHost: testphp.vulnweb.com\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0\r\nContent-Length: 116\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nContent-Type: application/x-www-form-urlencoded\r\nOrigin: http://testphp.vulnweb.com\r\nReferer: http://testphp.vulnweb.com/login.php\r\nUpgrade-Insecure-Requests: 1\r\nAccept-Encoding: gzip\r\n\r\npass=123%27and%28select%2Afrom%28select%2Bsleep%282%29%29a%2F%2A%2A%2Funion%2F%2A%2A%2Fselect%2B1%29%3D%27&uname=123",
                         "HTTP/1.1 302 Found\r\nConnection: keep-alive\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 06 Mar 2023 08:20:08 GMT\r\nLocation: login.php\r\nServer: nginx/1.19.0\r\nX-Powered-By: PHP/5.6.40-38+ubuntu20.04.1+deb.sury.org+1\r\n\r\n"
                     ]]
                },
                "plugin": "sqldet/blind-based/default",
                "target": {
                    "params": [{
                        "path": ["pass"],
                        "position": "body"
                    }],
                    "url": "http://testphp.vulnweb.com/userinfo.php"
                }
            },
            "type": "web_vuln"
        }
        res = self.client.post('/api/v1/xray_webhook', data, format='json')
        print(res)

    def test_web_statistic(self):
        data = {
            "data": {
                "average_response_time": 0,
                "num_found_urls": 27,
                "num_scanned_urls": 27,
                "num_sent_http_requests": 5234,
                "ratio_failed_http_requests": 0.006113871,
                "ratio_progress": 0
            },
            "type": "web_statistic"
        }
        with self.assertLogs('dongtai-webapi', level='DEBUG') as cm:
            res = self.client.post('/api/v1/xray_webhook', data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(any((str(data) in i for i in cm.output)))

    def test_parse_xray_uuid(self):
        data = """HTTP/1.1 302 Found\r\nConnection: keep-alive\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 06 Mar 2023 08:20:06 GMT\r\nLocation: login.php\r\nServer: nginx/1.19.0\r\nXray: sadadasdadadddassd\r\nX-Powered-By: PHP/5.6.40-38+ubuntu20.04.1+deb.sury.org+1\r\n\r\n"""
        header = parse_xray_uuid(data)
        self.assertEqual(header, "sadadasdadadddassd")
        pass
    
    def test_parse_agent_id(self):
        data = """HTTP/1.1 302 Found\r\nConnection: keep-alive\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 06 Mar 2023 08:20:06 GMT\r\nLocation: login.php\r\nServer: nginx/1.19.0\r\nAgentId: 1\r\nX-Powered-By: PHP/5.6.40-38+ubuntu20.04.1+deb.sury.org+1\r\n\r\n"""
        header = parse_agent_id(data)
        self.assertEqual(header, "1")
        pass
