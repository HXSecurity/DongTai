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
from django.utils.translation import get_language
from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion

class ScaExportSer(ScaSerializer):
    class Meta:
        model = Asset
        fields = [
            'package_name',
            'version',
            'project_name',
            'project_version',
            'language',
            'package_path',
            'agent_name',
            'level',
            'signature_value',
        ]


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
        sca_data = ScaExportSer(queryset, many=True).data
        rows = []
        signatures = [i['signature_value']for i in sca_data]
        smas_total = ScaMavenArtifact.objects.filter(
            signature__in=signatures).values_list("signature", "aid",
                                                  "safe_version").all()
        headers = [
            'package_name', 'version', 'vul_name', 'level', 'package_path',
            'vulcve', 'vulcwe', 'project_name', 'project_version', 'language',
            'agent_name'
        ]
        zh_headers = [
            '组件名称', '组件版本', '漏洞名称', '风险等级', '组件路径', 'CVE 编号', 'CWE 编号', '项目名称',
            '项目版本', '语言', 'Agent 名称'
        ]
        dic = {}
        for i in smas_total:
            if dic.get(i[0], None):
                dic[i[0]].append((i[1:3]))
            else:
                dic[i[0]] = [(i[1:3])]
        for data in sca_data:
            smas = dic.get(data['signature_value'], [])
            datas = []
            for sma in smas:
                data_ = copy.deepcopy(data)
                svds = ScaArtifactDb.objects.filter(id=sma[0]).values(
                    'cve_id', 'cwe_id', 'title', 'overview', 'teardown',
                    'reference', 'level')
                if len(svds) == 0:
                    continue

                svd = svds[0]
                data_.update({
                    'vulcve':
                    get_cve(svd['cve_id']),
                    'vulcwe':
                    get_cwe(svd['cwe_id']),
                    'vul_name':
                    svd['title'],
                })
                datas.append(data_)
            for data_1 in datas:
                data_row = []
                for header in headers:
                    data_row.append(data_1.get(header, None))
                rows.append(data_row)
            if datas == []:
                data_row = []
                for header in headers:
                    data_row.append(data.get(header, None))
                rows.append(data_row)
        fileuuid = uuid.uuid1()
        i18n_headers = zh_headers if get_language() == 'zh' else headers
        filename = '组件报告' if get_language() == 'zh' else 'SCA REPORT'
        with open(f'/tmp/{fileuuid}.csv', 'wb') as csv_file:
            csv_file.write(b'\xEF\xBB\xBF')
        with open(f'/tmp/{fileuuid}.csv', 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(i18n_headers)
            for row in rows:
                writer.writerow(row)
        project_name = project_name if project_name else IastProject.objects.filter(
            pk=project_id).values_list('name', flat=True).first()
        project_version_id = current_project_version.get(
            "version_id", 0) if project_id else None
        project_version_name = IastProjectVersion.objects.filter(
            pk=project_version_id).values_list(
                'version_name',
                flat=True).first() if project_version_id else ''
        response = FileResponse(open(f'/tmp/{fileuuid}.csv', 'rb'),
                                filename=f'{filename}-{project_name}-{project_version_name}.csv')
        return response


def get_cve(cve_id):
    return 'https://cve.mitre.org/cgi-bin/cvename.cgi?name=' + cve_id


def get_cwe(cwe_id):
    if cwe_id in (None, 'NVD-CWE-Other', 'NVD-CWE-noinfo', ''):
        return cwe_id
    else:
        return f"https://cwe.mitre.org/data/definitions/{cwe_id.replace('CWE-','')}.html"
