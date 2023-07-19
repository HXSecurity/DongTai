from django.test import TestCase

from dongtai_web.vul_log.vul_log import (
    log_change_status,
    log_push_to_integration,
    log_recheck_vul,
    log_vul_found,
)


class CreateLogTestCase(TestCase):
    def test_query_agent(self):
        log_change_status(user_id=1, user_name="hello", vul_id=[1], vul_status="已确认")
        log_recheck_vul(user_id=1, user_name="hello", vul_id=[1], vul_status="已确认")
        log_push_to_integration(
            user_id=1,
            user_name="hello",
            vul_id=1,
            integration_name="JIRA",
            source_vul_type=1,
        )
        log_vul_found(
            user_id=1,
            project_name="helloproject",
            project_id=1,
            vul_id=1,
            vul_name="已确认",
        )
