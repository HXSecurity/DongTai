from rest_framework.test import APITestCase
import json

data1 = {
    "vul_name":
    "/vulns/002-file-read.jsp 路径穿越",
    "detail":
    "test",
    "vul_level":
    "HIGH",
    "urls": [
        "http://192.168.0.64:8080/vulns/002-file-read.jsp",
        "http://192.168.0.64:8080/vulns/002-file-read.jsp"
    ],
    "payload":
    "string",
    "create_time":
    2147483647,
    "vul_type":
    "路径穿越",
    "request_messages": [{
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:\n"
    }, {
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false\n\n"
    }],
    "dt_uuid_id": ["213123123122312312312313"],
    "dongtai_vul_type": ["string"],
    "dast_tag":
    "test",
    "agent_id": ["1"],
    "target":
    "http://192.168.0.64:8080/"
}

data2 = {
    "vul_name":
    "/vulns/002-file-read.jsp 路径穿越",
    "detail":
    "test",
    "vul_level":
    "HIGH",
    "urls": [
        "http://192.168.0.64:8080/vulns/002-file-read.jsp",
        1,
    ],
    "payload":
    111,
    "create_time":
    2147483647,
    "vul_type":
    "路径穿越",
    "request_messages": [{
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
    }, {
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false\n\n"
    }],
    "dongtai_vul_type": ["string"],
    "target":
    "http://192.168.0.64:8080/"
}

data3 = {
    "vul_name":
    "/vulns/002-file-read.jsp 路径穿越",
    "detail":
    "test",
    "vul_level":
    "HIGH",
    "urls": [
        "http://192.168.0.64:8080/vulns/002-file-read.jsp",
        "http://192.168.0.64:8080/vulns/002-file-read.jsp"
    ],
    "payload":
    "string",
    "create_time":
    2147483647,
    "vul_type":
    "路径穿越",
    "request_messages": [{
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:\n"
    }, {
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false\n\n"
    }],
    "dt_uuid_id": ["213123123122312312312313"],
    "dongtai_vul_type": ["string"],
    "dast_tag":
    "test",
    "agent_id": [],
    "target":
    "http://192.168.0.64:8080/"
}

data4 = {
    "vul_name":
    "/vulns/002-file-read.jsp 路径穿越",
    "detail":
    "",
    "vul_level":
    "HIGH",
    "urls": [
        "http://192.168.0.64:8080/vulns/002-file-read.jsp",
        "http://192.168.0.64:8080/vulns/002-file-read.jsp"
    ],
    "payload":
    "",
    "create_time":
    2147483647,
    "vul_type":
    "路径穿越",
    "request_messages": [{
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:\n"
    }, {
        "request":
        "GET /vulns/002-file-read.jsp?file=..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fpasswd HTTP/1.1\r\nHost: 192.168.0.64:8080\r\nUser-Agent: Xray_Test\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2\r\nCookie: JSESSIONID=86F07EDEF41475ADB61064DE440DD395; DTCsrfToken=UzfLT62TGKeJKgNxfNcyoOjEVh124WV3Fl8arbOGzUZDllACTaBOWlin6cRImHt7\r\nDt-Dast: Xray\r\nReferer: http://192.168.0.64:8080/vulns/002-file-read.jsp\r\nUpgrade-Insecure-Requests: 1\r\nXray: x\r\nAccept-Encoding: gzip\r\n\r\n",
        "response":
        "HTTP/1.1 200 \r\nContent-Length: 5099\r\nContent-Type: text/html;charset=UTF-8\r\nDate: Sat, 18 Mar 2023 07:49:52 GMT\r\nDongtai: v1.9.0-beta1\r\nDt-Request-Id: 23.0794e3c3f73c4c14880b4896ce63b9ec\r\nSet-Cookie: JSESSIONID=7177BD5F10CECCED16BF3745D2CDF6B5; Path=/vulns; HttpOnly\r\n\r\n\n\n\n\n\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\n    <title>002 任意文件下载/读取漏洞</title>\n</head>\n<body>\n<h1>002 - 任意文件下载/读取漏洞（路径拼接）</h1>\n<p>正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=example.pdf\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../../../../../../../../../../../../../etc/passwd\n</a>'</p>\n\n<p>不正常调用: </p>\n<p>curl '<a href=\"http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\"\n            target=\"_blank\">http://192.168.0.64:8080/vulns/002-file-read.jsp?file=../../../conf/tomcat-users.xml\n</a>'</p>\n\n<br>\n<p>读取内容</p>\n<pre>root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nadm:x:3:4:adm:/var/adm:/sbin/nologin\nlp:x:4:7:lp:/var/spool/lpd:/sbin/nologin\nsync:x:5:0:sync:/sbin:/bin/sync\nshutdown:x:6:0:shutdown:/sbin:/sbin/shutdown\nhalt:x:7:0:halt:/sbin:/sbin/halt\nmail:x:8:12:mail:/var/spool/mail:/sbin/nologin\noperator:x:11:0:operator:/root:/sbin/nologin\ngames:x:12:100:games:/usr/games:/sbin/nologin\nftp:x:14:50:FTP User:/var/ftp:/sbin/nologin\nnobody:x:99:99:Nobody:/:/sbin/nologin\nsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologin\ndbus:x:81:81:System message bus:/:/sbin/nologin\npolkitd:x:999:997:User for polkitd:/:/sbin/nologin\nmysql:x:27:27:MySQL Server:/var/lib/mysql:/bin/false\n\n"
    }],
    "dt_uuid_id": ["213123123122312312312313"],
    "dongtai_vul_type": ["string"],
    "dast_tag":
    "test",
    "agent_id": ["1"],
    "target":
    "http://192.168.0.64:8080/"
}

class DastWebhookTestCase(APITestCase):

    def setUp(self):
        from dongtai_conf.settings import DAST_TOKEN
        self.client.credentials(
            HTTP_X_DONGTAI_DAST_VUL_API_AUTHORIZATION=DAST_TOKEN)

    def test_positive_push_201_1(self):
        res = self.client.post('/api/v1/dast_webhook',
                               json.dumps(data1),
                               content_type="application/json")
        self.assertEqual(res.status_code, 201)
    
    def test_positive_push_201_2(self):
        res = self.client.post('/api/v1/dast_webhook',
                               json.dumps(data4),
                               content_type="application/json")
        self.assertEqual(res.status_code, 201)

    def test_nagetive_push_422(self):
        res = self.client.post('/api/v1/dast_webhook',
                               json.dumps(data2),
                               content_type="application/json")
        self.assertEqual(res.status_code, 422)
        print(json.loads(res.content))
        pass

    def test_nagetive_push_412(self):
        res = self.client.post('/api/v1/dast_webhook',
                               json.dumps(data3),
                               content_type="application/json")
        self.assertEqual(res.status_code, 412)
        pass

    def tearDown(self):
        pass
