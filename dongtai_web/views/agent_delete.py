#!/usr/bin/env python


import logging

from django.utils.translation import gettext_lazy as _

from dongtai_common.endpoint import R, UserEndPoint
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.agent_method_pool import MethodPool
from dongtai_common.models.asset import Asset
from dongtai_common.models.errorlog import IastErrorlog
from dongtai_common.models.heartbeat import IastHeartbeat
from dongtai_common.models.iast_overpower_user import IastOverpowerUserAuth
from dongtai_common.models.replay_method_pool import IastAgentMethodPoolReplay
from dongtai_common.models.replay_queue import IastReplayQueue
from dongtai_common.models.vulnerablity import IastVulnerabilityModel
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

logger = logging.getLogger("dongtai-webapi")

_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Agent and related data deleted successfully")), ""),
        ((202, _("Agent does not exist or no permission to access")), ""),
        ((202, _("Error while deleting, please try again later")), ""),
    )
)


class AgentDeleteEndPoint(UserEndPoint):
    name = "api-v1-agent-<pk>-delete"
    description = _("Delete Agent")

    @extend_schema_with_envcheck(
        tags=[_("Agent")],
        summary=_("Agent Delete"),
        description=_("Delete the agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request, pk=None):
        try:
            user = request.user
            queryset = IastAgent.objects.filter(user=user, id=pk).first()
            if queryset:
                self.agent = queryset
                self.delete_error_log()
                self.delete_heart_beat()
                self.delete_sca()
                self.delete_vul()
                self.delete_method_pool()
                self.delete_method_pool_replay()
                self.delete_replay_queue()
                self.agent.delete()

                return R.success(msg=_("Agent and related data deleted successfully"))
            return R.failure(msg=_("Agent does not exist or no permission to access"))
        except Exception as e:
            logger.exception(f"user_id:{request.user.id} msg: ", exc_info=e)
            return R.failure(msg=_("Error while deleting, please try again later"))

    def delete_error_log(self):
        try:
            deleted, _rows_count = IastErrorlog.objects.filter(agent=self.agent).delete()
            logger.error(_("Error logs deleted successfully, Deletion Amount: {}").format(deleted))
        except Exception as e:
            logger.exception(
                _("Failed to delete error logs, probe ID: {}, error message: ").format(self.agent.id),
                exc_info=e,
            )

    def delete_heart_beat(self):
        try:
            deleted, _rows_count = IastHeartbeat.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(_("Failed to delete heartbeat data, error message: "), exc_info=e)

    def delete_vul_overpower(self):
        try:
            deleted, _rows_count = IastOverpowerUserAuth.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(_("Failed to delete unauthorized data, error message: "), exc_info=e)

    def delete_vul(self):
        try:
            deleted, _rows_count = IastVulnerabilityModel.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(_("Failed to delete vulnerability data, error message:"), exc_info=e)

    def delete_sca(self):
        try:
            deleted, _rows_count = Asset.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(
                _("Failed to delete third-party component data, error message: "),
                exc_info=e,
            )

    def delete_method_pool(self):
        try:
            deleted, _rows_count = MethodPool.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(_("Failed to delete method pool data, error message: "), exc_info=e)

    def delete_method_pool_replay(self):
        try:
            deleted, _rows_count = IastAgentMethodPoolReplay.objects.filter(agent=self.agent).delete()
            logger.error(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.exception(
                _("Failed to delete replay request method pool data, error message: "),
                exc_info=e,
            )

    def delete_replay_queue(self):
        try:
            deleted, _rows_count = IastReplayQueue.objects.filter(agent=self.agent).delete()
            logger.error(_("Replay request queue deleted successfully, Deletion amount: {}").format(deleted))
        except Exception as e:
            logger.exception(_("Failed to delete replay request queue, error message: "), exc_info=e)


if __name__ == "__main__":
    MethodPool.objects.count()
    IastErrorlog.objects.count()
    IastHeartbeat.objects.count()
    IastOverpowerUserAuth.objects.count()
    Asset.objects.count()
    IastVulnerabilityModel.objects.count()
    MethodPool.objects.count()
