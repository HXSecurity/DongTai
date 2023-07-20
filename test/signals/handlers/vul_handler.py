#!/usr/bin/env python
# -*- coding:utf-8 -*-
# datetime: 2021/5/6 上午11:35
import unittest

from test import DongTaiTestCase


class VulHandlerTest(DongTaiTestCase):
    def test_send_vul_notify(self):
        from dongtai_common.models.vulnerablity import IastVulnerabilityModel

        IastVulnerabilityModel.objects.filter(id=2208).first()

    def test_create_notify_config(self):
        web_hook_config = {
            "url": "https://open.feishu.cn/open-apis/bot/v2/hook/af91727f-7287-427e-8206-78f4e65d1fe5",
            "template": "url:{{url}}\n漏洞类型:{{vul_type}}\n账号:{{username}}\n项目:{{project}}",
        }
        import json
        from dongtai_common.models.notify_config import IastNotifyConfig

        IastNotifyConfig.objects.create(
            notify_type=IastNotifyConfig.WEB_HOOK,
            notify_meta_data=json.dumps(web_hook_config),
            user_id=18,
        )


if __name__ == "__main__":
    unittest.main()
