#!/usr/bin/env python

import logging

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

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


class AgentDeleteQuerysSerializer(serializers.Serializer):
    ids = serializers.CharField(
        help_text=_('The id corresponding to the agent, use"," for segmentation.')
    )


_ResponseSerializer = get_response_serializer(
    status_msg_keypair=(
        ((201, _("Deleted Successfully")), ""),
        ((201, _("Deletion failed")), ""),
        ((201, _("Successfully deleted {} strips, failed to deleted {} strips")), ""),
    )
)


class AgentsDeleteEndPoint(UserEndPoint):
    name = "api-v1-agent-<pk>-delete"
    description = _("Delete Agent")

    @extend_schema_with_envcheck(
        [AgentDeleteQuerysSerializer],
        tags=[_("Agent")],
        summary=_("Agent Delete batch"),
        description=_("Stop the running agent by specifying the id."),
        response_schema=_ResponseSerializer,
    )
    def get(self, request):
        agent_ids = request.GET.get("ids")
        try:
            agent_ids = [int(i) for i in agent_ids.split(",")]
        except Exception:
            return R.failure("agent_ids should able to numeric")
        result = []
        for pk in agent_ids:
            try:
                user = request.user
                queryset = IastAgent.objects.filter(user=user, pk=pk).first()
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
                    result.append(True)
                else:
                    result.append(False)
                    pass
            except Exception as e:
                result.append(False)
                logger.warning(f"user_id:{request.user.id} msg:{e}")
        success = list(filter(lambda x: x is True, result))
        failure = list(filter(lambda x: x is False, result))
        if len(success) == len(agent_ids):
            return R.success(msg=_("Deleted Successfully"))
        if len(failure) == len(agent_ids):
            return R.success(msg=_("Deletion failed"))
        return R.success(
            msg=_("Successfully deleted {} strips, failed to deleted {} strips").format(
                len(success), len(failure)
            )
        )

    def delete_error_log(self):
        try:
            deleted, _rows_count = IastErrorlog.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _("Error logs deleted successfully, Deletion Amount: {}").format(
                    deleted
                )
            )
        except Exception as e:
            logger.warning(
                _(
                    "Failed to delete error logs, probe ID: {}, error message: {}"
                ).format(self.agent.id, e)
            )

    def delete_heart_beat(self):
        try:
            deleted, _rows_count = IastHeartbeat.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete heartbeat data, error message: {}").format(e)
            )

    def delete_vul_overpower(self):
        try:
            deleted, _rows_count = IastOverpowerUserAuth.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete unauthorized data, error message: {}").format(e)
            )

    def delete_vul(self):
        try:
            deleted, _rows_count = IastVulnerabilityModel.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete vulnerability data, error message: {}").format(e)
            )

    def delete_sca(self):
        try:
            deleted, _rows_count = Asset.objects.filter(agent=self.agent).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _(
                    "Failed to delete third-party component data, error message: {}"
                ).format(e)
            )

    def delete_method_pool(self):
        try:
            deleted, _rows_count = MethodPool.objects.filter(agent=self.agent).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete method pool data, error message: {}").format(e)
            )

    def delete_method_pool_replay(self):
        try:
            deleted, _rows_count = IastAgentMethodPoolReplay.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _(
                    "The replay request method pool data was successfully deleted, A total of {} replay requests are deleted"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete replay request queue, error message: {}").format(e)
            )

    def delete_replay_queue(self):
        try:
            deleted, _rows_count = IastReplayQueue.objects.filter(
                agent=self.agent
            ).delete()
            logger.warning(
                _(
                    "Replay request queue deleted successfully, Deletion amount: {}"
                ).format(deleted)
            )
        except Exception as e:
            logger.warning(
                _("Failed to delete replay request queue, error message: {}").format(e)
            )


if __name__ == "__main__":
    MethodPool.objects.count()
    IastErrorlog.objects.count()
    IastHeartbeat.objects.count()
    IastOverpowerUserAuth.objects.count()
    Asset.objects.count()
    IastVulnerabilityModel.objects.count()
    MethodPool.objects.count()
