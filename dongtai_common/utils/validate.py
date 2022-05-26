#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/7/16 下午2:25
# project: dongtai-engine


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
            except:
                return False
        return True

    @staticmethod
    def is_empty(obj):
        """
        Return True if obj is None or obj is ''
        :param obj:
        :return:
        """
        return obj is None or obj == ''
