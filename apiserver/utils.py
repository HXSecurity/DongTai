#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: owefsad@huoxian.cn
# datetime: 2021/6/1 上午9:53
# project: dongtai-openapi

# -*- coding: utf-8 -*-
import logging

import oss2
from oss2.exceptions import NoSuchKey

from AgentServer import settings

logger = logging.getLogger('dongtai.openapi')


class OssDownloader(object):
    BUCKET_URL = 'https://oss-cn-beijing.aliyuncs.com'
    BUCKET_NAME = 'dongtai'

    @staticmethod
    def download_file_to_path(access_key, access_key_secret, bucket_url, bucket_name, object_name, local_file):
        """

        :param access_key:
        :param access_key_secret:
        :param bucket_url:
        :param bucket_name:
        :param object_name:
        :param local_file:
        :return:
        """
        try:
            auth = oss2.Auth(access_key, access_key_secret)
            bucket = oss2.Bucket(auth, bucket_url, bucket_name)
            bucket.get_object_to_file(object_name, local_file)
            return True
        except NoSuchKey as e:
            # NoSuchKey表示oss云端文件不存在，通知管理员
            logger.error(f'oss download failure, reason: remote file not found, filename: {object_name}')
            return False
        except Exception as e:
            logger.error(f'oss download failure, reason: {e}')
            return False

    @staticmethod
    def download_file(object_name, local_file):
        return OssDownloader.download_file_to_path(access_key=settings.ACCESS_KEY,
                                                   access_key_secret=settings.ACCESS_KEY_SECRET,
                                                   bucket_url=OssDownloader.BUCKET_URL,
                                                   bucket_name=OssDownloader.BUCKET_NAME,
                                                   object_name=object_name,
                                                   local_file=local_file)
