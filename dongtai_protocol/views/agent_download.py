#!/usr/bin/env python
# datetime:2021/1/14 下午7:17
import json
import os
import re
import uuid
import logging

from django.http import FileResponse
from dongtai_common.endpoint import R, OpenApiEndPoint
from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from dongtai_common.common.utils import DepartmentTokenAuthentication

from dongtai_protocol.api_schema import DongTaiParameter
from dongtai_protocol.utils import OssDownloader
from dongtai_conf.settings import BUCKET_NAME_BASE_URL, VERSION

import shutil
import tarfile
import threading
import time

logger = logging.getLogger("dongtai.openapi")


class JavaAgentDownload:
    def __init__(self, user_id):
        t = threading.currentThread()
        self.user_id = user_id
        self.agent_file = "dongtai-agent.jar"
        self.original_agent_path = "/tmp/iast_cache/package"
        self.original_agent_file = f"/tmp/iast_cache/package/{self.agent_file}"
        self.user_target_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}"
        self.target_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}/iast_cache/package"
        self.remote_agent_file = (
            BUCKET_NAME_BASE_URL + "java/" + VERSION + "/dongtai-agent.jar"
        )
        if not os.path.exists(f"{self.target_path}"):
            os.makedirs(f"{self.target_path}")
        if not os.path.exists(self.original_agent_path):
            os.makedirs(self.original_agent_path)

    def download_agent(self):
        if os.path.exists(self.original_agent_file):
            return True
        return OssDownloader.download_file(
            object_name=self.remote_agent_file,
            local_file=f"{self.original_agent_file}",
        )

    def create_config(
        self,
        base_url,
        agent_token,
        auth_token,
        project_name,
        project_version,
        template_id,
    ):
        try:
            user_file = f"{self.target_path}/{self.agent_file}"
            if not os.path.exists(user_file):
                shutil.copyfile(self.original_agent_file, user_file)

            data = "iast.response.name=DongTai Iast\niast.server.url={url}\niast.server.token={token}\niast.allhook.enable=false\niast.dump.class.enable=false\niast.dump.class.path=/tmp/iast-class-dump/\niast.service.report.interval=30000\napp.name=DongTai\nengine.status=start\nengine.name={agent_token}\njdk.version={jdk_level}\nproject.name={project_name}\niast.proxy.enable=false\niast.proxy.host=\niast.proxy.port=\niast.server.mode=local\ndongtai.app.template={template_id}\nproject.version={project_version}\n"
            with open(f"{self.user_target_path}/iast.properties", "w") as config_file:
                config_file.write(
                    data.format(
                        url=base_url,
                        token=auth_token,
                        agent_token=agent_token,
                        jdk_level=1,
                        project_name=project_name,
                        template_id=template_id,
                        project_version=project_version,
                    )
                )
            return True
        except Exception as e:
            logger.error(
                _("Agent configuration file creation failed, reason: {E}").format(e)
            )
            return False

    def replace_config(self):
        user_file = f"{self.target_path}/{self.agent_file}"
        # 执行jar -uvf {JavaAgentDownload.LOCAL_AGENT_FILE} iast.properties更新jar包的文件
        import os

        os.system(  # nosec
            f"cd {self.user_target_path};zip -u {user_file} iast.properties"
        )
        # ignore because no userinput invoked here.


