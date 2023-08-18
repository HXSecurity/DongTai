import unittest
from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_HttpRequest(self):
        from dongtai_web.views.vul_request_replay import HttpRequest

        raw_request = (
            "POST /system/role/list HTTP/1.1\n"
            "host:localhost\n"
            "connection:keep-alive\n"
            "content-length:125\n"
            'sec-ch-ua:" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"\n'
            "accept:application/json, text/javascript, */*; q=0.01\n"
            "x-requested-with:XMLHttpRequest\n"
            "sec-ch-ua-mobile:?0\n"
            "user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\n"
            "content-type:application/x-www-form-urlencoded\n"
            "origin:http://localhost\n"
            "sec-fetch-site:same-origin\n"
            "sec-fetch-mode:cors\n"
            "sec-fetch-dest:empty\n"
            "referer:http://localhost/system/role\n"
            "accept-encoding:gzip, deflate, br\n"
            "accept-language:zh-CN,zh;q=0.9\n"
            "cookie:JSESSIONID=ec213e6e-ff23-42f6-b8f9-079eeb00d1a8\n\n"
            "pageSize=10&pageNum=1&orderByColumn=roleSort&isAsc=asc&roleName=&roleKey=&status=&"
            "params[beginTime]=&params[endTime]="
        )
        request = HttpRequest(raw_request)
        print(request)

    def test_split_request(self):
        raw_request = (
            "POST /system/role/list?name=123 HTTP/1.1\n"
            "host:127.0.0.1:8002\n"
            "connection:keep-alive\n"
            "content-length:125\n"
            'sec-ch-ua:" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"\n'
            "accept:application/json, text/javascript, */*; q=0.01\n"
            "x-requested-with:XMLHttpRequest\n"
            "sec-ch-ua-mobile:?0\n"
            "user-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\n"
            "content-type:application/x-www-form-urlencoded\n"
            "origin:http://localhost\n"
            "sec-fetch-site:same-origin\n"
            "sec-fetch-mode:cors\n"
            "sec-fetch-dest:empty\n"
            "referer:http://localhost/system/role\naccept-encoding:gzip, deflate, br\n"
            "accept-language:zh-CN,zh;q=0.9\n"
            "cookie:JSESSIONID=ec213e6e-ff23-42f6-b8f9-079eeb00d1a8\n\n"
            "pageSize=10&pageNum=1&orderByColumn=roleSort&isAsc=asc&roleName=&roleKey=&"
            "status=&params[beginTime]=&params[endTime]="
        )
        from dongtai_web.views.vul_request_replay import HttpRequest

        request = HttpRequest(raw_request)
        print(request.command)
        print(request.uri)
        print(request.request_version)
        print(request.headers.as_string().strip())
        print(request.params)
        print(request.body)


if __name__ == "__main__":
    unittest.main()
