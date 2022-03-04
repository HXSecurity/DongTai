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

    @extend_schema_with_envcheck(
        [_ProjectReportExportQuerySerializer],
        tags=[_('Project')],
        summary=_('Projects Report Export'),
        description=
        _("According to the conditions, export the report of the specified project or the project of the specified vulnerability."
          ),
    )
    def get(self, request):
        timestamp = time.time()
        try:
            pid = int(request.query_params.get("pid", 0))
            pname = request.query_params.get('pname')
            vid = int(request.query_params.get("vid", 0))
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

            document = Document()
            document.styles.add_style('TitleOne', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleTwo', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleThree', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleFour', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'


            document.add_heading(u'%s' % project.name, 0)


            document.add_heading(u'%s' % project.mode, 2)

            timeArray = time.localtime(project.latest_time)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            pTime = document.add_paragraph(u'%s' % otherStyleTime)
            pTime.paragraph_format.space_before = Pt(400)
            pTime.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            pReport = document.add_paragraph(_(u'Security Testing Report'))
            pReport.paragraph_format.line_spacing = Pt(20)
            pReport.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            footer = document.sections[0].footer
            paragraph = footer.paragraphs[0]
            paragraph.add_run(u'北京安全共识科技有限公司')
            paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            document.add_page_break()


            oneTitle = document.add_paragraph()
            oneTitle.add_run(_(u'First, project information')).font.name = 'Arial'
            oneTitle.style = "TitleOne"

            table = document.add_table(rows=1, cols=2, style='Table Grid')

            hdr_cells = table.rows[0].cells

            new_cells = table.add_row().cells
            new_cells[0].text = _('Application name')
            new_cells[1].text = project.name
            new_cells = table.add_row().cells
            new_cells[0].text = _('Author')
            new_cells[1].text = user.username
            new_cells = table.add_row().cells
            new_cells[0].text = _('Application type')
            new_cells[1].text = project.mode
            new_cells = table.add_row().cells
            new_cells[0].text = _('Number of Vulnerability')
            new_cells[1].text = str(project.vul_count)
            new_cells = table.add_row().cells
            new_cells[0].text = _('Number of Agent')
            new_cells[1].text = str(project.agent_count)
            new_cells = table.add_row().cells
            new_cells[0].text = _('Latest time')
            new_cells[1].text = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            levelInfo = IastVulLevel.objects.all()

            levelNameArr = {}
            levelIdArr = {}
            if levelInfo:
                for level_item in levelInfo:
                    levelNameArr[level_item.name_value] = level_item.id
                    levelIdArr[level_item.id] = level_item.name_value

            count_result = get_vul_count_by_agent(agent_ids, vid, user)


            type_summary = count_result['type_summary']

            levelCount = count_result['levelCount']

            vulDetail = count_result['vulDetail']

            oneTitle = document.add_paragraph()
            oneTitle.add_run(_(u'Second, the result analysis'))
            oneTitle.style = "TitleOne"

            twoTitle = document.add_paragraph()
            twoTitle.add_run(_(u'2.1 Vulnerability Severity Levels Distribution'))
            twoTitle.style = "TitleTwo"
            levelCountArr = []
            if levelCount:
                for ind in levelCount.keys():
                    levelCountArr.append(str(levelIdArr[ind]) + str(levelCount[ind]))
            levelCountStr = ",".join(levelCountArr)
            document.add_paragraph(levelCountStr)

            twoTitle = document.add_paragraph()
            twoTitle.add_run(_(u'2.2 Distribution of Vulnerability'))
            twoTitle.style = "TitleTwo"

            table = document.add_table(rows=1, cols=3, style='Table Grid')

            hdr_cells = table.rows[0].cells


            hdr_cells[0].text = _('Severity levels')
            hdr_cells[1].text = _('Vulnerability type name')
            hdr_cells[2].text = _('Number')
            if type_summary:
                for type_item in type_summary:

                    new_cells = table.add_row().cells
                    new_cells[0].text = levelIdArr[type_item['type_level']]
                    new_cells[1].text = type_item['type_name']
                    new_cells[2].text = str(type_item['type_count'])


            document.add_page_break()

            twoTitle = document.add_paragraph()
            twoTitle.add_run(_(u'2.3 Vulnerability details'))
            twoTitle.style = "TitleTwo"

            # rn = p_new.add_run(r_text, r.style)
            # self.copyFont(r, rn)
            # rn.font.name = 'Arial'
            # rn.font.size = Pt(10)


            if vulDetail:
                type_ind = 1
                for vul in vulDetail.keys():

                    threeTitle = document.add_paragraph()
                    threeTitle.add_run(u'%s(%s)' % ("2.3." + str(type_ind) + "  " + vul, len(vulDetail[vul])))
                    threeTitle.style = "TitleThree"
                    if vulDetail[vul]:
                        ind = 1
                        for one in vulDetail[vul]:
                            p = document.add_paragraph()
                            p.add_run("2.3." + str(type_ind) + "." + str(ind) + "  " + one['title']).bold = True
                            p.style = "TitleFour"
                            ind = ind + 1
                            document.add_heading(_(u'Summary'), level=4)

                            table = document.add_table(rows=1, cols=2, style='Table Grid')
                            new_cells = table.add_row().cells
                            new_cells[0].text = _("Severity level")
                            new_cells[1].text = levelIdArr[one['level_id']]

                            new_cells = table.add_row().cells
                            new_cells[0].text = _("First scan time")
                            new_cells[1].text = one['first_time']

                            new_cells = table.add_row().cells
                            new_cells[0].text = _("Last scan time")
                            new_cells[1].text = one['latest_time']

                            new_cells = table.add_row().cells
                            new_cells[0].text = _("Development language")
                            new_cells[1].text = one['language']

                            new_cells = table.add_row().cells
                            new_cells[0].text = _("Vulnerability URL")
                            new_cells[1].text = one['url']
                            document.add_heading(_(u'Vulnerability description'), level=4)
                            if one['detail_data']:
                                for item in one['detail_data']:
                                    document.add_paragraph(u'%s' % item)
                    type_ind = type_ind + 1

            document.styles['TitleOne'].font.size = Pt(20)
            document.styles['TitleOne'].font.name = "Arial"
            document.styles['TitleTwo'].font.size = Pt(18)
            document.styles['TitleTwo'].font.name = "Arial"
            document.styles['TitleThree'].font.size = Pt(16)
            document.styles['TitleFour'].font.size = Pt(14)
            filename = f"{MEDIA_ROOT}/reports/vul-report-{user.id}-{timestamp}.docx"
            file_stream = BytesIO()
            document.save(file_stream)
            return filename, file_stream

        return None

    @staticmethod
    def generate_pdf_report(filename):
        try:
            pdf_filename = filename.replace('docx', 'pdf')
            return pdf_filename
        except:
            pass

    @staticmethod
    def generate_pdf_with_string():
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen.canvas import Canvas
        from reportlab.lib.pagesizes import A4
        canv = Canvas('/tmp/text-on-image.pdf', pagesize=A4)
        img = ImageReader('/tmp/pythonpowered.gif')

        # now begin the work
        x = 113
        y = 217
        w = 103
        h = 119
        canv.drawImage(img, x, y, w, h, anchor='sw', anchorAtXY=True, showBoundary=False)
        canv.setFont('arial', 14)
        canv.setFillColor((1, 0, 0))  # change the text color
        canv.drawCentredString(x + w * 0.5, y + h * 0.5, 'On Top')
        canv.save()
