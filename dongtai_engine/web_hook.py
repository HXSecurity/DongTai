import json
import time
import requests
from celery.apps.worker import logger
from celery import shared_task
from dongtai.models.agent_webhook_setting import IastAgentUploadTypeUrl


@shared_task(queue='dongtai-report-task')
def forward_for_upload(id, reports, report_type):

    """
    agent 流量转发 web hook
    :return:
    """
    print("search agent forward for url time {}, type_id:{}".format(str(int(time.time())), str(report_type)))
    typeData = IastAgentUploadTypeUrl.objects.filter(user_id=id, type_id=report_type).order_by("-create_time").first()
    # print(report_type)

    try:
        if typeData and typeData.url:
            if typeData.headers:
                headers = typeData.headers
            else:
                headers = {}
        else:
            return None
        logger.info(f'agent report upload forward begin [{str(report_type)}]')
        req = requests.post(typeData.url, json=reports, headers=headers, timeout=60)
        reports_data = json.dumps(reports)
        logger.info("Forward for url response status {} -".format(str(req.status_code)))
        logger.info("Forward for url request= {} ; response={} ;".format(reports_data, req.content))
        if req.status_code == 200:
            data = json.loads(req.text)
            if data.get("code", 0) == 200:
                typeData.send_num = typeData.send_num+1
                typeData.save()
    except Exception as e:
        logger.info(f'upload forward error [{e}]')

