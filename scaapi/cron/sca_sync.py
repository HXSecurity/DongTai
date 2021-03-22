#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/12/25 上午10:17
# software: PyCharm
# project: lingzhi-webapi
from iast.models.asset import Asset
from iast.models.sca_maven_artifact import ScaMavenArtifact
from iast.models.sca_vul_db import ScaVulDb
from iast.models.vul_level import IastVulLevel
from scaapi.cron.mvn_spider import MavenSpider
from scaapi.utils.common_log import logger


def sync():
    assets = Asset.objects.all()
    MavenSpider.notify(f"SCA组件漏洞同步开始，共{len(assets)}条数据待更新")
    for asset in assets:
        signature = asset.signature_value
        aids = ScaMavenArtifact.objects.filter(signature=signature).values("aid")
        vul_count = len(aids)
        levels = ScaVulDb.objects.filter(id__in=aids).values('vul_level')

        level = 'info'
        if len(levels) > 0:
            levels = [_['vul_level'] for _ in levels]
            if 'high' in levels:
                level = 'high'
            elif 'high' in levels:
                level = 'high'
            elif 'medium' in levels:
                level = 'medium'
            elif 'low' in levels:
                level = 'low'
            else:
                level = 'info'
        logger.debug(f'开始更新，sha1: {signature}，危害等级：{level}')
        asset.level = IastVulLevel.objects.get(name=level)
        asset.vul_count = vul_count
        asset.save()
    MavenSpider.notify(f"SCA组件漏洞同步结束")


if __name__ == '__main__':
    sync()
