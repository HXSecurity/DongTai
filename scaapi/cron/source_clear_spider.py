#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 18:40
# software: PyCharm
# project: SCA

"""
产品：SourceClear
查询站点：https://www.sourceclear.com/vulnerability-database/search#query=language:java%20type:vulnerability
API接口：https://api.sourceclear.com/catalog/search?q=language%3Ajava%20type:vulnerability&page=1
"""
import json
import time

import requests
from peewee import IntegrityError

from scaapi.cron.database import ArtifactDb, MavenArtifact, ScaRecord
from scaapi.cron.mvn_spider import MavenSpider
from scaapi.utils.common_log import logger


class SourceClearSpider():
    HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'
    }
    BASE_URL = 'https://api.sourceclear.com/catalog/search?q=language%3Ajava%20type:vulnerability&page={page}'

    def __init__(self):
        self.page = 66
        self.total_page = 96
        self.artifact_vuls = list()

    @staticmethod
    def spider(url):
        try:
            time.sleep(0.5)
            resp = requests.get(url, headers=SourceClearSpider.HEADER, timeout=(30, 30))
            return resp.json()
        except Exception as e:
            return None

    def set_total_page(self, total_page):
        logger.info(f'总页数：{total_page}')
        if self.total_page == -1:
            self.total_page = total_page

    def is_last_page(self):
        logger.info(f'当前第{self.page}页，共{self.total_page}页')
        if self.page == 1:
            return True
        else:
            self.page -= 1
            return False

    def parse_components(self, components, data, component_id):
        logger.info(f"开始解析组件数据，组件ID：{component_id}, 共{len(components)}条")
        reference_data = json.dumps(self.spider_links(component_id))
        for component in components:
            instances = list()
            artifact_data = dict()
            artifact_component_data = dict()
            artifact_component_data.update(data)
            artifact_component_data['group_id'] = component['coordOne']
            artifact_component_data['artifact_id'] = component['coordTwo']
            artifact_component_data['latest_version'] = component['componentLatestRelease']
            artifact_component_data['component_name'] = component['componentName']
            coord_hash = component['coordHash']
            version_ranges = component['versionRanges']

            for version_range in version_ranges:
                updateToVersion = version_range['updateToVersion']
                versionRange = version_range['versionRange']
                patch = version_range['patch'] if version_range['patch'] else ''
                componentInstances = version_range['componentInstances']

                for componentInstance in componentInstances:
                    cph_spilit = componentInstance['componentInstanceHash'].split(':')
                    instances.append({
                        'safe_version': updateToVersion,
                        'version_range': versionRange,
                        'patch': patch,
                        'cph_version': componentInstance['componentInstanceHash'],
                        'cph': coord_hash,
                        'type': cph_spilit[0],
                        'group_id': cph_spilit[1],
                        'artifact_id': cph_spilit[2],
                        'version': cph_spilit[3],
                    })

            artifact_component_data['reference'] = reference_data
            artifact_data['data'] = artifact_component_data
            artifact_data['artifacts'] = instances
            self.artifact_vuls.append(artifact_data)

    def parse(self, contents):
        index = 0
        for content in contents:
            index += 1
            logger.info(f"开始解析API数据，共{len(contents)}条，第{index}条")
            model = content['model']
            data = dict()
            cvss_score = model.get('nvdCvssScore')
            if cvss_score:
                pass
            else:
                cvss_score = model.get('srcclrCvssScore')

            cvss3_score = model.get('nvdCvss3Score')
            if cvss3_score:
                pass
            else:
                cvss3_score = model.get('srcclrCvss3Score')
            data['cvss_score'] = cvss_score
            data['cvss3_score'] = cvss3_score
            data['level'] = SourceClearSpider.calc_level(cvss_score, cvss3_score)
            data['cwe_id'] = model.get('cweId', '')
            data['cve_id'] = f"CVE-{model['cve']}" if model.get('cve', None) else ''
            data['stage'] = model['stage']
            data['title'] = model['title']
            data['overview'] = model.get('overview', '')
            data['teardown'] = model.get('teardown', '')
            # data['language'] = model['language'] # 解析语言
            components = model.get('artifactComponents', list())
            if components:
                self.parse_components(components, data, model.get("id"))

    def save(self):
        logger.info(f"开始保存结果，共{len(self.artifact_vuls)}条")
        for artifact_data in self.artifact_vuls:
            artifact = ArtifactDb.get_or_none(
                cve_id=artifact_data['data']['cve_id'],
                group_id=artifact_data['data']['group_id'],
                artifact_id=artifact_data['data']['artifact_id'],
                latest_version=artifact_data['data']['latest_version'],
            )
            if artifact:
                if bool(artifact.reference):
                    pass
                else:
                    artifact.reference = json.dumps(artifact_data['data']['reference'])
                if bool(artifact.cvss_score):
                    pass
                else:
                    artifact.cvss_score = artifact_data['data']['cvss_score']
                if bool(artifact.cvss3_score):
                    pass
                else:
                    artifact.cvss3_score = artifact_data['data']['cvss3_score']
                if bool(artifact.level):
                    pass
                else:
                    artifact.level = artifact_data['data']['level']
                artifact.save()
            else:
                artifact, status = ArtifactDb.get_or_create(**artifact_data['data'])
            aid = artifact.id

            for _artifact in artifact_data['artifacts']:
                _artifact['aid'] = aid

            try:
                for _artifact in artifact_data['artifacts']:
                    MavenArtifact.insert(_artifact).execute()
                # MavenArtifact.insert_many(artifact_data['artifacts']).execute()
            except IntegrityError as e:
                pass
            except Exception as e:
                logger.error(e)
                pass

    def get_data(self):
        logger.info(f'开始获取数据，模式：在线API接口，第{self.page}页')
        url = SourceClearSpider.BASE_URL.format(page=self.page)
        data = SourceClearSpider.spider(url)
        return data

    def get_data_from_file(self):
        logger.info(f'开始获取数据，模式：本地json文件，第{self.page}页')
        base_file = "assetdb/sourceclear-{page}.json"
        url = base_file.format(page=self.page)
        data = json.load(open(url, "r"))
        return data

    def run(self, local=False):
        self.recover()
        MavenSpider.notify(f"SourceClearSpider漏洞数据抓取开始，当前第{self.page}页，共{self.total_page}页")
        while True:
            if local:
                data = self.get_data_from_file()
            else:
                data = self.get_data()

            if data:
                self.parse(data['contents'])
                self.save()
                # 设置状态
                self.store_record(self.page, data['metadata']['totalPages'])

            if self.is_last_page():
                self.store_record(self.page - 1, data['metadata']['totalPages'])
                break
        MavenSpider.notify(f"SourceClearSpider漏洞数据抓取完成")

    def spider_links(self, component_id):
        """
        url = https://api.sourceclear.com/artifacts/components/3644
        :return:
        """

        def spider(url, timeout):
            time.sleep(0.5)
            try:
                resp = requests.get(url, headers=SourceClearSpider.HEADER, timeout=(30, 30))
                if resp.status_code == 200:
                    return resp.json()['artifactLinks']
            except:
                return None

        url = f'https://api.sourceclear.com/artifacts/components/{component_id}'
        times = 1
        time_stamp = 0.5
        data = []
        while True:
            data = spider(url, times * time_stamp)
            if data or times == 3:
                break
            else:
                logger.info(f"正在第{times}次重试，url: {url}")
                times += 1
        return data

    @classmethod
    def calc_level(cls, cvss, cvss3):
        if cvss3 == 0.0:
            return '无危害'
        elif cvss3 >= 0.1 and cvss3 <= 3.9:
            return '低危'
        elif cvss3 >= 4.0 and cvss3 <= 6.9:
            return '中危'
        elif cvss3 >= 7.0 and cvss3 <= 8.9:
            return '高危'
        elif cvss3 >= 9.0 and cvss3 <= 10.0:
            return '严重'
        else:
            return '无危害'

    def recover(self):
        record = ScaRecord.get_or_none(type='source.clear')
        if record:
            self.page = record.page
            self.total_page = record.total
            if self.page == 0:
                self.page = self.total_page

    def store_record(self, page, total):
        logger.info(f"开始维护爬虫状态，当前第{page}页，共{total}页")
        record, status = ScaRecord.get_or_create(type='source.clear')
        record.page = page
        record.total = total
        record.dt = int(time.time())
        record.save()


def cron():
    scs = SourceClearSpider()
    scs.run()


if __name__ == '__main__':
    cron()
    # scs = SourceClearSpider()
    # scs.run(local=True)
