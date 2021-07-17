import unittest

from test import DongTaiTestCase


class MyTestCase(DongTaiTestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_HttpRequest(self):
        from iast.views.vul_request_replay import HttpRequest
        raw_request = 'POST /system/role/list HTTP/1.1\nhost:localhost\nconnection:keep-alive\ncontent-length:125\nsec-ch-ua:\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"\naccept:application/json, text/javascript, */*; q=0.01\nx-requested-with:XMLHttpRequest\nsec-ch-ua-mobile:?0\nuser-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\ncontent-type:application/x-www-form-urlencoded\norigin:http://localhost\nsec-fetch-site:same-origin\nsec-fetch-mode:cors\nsec-fetch-dest:empty\nreferer:http://localhost/system/role\naccept-encoding:gzip, deflate, br\naccept-language:zh-CN,zh;q=0.9\ncookie:JSESSIONID=ec213e6e-ff23-42f6-b8f9-079eeb00d1a8\n\npageSize=10&pageNum=1&orderByColumn=roleSort&isAsc=asc&roleName=&roleKey=&status=&params[beginTime]=&params[endTime]='
        request = HttpRequest(raw_request)
        print(request)

    def test_split_request(self):
        raw_request = 'POST /system/role/list?name=123 HTTP/1.1\nhost:127.0.0.1:8002\nconnection:keep-alive\ncontent-length:125\nsec-ch-ua:\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"\naccept:application/json, text/javascript, */*; q=0.01\nx-requested-with:XMLHttpRequest\nsec-ch-ua-mobile:?0\nuser-agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36\ncontent-type:application/x-www-form-urlencoded\norigin:http://localhost\nsec-fetch-site:same-origin\nsec-fetch-mode:cors\nsec-fetch-dest:empty\nreferer:http://localhost/system/role\naccept-encoding:gzip, deflate, br\naccept-language:zh-CN,zh;q=0.9\ncookie:JSESSIONID=ec213e6e-ff23-42f6-b8f9-079eeb00d1a8\n\npageSize=10&pageNum=1&orderByColumn=roleSort&isAsc=asc&roleName=&roleKey=&status=&params[beginTime]=&params[endTime]='
        from iast.views.vul_request_replay import HttpRequest
        request = HttpRequest(raw_request)
        print(request.command)
        print(request.uri)
        print(request.request_version)
        print(request.headers.as_string().strip())
        print(request.params)
        print(request.body)


if __name__ == '__main__':
    unittest.main()
