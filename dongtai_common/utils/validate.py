#!/usr/bin/env python
# datetime: 2021/7/16 下午2:25


import hashlib
import os
from dataclasses import dataclass
from functools import reduce

from django.db.models import Q

from dongtai_common.models.profile import IastProfile
from dongtai_conf.settings import BASE_DIR


class Validate:
    """
    common Validate for dongtai project
    """

    @staticmethod
    def is_number(iterable):
        """
        Return True if x is int for all values x in the iterable.
        :param iterable:
        :return:
        """
        for item in iterable:
            try:
                int(item)
            except BaseException:
                return False
        return True

    @staticmethod
    def is_empty(obj):
        """
        Return True if obj is None or obj is ''
        :param obj:
        :return:
        """
        return obj is None or obj == ""


@dataclass
class FileHashPair:
    path: str
    sha1sum: str


def calculate_dir_sha() -> list[FileHashPair]:
    dic_list = []
    for path, dirs, files in os.walk(os.path.join(BASE_DIR, "static/data")):
        for file_ in sorted(files):
            fullpath = os.path.join(path, file_)
            sha = hashlib.sha1(usedforsecurity=False)
            with open(fullpath, "rb") as f:
                while True:
                    block = f.read(1)
                    if not block:
                        break
                    sha.update(block)
            dic = FileHashPair(
                path=fullpath,
                sha1sum=sha.hexdigest(),
            )
            dic_list.append(dic)
    return dic_list


def validate_hook_strategy_update() -> bool:
    filehashs = calculate_dir_sha()
    q_list = [Q(key=x.path, value=x.sha1sum) for x in filehashs]
    if not q_list:
        return False
    res = reduce(lambda x, y: x | y, q_list)
    if IastProfile.objects.filter(res).count() == len(filehashs):
        return True
    return False


def save_hook_stratefile_sha1sum() -> None:
    filehashs = calculate_dir_sha()
    for filehash in filehashs:
        IastProfile.objects.update_or_create(
            key=filehash.path,
            defaults={"value": filehash.sha1sum},
        )
