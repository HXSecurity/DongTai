# coding:utf-8

import time
from collections import namedtuple
from iast.utils import get_model_field

from django.db.models import Q
from django.http import FileResponse
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from dongtai.models.vulnerablity import IastVulnerabilityModel
from dongtai.endpoint import R
from iast.base.agent import get_vul_count_by_agent
from dongtai.endpoint import UserEndPoint
from dongtai.models.agent import IastAgent
from dongtai.models.project import IastProject
from dongtai.models.vul_level import IastVulLevel
from webapi.settings import MEDIA_ROOT
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from iast.utils import extend_schema_with_envcheck, get_response_serializer
from io import BytesIO
from dongtai.models.project_report import ProjectReport
from django.http import HttpResponse
import logging
import os
import xlwt
import xlrd

logger = logging.getLogger('dongtai-webapi')


class _ProjectReportExportQuerySerializer(serializers.Serializer):
    vid = serializers.CharField(
        help_text=_("The version id of the project"),
        required=False)
    pname = serializers.CharField(
        help_text=_("The name of the project"),
        required=False)
    pid = serializers.IntegerField(help_text=_("The id of the project"),
        required=False)


class ProjectReportExport(UserEndPoint):
    name = 'api-v1-word-maker'
    description = _('Vulnerability Report Generate - Word')

    @staticmethod
    def create_word():
        pass

    @staticmethod
    def get_agents_with_project_id(pid, auth_users):
        """
        :param pid:
        :param auth_users:
        :return:
        """
        agent_ids = IastAgent.objects.filter(bind_project_id=pid,
                                             user__in=auth_users).values_list(
                                                 "id", flat=True).all()
        return agent_ids

    @staticmethod
    def create_report():
        pass

    def get(self, request):
        # 生成报告
        timestamp = time.time()
        id = 0
        try:
            id = int(request.query_params.get("id", 0))
        except:
            pid = 0
            vid = 0
            pname = ""

        if (pid == 0 and pname == ''):
            return R.failure(status=202, msg=_('Parameter error'))
        auth_users = self.get_auth_users(request.user)
        res = self.generate_word_report(pid, pname, vid, auth_users,
                                                   request.user, timestamp)
        if res is None:
            return R.failure(status=202, msg=_('Parameter error'))
        word_file_name, file_stream = res
        if word_file_name:
            report_file_path = word_file_name
            report_type = request.query_params.get('type', 'docx')
            if report_type == 'pdf':
                report_file_path = self.generate_pdf_report(word_file_name)
            report_filename = _('Vulnerability Report - {}. {}').format(
                timestamp, report_type)
            file_stream.seek(0)
            from wsgiref.util import FileWrapper
            response = FileResponse(FileWrapper(file_stream))
            response['content_type'] = 'application/octet-stream'
            response[
                'Content-Disposition'] = f"attachment; filename={report_filename}"
            return response
        else:
            return R.failure(status=203, msg=_('no permission'))

    def generate_word_report(self, pid, pname, vid, auth_users, user,
                             timestamp):

        project = IastProject.objects.filter(Q(id=pid) | Q(name=pname),
                                             user__in=auth_users).first()

        vul = IastVulnerabilityModel.objects.filter(pk=vid).first()

        if project or vul:
            if not project:
                Project = namedtuple(
                    'Project',
                    get_model_field(IastProject,
                                    include=[
                                        'id', 'name', 'mode', 'latest_time',
                                        'vul_count', 'agent_count'
                                    ]))
                project = Project(id=0,
                                  name='NAN',
                                  mode='NAN',
                                  latest_time=time.time(),
                                  vul_count=1,
                                  agent_count=0)
            agent_ids = self.get_agents_with_project_id(project.id, auth_users)

            count_result = get_vul_count_by_agent(agent_ids, vid, user)

            levelInfo = IastVulLevel.objects.all()

            if type == 'docx':
                return self.generate_word_report(user, project, vul, count_result, levelInfo, timestamp)
                pass
            elif type == 'pdf':
                return self.generate_pdf_report(user, project, vul, count_result, levelInfo, timestamp)
            elif type == 'xlsx':
                return self.generate_xlsx_report(user, project, vul, count_result, levelInfo, timestamp)

        return None, None

    def generate_pdf_report(self, user, project, vul, count_result, levelInfo, timestamp):
        from django.template.loader import render_to_string
        import os

        levelNameArr = {}
        levelIdArr = {}
        if levelInfo:
            for level_item in levelInfo:
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

        type_summary = count_result['type_summary']

        levelCount = count_result['levelCount']

        vulDetail = count_result['vulDetail']

        levelCountArr = []
        if levelCount:
            for ind in levelCount.keys():
                levelCountArr.append(str(levelIdArr[ind]) + str(levelCount[ind]))
        levelCountStr = ",".join(levelCountArr)

        vulTypeTableBodyRows = []

        new_cells = []
        if type_summary:
            for type_item in type_summary:
                vulTypeTableBodyRow = {
                    "type_level": levelIdArr[type_item['type_level']],
                    "type_name": type_item['type_name'],
                    "type_count": str(type_item['type_count'])
                }
                vulTypeTableBodyRows.append(vulTypeTableBodyRow)

        vulTypeDetailArray = []
        if vulDetail:
            type_ind = 1
            for vul in vulDetail.keys():
                vulTypeDetail = {
                    "title": u'%s(%s)' % ("2.3." + str(type_ind) + "  " + vul, len(vulDetail[vul])),
                    "vuls": []
                }
                vulTypeDetailArray.append(vulTypeDetail)
                if vulDetail[vul]:
                    ind = 1
                    for one in vulDetail[vul]:
                        oneVul = {
                            "title": "2.3." + str(type_ind) + "." + str(ind) + "  " + one['title'],
                            "summary": _(u'Summary'),

                            "severity_level": _("Severity level"),
                            "level_id": levelIdArr[one['level_id']],
                            "first_scan_time": _("First scan time"),
                            "first_time": one['first_time'],
                            "last_scan_time": _("First scan time"),
                            "latest_time": one['first_time'],
                            "development_language": _("Development language"),
                            "language": one['language'],
                            "vulnerability_url": _("Vulnerability URL"),
                            "url": one['url'],

                            "description": _(u'Vulnerability description'),
                            "detail": "",
                        }
                        vulTypeDetail.vuls.append(
                            oneVul
                        )
                        ind = ind + 1
                        if one['detail_data']:
                            for item in one['detail_data']:
                                oneVul.detail += u'%s' % item
                type_ind = type_ind + 1

        pdf_filename = f"{MEDIA_ROOT}/reports/vul-report-{user.id}-{timestamp}.pdf"
        html_filename = f"{MEDIA_ROOT}/reports/vul-report-{user.id}-{timestamp}.html"

        rendered = render_to_string(
            './pdf.html',
            {
                "user": user,
                "project": project,
                "vul": vul,
                "count_result": count_result,
                "level_info": levelInfo,
                "time_str": time.strftime('%Y-%m-%d %H:%M:%s', time.localtime(timestamp)),
                "levelCountStr": levelCountStr,
                "vulTypeTableBodyRows": vulTypeTableBodyRows
            }
        )
        f = open(html_filename, 'w')
        f.write(rendered)
        f.close()
        os.system("cat {} | /usr/local/bin/wkhtmltopdf - {}".format(
            html_filename,
            pdf_filename
        ))
        ProjectReportExport.delete_old_files(f"{MEDIA_ROOT}/reports/")
        return "pdf", rendered

    def generate_xlsx_report(self, user, project, vul, count_result, levelInfo, timestamp):
        levelNameArr = {}
        levelIdArr = {}
        if levelInfo:
            for level_item in levelInfo:
                levelNameArr[level_item.name_value] = level_item.id
                levelIdArr[level_item.id] = level_item.name_value

        type_summary = count_result['type_summary']

        levelCount = count_result['levelCount']

        vulDetail = count_result['vulDetail']

        levelCountArr = []
        if levelCount:
            for ind in levelCount.keys():
                levelCountArr.append(str(levelIdArr[ind]) + str(levelCount[ind]))
        levelCountStr = ",".join(levelCountArr)

        vulTypeTableBodyRows = []

        new_cells = []
        if type_summary:
            for type_item in type_summary:
                vulTypeTableBodyRow = {
                    "type_level": levelIdArr[type_item['type_level']],
                    "type_name": type_item['type_name'],
                    "type_count": str(type_item['type_count'])
                }
                vulTypeTableBodyRows.append(vulTypeTableBodyRow)

        vulTypeDetailArray = []
        if vulDetail:
            type_ind = 1
            for vul in vulDetail.keys():
                vulTypeDetail = {
                    "title": u'%s' % ("2.3." + str(type_ind) + "  " + vul),
                    "vuls": []
                }
                vulTypeDetailArray.append(vulTypeDetail)
                if vulDetail[vul]:
                    ind = 1
                    for one in vulDetail[vul]:
                        oneVul = {
                            "title": "2.3." + str(type_ind) + "." + str(ind) + "  " + one['title'],
                            "summary": _(u'Summary'),

                            "severity_level": _("Severity level"),
                            "level_id": levelIdArr[one['level_id']],
                            "first_scan_time": _("First scan time"),
                            "first_time": one['first_time'],
                            "last_scan_time": _("Last scan time"),
                            "latest_time": one['last_time'],
                            "development_language": _("Development language"),
                            "language": one['language'],
                            "vulnerability_url": _("Vulnerability URL"),
                            "url": one['url'],

                            "description": _(u'Vulnerability description'),
                            "detail": "",
                        }
                        vulTypeDetail.vuls.append(
                            oneVul
                        )
                        ind = ind + 1
                        if one['detail_data']:
                            for item in one['detail_data']:
                                oneVul.detail += u'%s' % item
                type_ind = type_ind + 1
        from openpyxl import Workbook
        wb = Workbook()
        sheet1 = wb.active
        xlsx_filename = f"{MEDIA_ROOT}/reports/vul-report-{user.id}-{timestamp}.xlsx"

        sheet1['A1'] = str(_("Vulnerability type name"))
        sheet1['B1'] = str(_("Severity levels"))
        sheet1['C1'] = str(_("First scan time"))
        sheet1['D1'] = str(_("Last scan time"))
        sheet1['E1'] = str(_("Development language"))
        sheet1['F1'] = str(_("Vulnerability URL"))
        sheet1['G1'] = str(_('Vulnerability description'))
        line = 0
        for vulTypeDetail in vulTypeDetailArray:
            line += 1
            sheet1.write(line, 0, vulTypeDetail.title)
            for oneVul in vulTypeDetail.vuls:
                sheet1.append(
                    [vulTypeDetail.title, oneVul.level_id, oneVul.first_time, oneVul.latest_time, oneVul.language,
                     oneVul.url, oneVul.detail])
        wb.save(xlsx_filename)
        ProjectReportExport.delete_old_files(f"{MEDIA_ROOT}/reports/")
        return "xlsx", "11"

    @staticmethod
    def delete_old_files(path, save_seconds=10):
        for f in os.listdir(path):
            if os.stat(os.path.join(path, f)).st_mtime < time.time() - save_seconds:
                os.remove(os.path.join(path, f))
