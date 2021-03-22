#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2020/8/24 18:41
# software: PyCharm
# project: SCA

"""
产品：snyk
查询站点：https://snyk.io/vuln
API接口：无，需要写爬虫提取页面数据
"""
from scaapi.cron.database import ScaVulDb
from scaapi.cron.mvn_spider import MavenSpider

"""
### https://snyk.io/vln/search

##### 漏洞库

- 漏洞页面地址：https://snyk.io/vuln/page/1

- 页码：1

- 每页：30条

##### 漏洞列表页面

漏洞名称：/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[1]/span/a/strong/text()

漏洞地址：/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[2]/strong/a/@href

组件名：/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[2]/strong/a/text()

包管理器类型：/html/body/div[1]/main/div[5]/div/table/tbody/tr[1]/td[3]/text()



##### 组件页面

最新版本：/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/a/text()

首次发布时间：/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/text()

最近更新时间：/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/text()

开源协议：/html/body/div[1]/main/div[3]/div[2]/div[2]/ul/li/span[1]/a/text()

漏洞.名称列表：/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[1]/span/a/strong/text()

漏洞.地址列表：/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[1]/span/a/@href

漏洞.版本列表：/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[2]/span/text() - 解析组件版本

组件 .名称列表：/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[1]/span[1]/text()

组件.更新时间列表：/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[2]/text()

组件.高危漏洞列表：/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[1]/span/text()

组件.中危漏洞数量：/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[2]/span/text()

组件.低危漏洞数量：/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[3]/span/text()



##### 漏洞页面

CVE编号：/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[2]/a/text()

CVE地址：/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[2]/a/@href

CWE编号：/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[3]/a/text()

CWE地址：/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[3]/a/@href

参考链接.名称：/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/ul/li[*]/a/text()

参考链接.地址：/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/ul/li[*]/a/@href

升级建议：/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/p[3]/text()

漏洞等级：/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div/div/header/div[2]/div/span/text()


#### 版本拆分
maven：
version：name以空格拆分，第一个为artifact，第二个为版本；atrifact以:拆分，第一个为groupId，第二个为artifactId；
漏洞版本：
- 以"),["进行分割：re.split('(.*?[\)\]]),(.*?)', '[4.2.0.RELEASE, 4.3.20.RELEASE),[5.0.0.RELEASE, 5.0.10.RELEASE),[5.1.0.RELEASE, 5.1.1.RELEASE)')
- 拆分之后，过滤掉其中的空数据，生成新的版本范围
- 根据左右括号构建判断条件：[ => 大于等于、( => 大于、] => 小于等于、) => 小于
- 解析括号内的版本列表：以","分割版本，如果为空则代表所有，
- 解析版本：re.findall("(.*\d+)\.","4.3.0.RELEASE")
"""
import json
import re
import sys
import time
import traceback
from copy import deepcopy
from urllib.parse import urljoin

import requests
from lxml.etree import HTML
from scaapi.utils.common_log import logger

BASEURL = "https://snyk.io/vuln/page/{page}?type=maven"
PAGE_SIZE = 30

VUL_LIST = {
    'vul_name': '/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[1]/span/a/strong/text()',
    'vul_href': '/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[1]/span/a/@href',
    'artifact_name': '/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[2]/strong/a/text()',
    'artifact_href': '/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[2]/strong/a/@href',
    'artifact_type': '/html/body/div[1]/main/div[5]/div/table/tbody/tr[*]/td[3]/text()',
}

ARTIFACT_LIST = {
    'name': [
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[1]/a[1]/text()',
        '/html/body/div[1]/main/div[7]/div/div/div/table/tbody/tr[*]/td[1]/a[1]/text()',
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[1]/text()'
    ],
    'dt': [
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[2]/text()',
        '/html/body/div[1]/main/div[7]/div/div/div/table/tbody/tr[*]/td[2]/text()'
    ],
    'high_count': [
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[1]/span/text()',
        '/html/body/div[1]/main/div[7]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[1]/span/text()'
    ],
    'middle_count': [
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[2]/span/text()',
        '/html/body/div[1]/main/div[7]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[2]/span/text()'
    ],
    'low_count': [
        '/html/body/div[1]/main/div[6]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[3]/span/text()',
        '/html/body/div[1]/main/div[7]/div/div/div/table/tbody/tr[*]/td[4]/ul/li[3]/span/text()'
    ],
}

