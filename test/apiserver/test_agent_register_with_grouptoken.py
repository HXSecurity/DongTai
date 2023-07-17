######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : test_agent_register
# @created     : 星期五 12月 10, 2021 14:46:44 CST
#
# @description :
######################################################################

from test.apiserver.test_agent_base import AgentTestCase
from dongtai_common.models.agent import IastAgent
from dongtai_common.models.department import Department
from dongtai_web.projecttemplate.update_department_data import update_department_data
import json
import uuid


class AgentNewRegisterGroupTokenTestCase(AgentTestCase):

    def setUp(self):
        super().setUp()
        update_department_data()
        self.client.force_authenticate()
        self.test_agent_id = []

    def test_rep_register(self):
        department = Department.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION="Token GROUP" +
                                department.token)
        resp1 = self.raw_register(projectVersion='V1.1', projectName='PNAME')
        data1 = json.loads(resp1.content)
        resp2 = self.raw_register(name='newtoken',
                                  projectVersion='V1.1',
                                  projectName='PNAME')
        data2 = json.loads(resp2.content)
        self.assertNotEqual(data1['data']['id'], data2['data']['id'])

    def test_rep_register_2(self):
        department = Department.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION="Token GROUP" +
                                department.token)
        resp1 = self.raw_register(projectTemplateId=1,
                                  projectVersion='V1.1',
                                  projectName='PNAME')
        data1 = json.loads(resp1.content)
        self.assertEqual(data1['status'], 201)

    def test_rep_register_3(self):
        department = Department.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION="Token GROUP" +
                                department.token)
        resp1 = self.raw_register(token=uuid.uuid4().hex)
        data1 = json.loads(resp1.content)
        self.assertEqual(data1['status'], 201)
        agent_id1 = data1['data']['id']
        agent1 = IastAgent.objects.filter(pk=agent_id1).first()
        agent1.bind_project.department_id = 2
        agent1.bind_project.save()
        resp2 = self.raw_register(token=uuid.uuid4().hex)
        data2 = json.loads(resp2.content)
        self.assertEqual(data2['status'], 201)
        agent_id2 = data2['data']['id']
        agent2 = IastAgent.objects.filter(pk=agent_id2).first()
        self.assertNotEqual(agent1.bind_project_id, agent2.bind_project_id)
        self.assertNotEqual(agent1.project_version_id,
                            agent2.project_version_id)

    def test_rep_register_4(self):
        department = Department.objects.first()
        self.client.credentials(HTTP_AUTHORIZATION="Token GROUP" +
                                department.token)
        resp1 = self.raw_register(token=uuid.uuid4().hex)
        data1 = json.loads(resp1.content)
        self.assertEqual(data1['status'], 201)
        agent_id1 = data1['data']['id']
        agent1 = IastAgent.objects.filter(pk=agent_id1).first()
        agent1.bind_project.department_id = 2
        agent1.bind_project.save()
        resp2 = self.raw_register(token=uuid.uuid4().hex)
        data2 = json.loads(resp2.content)
        self.assertEqual(data2['status'], 201)
        agent_id2 = data2['data']['id']
        agent2 = IastAgent.objects.filter(pk=agent_id2).first()
        agent2.bind_project_id = agent1.bind_project_id
        agent2.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token GROUP" +
                                department.token)
        resp3 = self.raw_register(token=uuid.uuid4().hex)
        data3 = json.loads(resp3.content)
        self.assertEqual(data3['status'], 201)
        agent_id3 = data3['data']['id']
        agent3 = IastAgent.objects.filter(pk=agent_id3).first()
        self.assertNotEqual(agent_id3, agent_id2)
        self.assertNotEqual(agent3.bind_project_id, agent2.bind_project_id)
