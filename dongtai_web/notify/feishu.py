#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# project: dongtai-webapi
import requests
from django.utils.translation import gettext_lazy as _


def notify(msg):
    requests.post(
        url="https://open.feishu.cn/open-apis/bot/hook/6b4275518b8b457784682a507bb86304",
        json={"title": _("Maven official crawler"), "text": msg},
    )
