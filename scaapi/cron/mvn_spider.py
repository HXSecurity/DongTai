#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/25 11:08
# software: PyCharm
# project: sca

import hashlib
import json
import logging
import re
import time
from queue import Queue

import requests
from peewee import IntegrityError

from scaapi.cron.database import MavenDb, MavenArtifact, ScaRecord
from scaapi.utils.common_log import logger

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')

PATTERN = re.compile('(.*?)href="(.*?)"(.*?)')


class MavenSpider():
    BASEURL = "https://repo1.maven.org/maven2/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    PROXIES = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
    INDEX = 0

    def __init__(self):
        self.status_array = self.restore_state()
        self.is_stop = len(self.status_array) > 0

    @staticmethod
    def calc_sha1(url):
        times = 0
        while True:
            try:
                if times > 3:
                    break
                resp = requests.get(
                    url,
                    headers=MavenSpider.HEADERS,
                    # proxies=MavenSpider.PROXIES
                )
                data = resp.content
                HASH = hashlib.sha1()
                HASH.update(data)
                return HASH.hexdigest()
            except Exception as e:
                times += 1
                pass

    @staticmethod
    def spider(url):
        try:
            logger.debug(f"开始爬取：{url}")
            time.sleep(1)
            resp = requests.get(
                url,
                headers=MavenSpider.HEADERS,
                # proxies=MavenSpider.PROXIES
            )
            hrefs = re.findall('(.*?)href="(.*?)"(.*?)', resp.text)
            return hrefs
        except Exception as e:
            logger.error(f'当前url: {url}, 错误信息：{e.__traceback__}')

    @staticmethod
    def filter(href):
        return href.endswith('../')

    @staticmethod
    def filter_file(href):
        return href.endswith('../') or href.endswith('/') is False or href.endswith('-sources.jar') or href.endswith(
            '-javadoc.jar')

    @staticmethod
    def notify(msg):
        requests.post(
            url='https://open.feishu.cn/open-apis/bot/hook/6b4275518b8b457784682a507bb86304',
            json={"title": "Maven官方爬虫", "text": msg}
        )

    @staticmethod
    def resume(url, item):
        if url.endswith('.jar'):
            return url.endswith(item)
        else:
            return url.endswith(item + '/')

    def cron(self, url, index):
        hrefs = self.spider(url)
        q = Queue()
        for href in hrefs:
            if self.filter(href[1]):
                continue
            href = url + href[1]
            if self.is_stop:
                if self.resume(href, self.status_array[index]):
                    if href.endswith(".jar"):
                        q.put(href)
                        self.is_stop = False
                    else:
                        self.cron(href, index + 1)
                else:
                    continue
            else:
                q.put(href)

            latest_package_path = ''
            while q.empty() is False:
                base_url = q.get()
                datas = list()
                if base_url.endswith('.jar') and base_url.endswith('-sources.jar') is False and base_url.endswith(
                        '-javadoc.jar') is False:
                    signature = self.calc_sha1(base_url)
                    url_token = base_url.replace(MavenSpider.BASEURL, '').split('/')
                    data = {
                        'package_name': url_token[-1],
                        'sha_1': signature,
                        'group_id': '.'.join(url_token[:-3]),
                        'atrifact_id': url_token[-3],
                        'version': url_token[-2],
                    }
                    datas.append(data)
                    logging.info(f'package: {base_url} data:{json.dumps(data)}')
                elif base_url.endswith("/"):
                    hrefs = self.spider(base_url)
                    if hrefs is None:
                        continue

                    for href in hrefs:
                        if href[1].endswith('.jar') and href[1].endswith('-sources.jar') is False and href[1].endswith(
                                '-javadoc.jar') is False:
                            signature = self.calc_sha1(base_url + href[1])
                            url_token = base_url.replace(MavenSpider.BASEURL, '').split('/')
                            data = {
                                'package_name': url_token[-1],
                                'sha_1': signature,
                                'group_id': '.'.join(url_token[:-3]),
                                'atrifact_id': url_token[-3],
                                'version': url_token[-2],
                            }
                            datas.append(data)
                            latest_package_path = base_url + href[1]
                            logging.info(f'package: {latest_package_path} data:{json.dumps(data)}')
                        elif self.filter_file(href[1]):
                            continue
                        else:
                            href = base_url + href[1]
                            q.put(href)
                    base_url = latest_package_path

                for data in datas:
                    try:
                        data['aql'] = f'maven:{data["group_id"]}:{data["atrifact_id"]}:{data["version"]}:'
                        maven, status = MavenDb.get_or_create(aql=data['aql'])
                        maven.group_id = data['group_id']
                        maven.atrifact_id = data['atrifact_id']
                        maven.sha_1 = data['sha_1']
                        maven.version = data['version']
                        maven.package_name = data['package_name']
                        maven.save()
                    except IntegrityError as e:
                        pass
                    except Exception as e:
                        logging.error(e)

                    # where 查询多条记录，插叙条件需要用
                    logger.info(f"{data['aql']} sign: {data['sha_1']}")
                    objs = MavenArtifact.select().where(
                        MavenArtifact.cph_version == data['aql']
                    )
                    for obj in objs:
                        obj.signature = data['sha_1']
                        obj.package_name = data['package_name']
                        obj.save()
                if datas:
                    MavenSpider.store_record(base_url)
        self.notify(f"{url}已爬取结束，深度：{index}")

    @staticmethod
    def restore_state():
        record = ScaRecord.get_or_none(type='maven')
        if record:
            logger.debug(f'恢复爬虫状态，历史位置：{record.data}')
            return record.data.replace(MavenSpider.BASEURL, '').split('/')
        else:
            logger.debug(f'爬虫状态恢复失败，从开始进行爬取')
            return []

    @staticmethod
    def store_record(url):
        record, status = ScaRecord.get_or_create(type='maven')
        record.data = url
        record.total = -1
        record.dt = int(time.time())
        record.save()


if __name__ == '__main__':
    spider = MavenSpider()
    try:
        spider.cron(MavenSpider.BASEURL, MavenSpider.INDEX)
    except Exception as e:
        spider.notify(f'maven爬虫出现异常，异常信息：{e}')