ARTIFACT_VUL_LIST = {
    'name': [
        '/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[1]/span/a/strong/text()',
        '/html/body/div[1]/main/div[7]/div/table/tbody/tr[*]/td[1]/span/a/strong/text()'
    ],
    'href': [
        '/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[1]/span/a/@href',
        '/html/body/div[1]/main/div[7]/div/table/tbody/tr[*]/td[1]/span/a/@href'
    ],
    'version': [
        '/html/body/div[1]/main/div[6]/div/table/tbody/tr[*]/td[2]/span/text()',
        '/html/body/div[1]/main/div[7]/div/table/tbody/tr[*]/td[2]/span/text()'
    ],
}

ARTIFACT_DESC = {
    'latest_version': [
        '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/a/text()',
        '/html/body/div[1]/main/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/a/text()'
    ],
    'first_time': [
        '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/text()',
        '/html/body/div[1]/main/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/text()'
    ],
    'last_version': [
        '/html/body/div[1]/main/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/text()',
        '/html/body/div[1]/main/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/text()'
    ],
    'protocol': [
        '/html/body/div[1]/main/div[3]/div[2]/div[2]/ul/li/span[1]/a/text()',
        '/html/body/div[1]/main/div[4]/div[2]/div[2]/ul/li/span[1]/a/text()'
    ],
}

VUL_DESC = {
    'cve_id': '/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[2]/a/text()',
    'cve_href': '/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[2]/a/@href',
    'cwe_id': '/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[3]/a/text()',
    'cwe_href': '/html/body/div[1]/main/div[4]/div[2]/div/div[2]/div/dl/dd[3]/a/@href',
    'upgrade': '/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/p[3]/text()',
    'level': '/html/body/div[1]/main/div[4]/div[2]/div/div[1]/div/div/header/div[2]/div/span/text()',
}

VUL_REFERENCE_LIST = {
    'name': '/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/ul/li[*]/a/text()',
    'url': '/html/body/div[1]/main/div[4]/div[1]/div[2]/div/div/ul/li[*]/a/@href'
}

# npm; /html/body/div[1]/main/div[4]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td/a/text()

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36'
}


def spider(url, delay=None):
    times = 0
    delay_unit = 0.5
    text = None
    while True:
        try:
            if delay and isinstance(delay, int):
                time.sleep(delay)
            else:
                time.sleep(delay_unit * times)
            resp = requests.get(url, headers=HEADER, timeout=(30, 30))
            text = resp.text
            if text is not None:
                break
            else:
                times += 1
        except Exception as e:
            logger.error(f'当前url: {url}, 错误信息：{e.__traceback__}')
    return text


def convert_to_lxml(text):
    try:
        return HTML(text)
    except Exception as e:
        logger.error(f'转换html为lxml对象出错, 错误信息：{e.__traceback__}')


def not_empty(n):
    return bool(n.strip())


def xpath_parse(html, rules):
    # 从rules中提取key和value
    # key作为键，value作为xpath规则
    rule_values = deepcopy(rules)
    length = 0
    for key, value in rules.items():
        _value = list('')
        if isinstance(value, str):
            _value = html.xpath(value)
        elif isinstance(value, list):
            for __value in value:
                _value = html.xpath(__value)
                if _value:
                    break
        rule_values[key] = list(filter(not_empty, _value))
        if length == 0:
            length = len(rule_values[key])

    datas = [{} for i in range(length)]
    for key, values in rule_values.items():
        for i in range(length):
            try:
                datas[i][key] = str(values[i]).strip() if values else ''
            except Exception as e:
                datas[i][key] = ''
    return datas


