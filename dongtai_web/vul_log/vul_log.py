import logging

from dongtai_common.models.iast_vul_log import IastVulLog, MessageTypeChoices

logger = logging.getLogger("dongtai-webapi")


def log_change_status(user_id: int, user_name: str, vul_id: list, vul_status: str):
    kwargs = locals()
    logger.debug(kwargs)
    if "kwargs" in kwargs:
        del kwargs["kwargs"]
    msg = f"id为{user_id}的用户{user_name}修改漏洞状态为{vul_status}"
    IastVulLog.objects.bulk_create(
        [
            IastVulLog(
                msg_type=MessageTypeChoices.CHANGE_STATUS,
                msg=msg,
                meta_data=kwargs,
                vul_id=v_id,
                user_id=user_id,
            )
            for v_id in vul_id
        ]
    )


def log_recheck_vul(user_id: int, user_name: str, vul_id: list, vul_status: str):
    kwargs = locals()
    msg = f"自动验证修改漏洞状态为{vul_status}"
    IastVulLog.objects.bulk_create(
        [
            IastVulLog(
                msg_type=MessageTypeChoices.VUL_RECHECK,
                msg=msg,
                meta_data=kwargs,
                vul_id=v_id,
                user_id=user_id,
            )
            for v_id in vul_id
        ]
    )


def log_push_to_integration(
    user_id: int,
    user_name: str,
    vul_id: int,
    integration_name: str,
    source_vul_type: int,
):
    kwargs = locals()
    msg = f"id为{user_id}的用户{user_name}推送漏洞到{integration_name}"
    if source_vul_type == 1:
        IastVulLog.objects.create(
            msg_type=MessageTypeChoices.PUSH_TO_INTEGRATION,
            msg=msg,
            meta_data=kwargs,
            vul_id=vul_id,
            user_id=user_id,
        )
    else:
        IastVulLog.objects.create(
            msg_type=MessageTypeChoices.PUSH_TO_INTEGRATION,
            msg=msg,
            meta_data=kwargs,
            asset_vul_id=vul_id,
            user_id=user_id,
        )


def log_vul_found(user_id: int, project_name: str, project_id: int, vul_id: int, vul_name: str):
    kwargs = locals()
    msg = f"id为{project_id}的项目{project_name}检测到漏洞{vul_name}"
    IastVulLog.objects.create(
        msg_type=MessageTypeChoices.VUL_FOUND,
        msg=msg,
        meta_data=kwargs,
        vul_id=vul_id,
        user_id=user_id,
    )


def log_asset_vul_found(user_id: int, project_name: str, project_id: int, asset_vul_id: int, vul_name: str):
    kwargs = locals()
    msg = f"id为{project_id}的项目{project_name}检测到漏洞{vul_name}"
    IastVulLog.objects.create(
        msg_type=MessageTypeChoices.VUL_FOUND,
        msg=msg,
        meta_data=kwargs,
        asset_vul_id=asset_vul_id,
        user_id=user_id,
    )
