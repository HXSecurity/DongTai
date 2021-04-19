#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/4/19 下午3:13
# project: dongtai-webapi
import requests


def notify(msg):
    requests.post(
        url='https://open.feishu.cn/open-apis/bot/hook/6b4275518b8b457784682a507bb86304',
        json={"title": "Maven官方爬虫", "text": msg}
    )
