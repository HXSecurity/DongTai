######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : github_contributors
# @created     : Thursday Sep 16, 2021 10:52:20 CST
#
# @description :
######################################################################

import json
import logging
import time
from functools import partial
from urllib.parse import urljoin

import requests
from django.core.cache import cache

URL_LIST = [
    "https://api.github.com/repos/HXSecurity/DongTai-Doc-en/",
    "https://api.github.com/repos/HXSecurity/DongTai-Doc/",
    "https://api.github.com/repos/HXSecurity/DongTai-agent-java/",
    "https://api.github.com/repos/HXSecurity/DongTai/",
    "https://api.github.com/repos/HXSecurity/DongTai-Plugin-IDEA/",
    "https://api.github.com/repos/HXSecurity/vulhub-compose/",
    "https://api.github.com/repos/HXSecurity/DongTai-web/",
    "https://api.github.com/repos/HXSecurity/DongTai-webapi/",
    "https://api.github.com/repos/HXSecurity/DongTai-openapi/",
    "https://api.github.com/repos/HXSecurity/DongTai-engine/",
    "https://api.github.com/repos/HXSecurity/dongtai-core/",
    "https://api.github.com/repos/HXSecurity/Dongtai-Base-Image/",
]

logger = logging.getLogger("dongtai-dongtai_conf")


def _signed_state(dic: dict, state: int):
    dic["state"] = state
    return dic


def _change_dict_key(dic: dict, from_field: str, to_field: str):
    dic[to_field] = dic[from_field]
    del dic[from_field]
    return dic


def key_filiter(dic, keylist):
    new_dic = {}
    for key in keylist:
        new_dic[key] = dic[key]
    return new_dic


def _get_github_user(url_list=URL_LIST, suffix="pulls?state=all"):
    total_users = {}
    user_count = {}
    is_over_limit = False
    for url in url_list:
        resp = requests.get(urljoin(url, suffix))
        if resp.status_code == 403:
            is_over_limit = True
            break
        res = json.loads(resp.content)
        repo_users = [x["user"] for x in res]
        repo_users_dic = {_["id"]: _ for _ in repo_users}
        for user in repo_users:
            if user_count.get(user["id"], None):
                user_count[user["id"]] += 1
            else:
                user_count[user["id"]] = 1
        total_users.update(repo_users_dic)
    sorted_user_list = sorted(user_count.items(), key=lambda x: x[1], reverse=True)
    user_list = [total_users[user[0]] for user in sorted_user_list]
    return user_list, is_over_limit


_get_github_issues = partial(_get_github_user, suffix="issues?state=all")
_get_github_prs = partial(_get_github_user, suffix="pulls?state=all")


def get_github_contributors(dic=None, update=False):
    if dic is None:
        dic = {}
    if update:
        dic1 = {}
        dic1["issues"], is_over_limit_pr = _get_github_issues()
        dic1["prs"], is_over_limit_issue = _get_github_prs()
        dic1["time"] = int(time.time())
        if cache.get("github_contributors") is None or not any(
            [is_over_limit_pr, is_over_limit_issue]
        ):
            cache.set("github_contributors", dic1, 60 * 180)
    return cache.get("github_contributors", default={})
