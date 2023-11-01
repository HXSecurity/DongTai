import json
from time import time

from celery import shared_task
from celery.apps.worker import logger
from django.db.models import Q

from dongtai_common.models.agent import IastAgent
from dongtai_common.models.message import IastMessage, IastMessageType
from dongtai_common.models.profile import IastProfile
from dongtai_common.models.project import IastProject, ProjectStatus
from dongtai_common.models.user import User
from dongtai_engine.signals import send_notify

PROJECT_WARNING_TIME_KEY = "project_warning_time"
DEFAULT_PROJECT_WARNING_TIME = {"error_time": 2 * 7, "offline_time": 3 * 30}


def get_project_warning_time() -> dict[str, int]:
    profile = IastProfile.objects.filter(key=PROJECT_WARNING_TIME_KEY).values_list("value", flat=True).first()
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
        online_agent_count = IastAgent.objects.filter(bind_project=project, online=True).count()

        old_status = project.status

        if online_agent_count == 0:
            dt = int(time()) - project.last_has_online_agent_time
            project_warning_time = get_project_warning_time()
            error_time = project_warning_time["error_time"] * 60 * 60 * 24
            offline_time = project_warning_time["offline_time"] * 60 * 60 * 24

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
            send_notify.send_robust(sender=update_project_status, project_id=project.id)

            authed_user_ids = User.objects.filter(
                Q(deleted=False)
                & (
                    Q(is_global_permission=True)
                    | Q(iastprojectgroup__projects=project.id)
                    | Q(auth_projects=project.id)
                )
            ).values_list("id", flat=True)
            IastMessage.objects.bulk_create(
                IastMessage(
                    message=f"{project.name}】项目状态变更为【{ProjectStatus.names[project.status]}】",
                    relative_url=project.get_url(),
                    create_time=time(),
                    message_type=IastMessageType.objects.get(pk=2),
                    to_user_id=user_id,
                )
                for user_id in authed_user_ids
            )
            logger.info(f"update project status: {project} from {old_status} to {project.status}")

    logger.info("检测项目状态更新结束")
