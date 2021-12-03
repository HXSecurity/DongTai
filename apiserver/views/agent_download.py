#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/14 下午7:17
# software: PyCharm
# project: lingzhi-agent-server
import json
import os, re
import uuid, logging

from django.http import FileResponse
from dongtai.endpoint import OpenApiEndPoint, R
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

from apiserver.api_schema import DongTaiParameter, DongTaiAuth
from apiserver.utils import OssDownloader
from AgentServer.settings import BUCKET_NAME_BASE_URL
from configparser import ConfigParser

logger = logging.getLogger('dongtai.openapi')


class JavaAgentDownload():
    LOCAL_AGENT_PATH = '/tmp/iast_cache/package'
    LOCAL_AGENT_FILE = '/tmp/iast_cache/package/iast-agent.jar'
    REMOTE_AGENT_FILE = BUCKET_NAME_BASE_URL + 'java/iast-agent.jar'

    @staticmethod
    def download_agent():
        if not os.path.exists(JavaAgentDownload.LOCAL_AGENT_PATH):
            os.makedirs(JavaAgentDownload.LOCAL_AGENT_PATH)
        if os.path.exists(JavaAgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(
                object_name=JavaAgentDownload.REMOTE_AGENT_FILE, local_file=JavaAgentDownload.LOCAL_AGENT_FILE
            )

    @staticmethod
    def create_config(base_url, agent_token, auth_token, project_name):
        try:
            data = "iast.name=DongTai-Enterprise 1.0.0\niast.version=1.0.0\niast.response.name=DongTai Iast\niast.response.value=1.0.0\niast.server.url={url}\niast.server.token={token}\niast.allhook.enable=false\niast.dump.class.enable=false\niast.dump.class.path=/tmp/iast-class-dump/\niast.service.report.interval=30000\napp.name=DongTai\nengine.status=start\nengine.name={agent_token}\njdk.version={jdk_level}\nproject.name={project_name}\niast.proxy.enable=false\niast.proxy.host=\niast.proxy.port=\n"
            with open('/tmp/iast.properties', 'w') as config_file:
                config_file.write(
                    data.format(url=base_url, token=auth_token, agent_token=agent_token, jdk_level=1,
                                project_name=project_name)
                )
            return True
        except Exception as e:
            logger.error(_('Agent configuration file creation failed, reason: {E}').format(e))
            return False

    @staticmethod
    def replace_config():
        # 执行jar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties更新jar包的文件
        import os
        os.system(f'cd /tmp;jar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties')


class PythonAgentDownload():
    LOCAL_AGENT_FILE = '/tmp/dongtai_agent_python.tar.gz'
    LOCAL_AGENT_DIR = '/tmp/dongtai_agent_python'
    REMOTE_AGENT_FILE = BUCKET_NAME_BASE_URL + 'python/dongtai_agent_python.tar.gz'

    def __init__(self):
        import tarfile
        self.tarfile = tarfile

    @staticmethod
    def download_agent():
        if os.path.exists(PythonAgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(
                object_name=PythonAgentDownload.REMOTE_AGENT_FILE, local_file=PythonAgentDownload.LOCAL_AGENT_FILE
            )

    def create_config(self, base_url, agent_token, auth_token, project_name):
        try:
            agent_file = self.tarfile.open(PythonAgentDownload.LOCAL_AGENT_FILE)
            agent_file.extractall(path="/tmp/")
            names = agent_file.getnames()
            PythonAgentDownload.LOCAL_AGENT_DIR = "/tmp/" + names[0]
            config_path = ""
            for item in names:
                res = re.search("config.json", item)
                if res is not None:
                    config_path = item
                    break
            with open("/tmp/" + config_path, "r") as config_file:
                config = json.load(config_file)
                config['iast']['server']['token'] = auth_token
                config['iast']['server']['url'] = base_url
                config['project']['name'] = project_name
                config['engine']['name'] = agent_token
            with open("/tmp/" + config_path, "w+") as config_file:
                json.dump(config, config_file)
            return True
        except Exception as e:
            print(type(e))
            print(e)
            return False

    def replace_config(self):
        try:
            with self.tarfile.open(PythonAgentDownload.LOCAL_AGENT_FILE, "w:gz") as tar:
                tar.add(PythonAgentDownload.LOCAL_AGENT_DIR,
                        arcname=os.path.basename(PythonAgentDownload.LOCAL_AGENT_DIR))
            return True
        except Exception as e:
            logger.error(f'replace config error: {e}')
            return False


class PhpAgentDownload():
    LOCAL_AGENT_FILE = '/tmp/iast_cache/php-agent.tar.gz'
    LOCAL_AGENT_DIR = '/tmp/php'
    REMOTE_AGENT_FILE = BUCKET_NAME_BASE_URL + 'php/php-agent.tar.gz'

    def __init__(self):
        import tarfile
        self.tarfile = tarfile

    @staticmethod
    def download_agent():
        if os.path.exists(PhpAgentDownload.LOCAL_AGENT_FILE):
            return True
        else:
            return OssDownloader.download_file(
                object_name=PhpAgentDownload.REMOTE_AGENT_FILE, local_file=PhpAgentDownload.LOCAL_AGENT_FILE
            )

    def create_config(self, base_url, agent_token, auth_token, project_name):
        try:
            agent_file = self.tarfile.open(PhpAgentDownload.LOCAL_AGENT_FILE)
            agent_file.extractall(path="/tmp/php")
            config_lines = []
            config_path = "dongtai-php-property.ini"
            with open(os.path.join(PhpAgentDownload.LOCAL_AGENT_DIR, config_path), 'rb') as fp:
                for line in fp.readlines():
                    try:
                        key, value = line.decode().split('=')
                    except ValueError as e:
                        continue
                    if key == 'iast.server.url':
                        print(base_url)
                        value = base_url
                    if key == 'iast.server.token':
                        value = auth_token
                    if key == 'engine.name':
                        value = agent_token
                    if key == 'project.name':
                        value = project_name
                    config_lines.append("=".join([key, value + '\n']))
            with open(os.path.join(PhpAgentDownload.LOCAL_AGENT_DIR, config_path), 'w+') as fp:
                fp.writelines(config_lines)
            return True
        except Exception as e:
            logger.error(f'create config error: {e}')
            return False

    def replace_config(self):
        try:
            with self.tarfile.open(PhpAgentDownload.LOCAL_AGENT_FILE, "w:gz") as tar:
                tar.add(PhpAgentDownload.LOCAL_AGENT_DIR, arcname=os.path.basename(PhpAgentDownload.LOCAL_AGENT_DIR))
            return True
        except Exception as e:
            logger.error(f'replace config error: {e}')
            return False


class AgentDownload(OpenApiEndPoint):
    """
    当前用户详情
    """
    name = "download_iast_agent"
    description = "下载洞态Agent"
    DOWNLOAD_HANDLER = {
        'python': PythonAgentDownload(),
        'java': JavaAgentDownload(),
        'php': PhpAgentDownload(),
    }

    @extend_schema(
        parameters=[
            DongTaiParameter.OPENAPI_URL,
            DongTaiParameter.PROJECT_NAME,
            DongTaiParameter.LANGUAGE
        ],
        auth=[DongTaiAuth.TOKEN],
        responses=[FileResponse],
        methods=['GET']
    )
    def get(self, request):
        try:
            base_url = request.query_params.get('url', 'https://www.huoxian.cn')
            project_name = request.query_params.get('projectName', 'Demo Project')
            language = request.query_params.get('language')

            handler = self.DOWNLOAD_HANDLER[language]
            if handler.download_agent() is False:
                return R.failure(msg="agent file download failure. please contact official staff for help.")

            token, success = Token.objects.get_or_create(user=request.user)
            agent_token = ''.join(str(uuid.uuid4()).split('-'))
            if handler.create_config(base_url=base_url, agent_token=agent_token, auth_token=token.key,
                                     project_name=project_name):
                handler.replace_config()
                print(handler.LOCAL_AGENT_FILE)
                response = FileResponse(open(handler.LOCAL_AGENT_FILE, "rb"))
                response['content_type'] = 'application/octet-stream'
                response['Content-Disposition'] = "attachment; filename=agent.jar"
                return response
            else:
                return R.failure(msg="agent file not exit.")
        except Exception as e:
            raise e
            logger.error(
                _('Agent download failed, user: {}, error details: {}').format(
                    request.user.get_username()), e)
            return R.failure(msg="agent file not exit.")