def spider_page(page):
    url = BASEURL.format(page=page)
    text = spider(url)
    data = xpath_parse(convert_to_lxml(text), VUL_LIST)
    has_next = bool(len(data) == PAGE_SIZE)
    # 判断页面数量小于PAGE_SIZE，返回False
    return has_next, data


# fixme: 版本提取存在bug
def get_version_value(version):
    version = re.match('^(\d+\.)+\d+', version.strip()).group(0) if version.find('.') > -1 else version
    return version if version else '0'


def parse_lt_gt_condition(version):
    _left, _condition, _value = version[0] == '>', 0, 0

    if version[1] == '=':
        _condition = version[:2]
        _value = version[2:]
    else:
        _condition = version[0]
        _value = version[1:]
    return _left, _condition, _value


def parse_version(version):
    def remove_empty(version):
        return bool(version)

    if '[' in version or '(' in version:
        versions = list(filter(remove_empty, re.split('(.*?[\)\]]),(.*?)', version)))
    else:
        # fixme: 条件解析存在bug，版本条件复杂时，暂无法解析
        versions = list()
        if ' ' in version:
            _versions = version.split(' ')
            for _version in _versions:
                versions.extend(list(filter(remove_empty, re.split(',', _version))))
        else:
            versions = list(filter(remove_empty, re.split(',', version)))
    or_condition = list()
    for version in versions:
        if version[0] in ['[', '(']:
            version_left = get_version_value(version[1:version.index(',')])
            version_right = get_version_value(version[version.index(',') + 1:-1])
            if version[0] == '[':
                condition_left = '>='
            else:
                condition_left = '>'

            if version[-1] == ']':
                condition_right = '<='
            else:
                condition_right = '<'
            or_condition.append({
                'left_condition': condition_left,
                'left_value': version_left,
                'right_condition': condition_right,
                'right_value': version_right
            })
        elif version.strip() == '*':
            or_condition.append({
                'left_condition': '>',
                'left_value': '0',
                'right_condition': '<=',
                'right_value': '0'
            })
        elif version[0] in ['>', '<']:
            if ' ' in version:
                version_left = version[1:version.index(' ')]
                version_right = version[version.index(' ') + 1:-2]

                _left, _left_condition, _left_value = parse_lt_gt_condition(version_left)
                _left, _right_condition, _right_value = parse_lt_gt_condition(version_right)
                or_condition.append({
                    'left_condition': _left_condition,
                    'left_value': _left_value,
                    'right_condition': _right_condition,
                    'right_value': _right_value
                })
            else:
                _left, _condition, _value = parse_lt_gt_condition(version)
                if _left:
                    or_condition.append({
                        'left_condition': _condition,
                        'left_value': _value,
                        'right_condition': '<=',
                        'right_value': '0'
                    })
                else:
                    or_condition.append({
                        'left_condition': '>',
                        'left_value': '0',
                        'right_condition': _condition,
                        'right_value': _value
                    })
    return or_condition


def check_for_match(condition, version):
    left_match, right_match = False, False
    if condition['left_condition'] == '>=':
        left_match = version >= condition['left_value']
    elif condition['left_condition'] == '>':
        left_match = version > condition['left_value']

    if condition['right_condition'] == '<=':
        right_match = version <= condition['right_value'] if condition[
                                                                 'right_value'] != '0' else True
    elif condition['right_condition'] == '<':
        right_match = version < condition['right_value'] if condition[
                                                                'right_value'] != '0' else True
    return [left_match, right_match]


