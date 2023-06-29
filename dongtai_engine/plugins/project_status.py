import json
from time import time

from celery import shared_task
from celery.apps.worker import logger

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.profile import IastProfile
from dongtai_common.models.project import IastProject, ProjectStatus


PROJECT_WARNING_TIME_KEY = "project_warning_time"
DEFAULT_PROJECT_WARNING_TIME = {"error_time": 2 * 7, "offline_time": 3 * 30}


def get_project_warning_time() -> dict[str, int]:
    profile = (
        IastProfile.objects.filter(key=PROJECT_WARNING_TIME_KEY)
        .values_list("value", flat=True)
        .first()
    )
    if profile is None:
        IastProfile(
            key=PROJECT_WARNING_TIME_KEY,
            value=json.dumps(DEFAULT_PROJECT_WARNING_TIME),
        ).save()
        return DEFAULT_PROJECT_WARNING_TIME
    return json.loads(profile)


@shared_task(queue="dongtai-periodic-task")
def update_project_status() -> None:
    logger.info("检测项目状态更新开始")
    for project in IastProject.objects.all():
        online_agent_count = IastAgent.objects.filter(
            bind_project=project, online=True
        ).count()

        old_status = project.status

        if online_agent_count == 0:
            if project.last_has_online_agent_time == -1:
                project.last_has_online_agent_time = int(time())
                project.save(update_fields=("last_has_online_agent_time"))
                continue

            dt = int(time()) - project.last_has_online_agent_time
            project_warning_time = get_project_warning_time()
            error_time = project_warning_time["error_time"]
            offline_time = project_warning_time["offline_time"]

            if dt < error_time:
                project.status = ProjectStatus.NORMAL
                project.save(update_fields=("status",))
            elif dt < offline_time:
                project.status = ProjectStatus.ERROR
                project.save(update_fields=("status",))
            else:
                project.status = ProjectStatus.OFFLINE
                project.save(update_fields=("status",))
        else:
            project.last_has_online_agent_time = int(time())
            project.status = ProjectStatus.NORMAL
            project.save(update_fields=("status", "last_has_online_agent_time"))

        if old_status != project.status:
            logger.info(
                "update project status: "
                f"{project} from {old_status} to {project.status}"
            )

    logger.info("检测项目状态更新结束")
