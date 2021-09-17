######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : github_contributors
# @created     : Thursday Sep 16, 2021 10:52:20 CST
#
# @description :
######################################################################

import requests
from urllib.parse import urljoin
import json
from django.db import models
from rest_framework import serializers
import logging
from functools import partial
import time



URL_LIST = [
    'https://api.github.com/repos/HXSecurity/DongTai-Doc-en/',
    'https://api.github.com/repos/HXSecurity/DongTai-Doc/',
    'https://api.github.com/repos/HXSecurity/DongTai-agent-java/',
    'https://api.github.com/repos/HXSecurity/DongTai/',
    'https://api.github.com/repos/HXSecurity/DongTai-Plugin-IDEA/',
    'https://api.github.com/repos/HXSecurity/vulhub-compose/',
    'https://api.github.com/repos/HXSecurity/DongTai-web/',
    'https://api.github.com/repos/HXSecurity/DongTai-webapi/',
    'https://api.github.com/repos/HXSecurity/DongTai-openapi/',
    'https://api.github.com/repos/HXSecurity/DongTai-engine/',
    'https://api.github.com/repos/HXSecurity/dongtai-core/',
    'https://api.github.com/repos/HXSecurity/Dongtai-Base-Image/',
]

logger = logging.getLogger('dongtai-webapi')
def _signed_state(dic: dict, state: int):
    dic['state'] = state
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



def _get_github_user(url_list=URL_LIST, suffix='pulls?state=all'):

    total_users = {}
    user_count = {}
    for url in url_list:
        resp = requests.get(urljoin(url, suffix))
        if resp.status_code == 403:
            return {}
        res = json.loads(resp.content)
        repo_users = list(map(lambda x: x['user'], res))
        repo_users_dic = {_['id']: _ for _ in repo_users}
        for user in repo_users:
            if user_count.get(user['id'], None):
                user_count[user['id']] += 1
            else:
                user_count[user['id']] = 1
        total_users.update(repo_users_dic)
    sorted_user_list = sorted(user_count.items(),
                              key=lambda x: x[1],
                              reverse=True)
    user_list = []
    for user in sorted_user_list:
        user_list.append(total_users[user[0]])
    return user_list



_get_github_issues = partial(_get_github_user, suffix='issues?state=all')
_get_github_prs = partial(_get_github_user, suffix='pulls?state=all')



def get_github_contributors(dic={}, update=False):
    if update:
        dic['issues'] = _get_github_issues()
        dic['prs'] = _get_github_prs()
        dic['time'] = int(time.time())
    return dic