class PythonAgentDownload:
    def __init__(self, user_id):
        t = threading.currentThread()
        self.user_id = user_id
        self.agent_file = "dongtai_agent_python.tar.gz"
        self.original_agent_file = f"/tmp/{self.agent_file}"
        self.target_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}"
        self.target_source_path = (
            f"/tmp/{os.getpid()}-{t.ident}-{user_id}/dongtai_agent_python"
        )
        self.remote_agent_file = (
            BUCKET_NAME_BASE_URL + "python/dongtai_agent_python.tar.gz"
        )
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
        if not os.path.exists(self.target_source_path):
            os.makedirs(self.target_source_path)

    def download_agent(self):
        if os.path.exists(self.original_agent_file):
            return True
        return OssDownloader.download_file(
            object_name=self.remote_agent_file,
            local_file=f"{self.original_agent_file}",
        )

    def create_config(self, base_url, agent_token, auth_token, project_name, **kwargs):
        try:
            user_file = f"{self.target_path}/{self.agent_file}"
            if not AgentDownload.is_tar_file(self.original_agent_file):
                shutil.rmtree(self.original_agent_file)
                return False

            if not os.path.exists(user_file):
                shutil.copyfile(self.original_agent_file, user_file)
                shutil.copyfile(self.original_agent_file, f"{user_file}.bak")

            agent_file = tarfile.open(user_file)
            agent_file.extractall(path=self.target_path)  # nosec
            # trust upstream package until upstream provide file list to validate.
            names = agent_file.getnames()
            self.target_source_path = f"{self.target_path}/{names[0]}"
            config_path = ""
            for item in names:
                res = re.search("config.json", item)
                if res is not None:
                    config_path = item
                    break
            with open(f"{self.target_path}/{config_path}") as config_file:
                config = json.load(config_file)
                config["iast"]["server"]["token"] = auth_token
                config["iast"]["server"]["url"] = base_url
                config["project"]["name"] = project_name
                config["engine"]["name"] = agent_token
            with open(f"{self.target_path}/{config_path}", "w+") as config_file:
                json.dump(config, config_file)
            return True
        except Exception as e:
            print(type(e))
            print(e)
            return False

    def replace_config(self):
        user_file = f"{self.target_path}/{self.agent_file}"
        try:
            with tarfile.open(user_file, "w:gz") as tar:
                tar.add(
                    self.target_source_path,
                    arcname=os.path.basename(self.target_source_path),
                )
            return True
        except Exception as e:
            logger.error(f"replace config error: {e}")
            return False


class PhpAgentDownload:
    def __init__(self, user_id):
        t = threading.currentThread()
        self.user_id = user_id
        self.agent_file = "php-agent.tar.gz"
        self.original_agent_file = f"/tmp/{self.agent_file}"
        self.target_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}"
        self.target_source_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}/php-agent"
        self.remote_agent_file = BUCKET_NAME_BASE_URL + "php/php-agent.tar.gz"
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
        if not os.path.exists(self.target_source_path):
            os.makedirs(self.target_source_path)

    def download_agent(self):
        if os.path.exists(self.original_agent_file):
            return True
        return OssDownloader.download_file(
            object_name=self.remote_agent_file,
            local_file=f"{self.original_agent_file}",
        )

    def create_config(self, base_url, agent_token, auth_token, project_name, **kwargs):
        try:
            user_file = f"{self.target_path}/{self.agent_file}"
            if not AgentDownload.is_tar_file(self.original_agent_file):
                shutil.rmtree(self.original_agent_file)
                return False

            if not os.path.exists(user_file):
                shutil.copyfile(self.original_agent_file, user_file)
                shutil.copyfile(self.original_agent_file, f"{user_file}.bak")

            agent_file = tarfile.open(user_file)
            agent_file.extractall(path=self.target_path)  # nosec
            # trust upstream package until upstream provide file list to validate.
            agent_file.close()

            config_lines = []
            config_path = "dongtai-php-property.ini"
            with open(os.path.join(self.target_source_path, config_path), "rb") as fp:
                for line in fp.readlines():
                    try:
                        key, value = line.decode().split("=")
                    except ValueError:
                        continue
                    if key == "iast.server.url":
                        print(base_url)
                        value = base_url
                    if key == "iast.server.token":
                        value = auth_token
                    if key == "engine.name":
                        value = agent_token
                    if key == "project.name":
                        value = project_name
                    config_lines.append("=".join([key, value + "\n"]))
            with open(os.path.join(self.target_source_path, config_path), "w+") as fp:
                fp.writelines(config_lines)
            return True
        except Exception as e:
            logger.error(f"create config error: {e}")
            return False

    def replace_config(self):
        user_file = f"{self.target_path}/{self.agent_file}"
        try:
            with tarfile.open(user_file, "w:gz") as tar:
                tar.add(
                    self.target_source_path,
                    arcname=os.path.basename(self.target_source_path),
                )
            return True
        except Exception as e:
            logger.error(f"replace config error: {e}")
            return False


