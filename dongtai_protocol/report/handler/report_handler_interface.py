#!/usr/bin/env python
# datetime:2020/10/30 10:31
import logging
from typing import Optional

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dongtai_common.common.utils import cached_decorator
from dongtai_common.models.agent import IastAgent

logger = logging.getLogger("dongtai.openapi")


@cached_decorator(
    random_range=(60, 120), use_celery_update=False, cache_logic_none=False
)
def get_agent(agent_id, kwargs, fields):
    return (
        IastAgent.objects.filter(
            id=agent_id,
            **kwargs,
        )
        .only(*fields)
        .first()
    )


class IReportHandler:
    def __init__(self):
        self._report = None
        self._detail = None
        self._user_id = None
        self.agent_id = 0
        self.project_name = None
        self.agent: IastAgent = IastAgent()

    @property
    def report(self):
        return self._report

    @report.setter
    def report(self, reports):
        self._report = reports

    @property
    def detail(self):
        return self._detail

    @detail.setter
    def detail(self, detail):
        self._detail = detail

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    def common_header(self):
        self.detail = self.report.get("detail")
        self.agent_id = self.detail.get("agentId")

    def has_permission(self):
        self.agent = self.get_agent(agent_id=self.agent_id)
        logger.info(
            f"report_type : {self.report.get('type',0)} agent_id: {self.agent_id} has_permission: {'YES' if self.agent else 'No'}"
        )
        if not self.agent:
            return None
        return self.agent

    def parse(self):
        pass

    def save(self):
        pass

    def get_result(self, msg=None):
        return msg if msg else ""

    def handle(self, report, user):
        logger.info(_("[{}] Report resolution start").format(self.__class__.__name__))
        self.report = report
        self.user_id = user
        self.common_header()
        if self.has_permission():
            self.parse()
            self.save()
            logger.info(
                _("[{classname}] Report Analysis Completed").format(
                    classname=self.__class__.__name__
                )
            )
            return self.get_result()
        logger.info(
            _(
                "[{classname}] report resolution failed, Agent does not exist or no right to access, report data: {report}"
            ).format(classname=self.__class__.__name__, report=self.report)
        )
        return "no permission"

    def get_project_agents(self, agent):
        if agent.bind_project_id != 0:
            agents = IastAgent.objects.filter(
                Q(project_name=self.project_name)
                | Q(bind_project_id=agent.bind_project_id),
                online=1,
                user=self.user_id,
                project_version_id=agent.project_version_id,
            )
        else:
            agents = IastAgent.objects.filter(
                project_name=agent.project_name, user=self.user_id
            )
        return agents

    def get_agent(self, agent_id):
        return get_agent(
            agent_id,
            {
                "pk": agent_id,
                "online": 1,
                "user": self.user_id,
            },
            (
                "id",
                "bind_project_id",
                "project_version_id",
                "project_name",
                "language",
                "project_version_id",
                "server_id",
                "filepathsimhash",
                "servicetype",
            ),
        )
