######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : sca_export
# @created     : 星期五 12月 24, 2021 15:20:45 CST
#
# @description :
######################################################################



from dongtai.models.sca_artifact_db import ScaArtifactDb
from dongtai.models.sca_maven_artifact import ScaMavenArtifact
from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from iast.serializers.sca import ScaSerializer
from iast.base.agent import get_agents_with_project
from iast.base.project_version import get_project_version, get_project_version_by_id
import csv
from io import StringIO,BytesIO
from wsgiref.util import FileWrapper
from django.http import FileResponse
import uuid
import copy
from django.utils.translation import gettext_lazy as _
class ScaExport(UserEndPoint):
    def get(self, request):
        auth_users = self.get_auth_users(request.user)
        auth_agents = self.get_auth_agents(auth_users)
        project_id = request.query_params.get('project_id', None)
        project_name = request.query_params.get('project_name')
        queryset = Asset.objects.filter(agent__in=auth_agents)
        if project_id and project_id != '':

            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
            agents = self.get_auth_agents(auth_users).filter(
                bind_project_id=project_id,
                project_version_id=current_project_version.get(
                    "version_id", 0))
            queryset = queryset.filter(agent__in=agents)

        elif project_name and project_name != '':
            agent_ids = get_agents_with_project(project_name, auth_users)
            if agent_ids:
                queryset = queryset.filter(agent_id__in=agent_ids)
        sca_data = ScaSerializer(queryset, many=True).data
        headers = ScaSerializer.Meta.fields + [
            'vul_safe_version', 'vulcve', 'vulcwe', 'vulname', 'vul_overview',
            'vul_teardown', 'vul_reference', 'vul_level'
        ]
        rows = []
        for data in sca_data:
            smas = ScaMavenArtifact.objects.filter(
                signature=data['signature_value']).values(
                    "aid", "safe_version")
            datas = []
            for sma in smas:
                data_ = copy.deepcopy(data)
                svds = ScaArtifactDb.objects.filter(id=sma['aid']).values(
                    'cve_id', 'cwe_id', 'title', 'overview', 'teardown',
                    'reference', 'level')
                if len(svds) == 0:
                    continue

                svd = svds[0]
                data_.update({
                    'vul_safe_version':
                    sma['safe_version'] if sma['safe_version'] else
                    _('Current version stopped for maintenance or it is not a secure version'
                      ),
                    'vulcve':
                    svd['cve_id'],
                    'vulcwe':
                    svd['cwe_id'],
                    'vulname':
                    svd['title'],
                    'vul_overview':
                    svd['overview'],
                    'vul_teardown':
                    svd['teardown'],
                    'vul_reference':
                    svd['reference'],
                    'vul_level':
                    svd['level'],
                })
                datas.append(data_)
            for data_1 in datas:
                data_row = []
                for header in headers:
                    data_row.append(data_1.get(header, None))
                rows.append(data_row)
        fileuuid = uuid.uuid1()
        with open(f'/tmp/{fileuuid}.csv', 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)
        response = FileResponse(open(f'/tmp/{fileuuid}.csv', 'rb'),
                                filename='sca.csv')
        return response