class GoAgentDownload:
    def __init__(self, user_id):
        t = threading.currentThread()
        self.user_id = user_id
        self.agent_file = "dongtai-go-agent-config.yaml"
        self.original_agent_file = f"/tmp/{self.agent_file}"
        self.target_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}"
        self.target_source_path = f"/tmp/{os.getpid()}-{t.ident}-{user_id}/php-agent"
        self.remote_agent_file = BUCKET_NAME_BASE_URL + "php/php-agent.tar.gz"
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)
        if not os.path.exists(self.target_source_path):
            os.makedirs(self.target_source_path)

    def download_agent(self):
        return True

    def create_config(self, base_url, agent_token, auth_token, project_name, **kwargs):
        with open(f"{self.target_path}/{self.agent_file}", "w") as fp:
            configs = [
                f'DongtaiGoOpenapi: "{base_url}"',
                f'DongtaiGoToken: "{auth_token}"',
                f'DongtaiGoProjectName: "{project_name}"',
                'DongtaiGoProjectVersion: "0.1.0"',
                "DongtaiGoProjectCreate: true",
                f'DongtaiGoAgentToken: "{agent_token}"',
            ]
            fp.writelines([config + "\n" for config in configs])
        return True

    def replace_config(self):
        return True


class AgentDownload(OpenApiEndPoint):
    """
    Agent 下载接口
    """

    name = "download_iast_agent"
    description = "下载洞态Agent"
    authentication_classes = (
        DepartmentTokenAuthentication,
        TokenAuthentication,
        SessionAuthentication,
    )

    @staticmethod
    def is_tar_file(file):
        tmp_path = f"/tmp/.dongtai_agent_test/{time.time_ns()}"
        try:
            agent_file = tarfile.open(file)
            agent_file.extractall(path=tmp_path)  # nosec
            # trust upstream package until upstream provide file list to validate.
        except tarfile.ReadError:
            return False
        finally:
            shutil.rmtree(tmp_path)
        return True

    def make_download_handler(self, language, user_id):
        if language == "python":
            return PythonAgentDownload(user_id)
        if language == "java":
            return JavaAgentDownload(user_id)
        if language == "php":
            return PhpAgentDownload(user_id)
        if language == "go":
            return GoAgentDownload(user_id)
        return None

    @extend_schema(
        operation_id="agent download api",
        tags=[_("Agent服务端交互协议")],
        summary="Agent 下载",
        parameters=[
            DongTaiParameter.OPENAPI_URL,
            DongTaiParameter.PROJECT_NAME,
            DongTaiParameter.PROJECT_VERSION,
            DongTaiParameter.TEMPLATE_ID,
            DongTaiParameter.DEPARTMENT_TOKEN,
            DongTaiParameter.LANGUAGE,
        ],
        responses=[FileResponse],
        methods=["GET"],
    )
    def get(self, request):
        try:
            base_url = request.query_params.get("url", "https://www.huoxian.cn")
            project_name = request.query_params.get("projectName", "Demo Project")
            project_version = request.query_params.get("projectVersion", "V1.0")
            language = request.query_params.get("language")
            department_token = request.query_params.get("department_token")
            template_id = request.query_params.get("template_id", 5)
            user_token = request.query_params.get("token", None)
            if department_token:
                final_token = department_token
            elif not user_token:
                token, success = Token.objects.get_or_create(user=request.user)
                final_token = token.key
            else:
                final_token = user_token
            agent_token = "".join(str(uuid.uuid4()).split("-"))

            handler = self.make_download_handler(language, request.user.id)

            if handler.download_agent() is False:
                return R.failure(
                    msg="agent file download failure. please contact official staff for help."
                )

            if handler.create_config(
                base_url=base_url,
                agent_token=agent_token,
                auth_token=final_token,
                project_name=project_name,
                project_version=project_version,
                template_id=template_id,
            ):
                handler.replace_config()
                with open(f"{handler.target_path}/{handler.agent_file}", "rb") as f:
                    response = FileResponse(f)
                    response["content_type"] = "application/octet-stream"
                    response[
                        "Content-Disposition"
                    ] = f"attachment; filename={handler.agent_file}"
                    return response
            return R.failure(msg="agent file not exit.")
        except Exception as e:
            logger.error(
                _("Agent download failed, user: {}, error details: {}").format(
                    request.user.get_username(), e
                ),
                exc_info=e,
            )
            return R.failure(msg="agent file not exit.")
        finally:
            try:
                shutil.rmtree(f"{handler.target_path}")
            except Exception as e:
                logger.info(e)
