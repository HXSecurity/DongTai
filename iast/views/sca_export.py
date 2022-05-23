######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : sca_export
# @created     : 星期五 12月 24, 2021 15:20:45 CST
#
# @description :
######################################################################

from dongtai.endpoint import R, UserEndPoint
from dongtai.models.asset import Asset
from iast.serializers.sca import ScaSerializer
from iast.base.project_version import get_project_version, get_project_version_by_id
import csv
from django.http import FileResponse
import uuid
from django.utils.translation import get_language
from dongtai.models.project import IastProject
from dongtai.models.project_version import IastProjectVersion
from dongtai.models.asset_vul import IastAssetVul

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
        project_id = request.query_params.get('project_id', None)
        project_name = request.query_params.get('project_name')
        if project_id and project_id != '':
            version_id = request.GET.get('version_id', None)
            if not version_id:
                current_project_version = get_project_version(
                    project_id, auth_users)
            else:
                current_project_version = get_project_version_by_id(version_id)
        sca_data = IastAssetVul.objects.filter(
            iastvulassetrelation__asset__user__in=auth_users,
            iastvulassetrelation__asset__project_id=project_id
        ).values(
            'iastvulassetrelation__asset__package_name',
            'iastvulassetrelation__asset__version', 'vul_name',
            'level__name_type', 'iastvulassetrelation__asset__package_path',
            'vul_cve_nums',
            'iastvulassetrelation__asset__agent__bind_project__name',
            'iastvulassetrelation__asset__agent__project_version__version_name',
            'iastvulassetrelation__asset__agent__language',
            'iastvulassetrelation__asset__agent__token')
        sca_data = list(sca_data)
        headers = [
            'package_name', 'version', 'vul_name', 'level', 'package_path',
            'project_name', 'project_version', 'language', 'agent_name',
            'vulcve', 'vulcwe'
        ]
        zh_headers = [
            '组件名称', '组件版本', '漏洞名称', '风险等级', '组件路径', '项目名称', '项目版本', '语言',
            'Agent 名称', 'CVE 编号', 'CWE 编号'
        ]
        rows = []
        for i in sca_data:
            cve_id = i['vul_cve_nums'].get('cve', None)
            cwe_id = i['vul_cve_nums'].get('cwe', None)
            i['vulcve'] = get_cve(cve_id) if cve_id else ''
            i['vulcwe'] = get_cwe(cwe_id) if cwe_id else ''
            del i['vul_cve_nums']
            rows.append(i.values())
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