def spider_artifact(uri, build_tools):
    try:
        url = urljoin(BASEURL, uri)
        html = convert_to_lxml(spider(url))

        logger.info(f'开始解析{url}页面')
        data = xpath_parse(html, ARTIFACT_DESC)
        artifact_desc = data[0] if data else {}
        artifact_desc['url'] = url
        artifact_desc['vuls'] = xpath_parse(html, ARTIFACT_VUL_LIST)
        artifact_desc['versions'] = xpath_parse(html, ARTIFACT_LIST)
        # 解析版本信息
        for vul in artifact_desc['vuls']:
            data = spider_vuln(vul['href'])
            if data:
                vul.update(data)
            versions = parse_version(vul['version'])
            vul['version_condition'] = versions
            # 保存漏洞数据
            try:
                svd = ScaVulDb(
                    vul_name=vul['name'],
                    vul_level=vul['level'].split(' ')[0],
                    cve=vul['cve_id'],
                    cve_href=vul['cve_href'],
                    cwe=vul['cwe_id'],
                    cwe_href=vul['cwe_href'],
                    package_type=build_tools,
                    source='synkdb',
                    url=vul['url'],
                    version_range=vul['version'],
                    version_condition=json.dumps(vul['version_condition']),
                    extra=json.dumps(vul)
                )
                svd.save()
            except Exception as e:
                logger.error(e)

        # 检查组件与漏洞之间的关系
        for artiface_version in artifact_desc['versions']:
            # 解析artifact
            if build_tools == 'Maven':
                _temps = artiface_version['name'].split(' ')
                _version = _temps[1]
                _temps = _temps[0].split(':')
                _group_id = _temps[0]
                _artifact_id = _temps[1]
                artiface_version['group_id'] = _group_id
                artiface_version['artifact_id'] = _artifact_id
                artiface_version['version'] = _version
                artiface_version['aql'] = f'maven:{_group_id}:{_artifact_id}:{_version}:'
                # 解析maven数据
            elif build_tools == 'npm':
                _temps = artiface_version['name'].split(' ')
                _name = _temps[0]
                _version = _temps[1]
                artiface_version['package_name'] = _name
                artiface_version['version'] = _version
                artiface_version['aql'] = f'npm:{_name}:{_version}:'
            elif build_tools == 'Composer':
                pass
            elif build_tools == 'RubyGems':
                pass
            elif build_tools == 'pip':
                pass
            elif build_tools == 'cocoapods':
                pass
            elif build_tools == 'Go':
                pass
            # NuGet
            elif build_tools == 'NuGet':
                pass

            # if any([
            #     int(artiface_version['high_count']),
            #     int(artiface_version['middle_count']),
            #     int(artiface_version['low_count'])
            # ]):
            #     # 检查命中的漏洞
            #     if build_tools in ['Maven', 'npm']:
            #         for vul in artifact_desc['vuls']:
            #             for condition in vul['version_condition']:
            #                 if all(check_for_match(condition, artiface_version['version'])):
            #                     logger.info(
            #                         f'组件：{artiface_version["aql"]} 存在{vul["name"]}漏洞，cve: {vul.get("cve_id")} cwe: {vul.get("cwe_id")}')
            #     else:
            #         logger.info('unknown')
        return artifact_desc
    except Exception as e:
        traceback.print_exc(file=sys.stdout)


def spider_vuln(uri):
    try:
        url = urljoin(BASEURL, uri)
        html = convert_to_lxml(spider(url))
        data = xpath_parse(html, VUL_DESC)
        vul_desc = data[0] if data else {}
        vul_desc['url'] = url
        vul_desc['reference'] = xpath_parse(html, VUL_REFERENCE_LIST)
        return vul_desc
    except Exception as e:
        traceback.print_exc(file=sys.stdout)


def main():
    # 100
    page = 0
    while True:
        logger.info(f'开始爬取第{page}页的漏洞数据')
        has_next, vul_list = spider_page(page)
        for vul in vul_list:
            vul['atrifact'] = spider_artifact(vul['artifact_href'], vul['artifact_type'])
        if has_next:
            page += 1
        else:
            break
        # if page == total_page:
        #     break
    MavenSpider.notify(f"Snyk漏洞数据抓取完成，共{page}页")


def cron():
    main()


if __name__ == '__main__':
    main()
