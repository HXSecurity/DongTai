# coding:utf-8
# 写word文档文件
import time

from django.db.models import Q
from django.http import FileResponse
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from base import R
from iast.base.agent import get_vul_count_by_agent
from iast.base.user import UserEndPoint
from dongtai_models.models.agent import IastAgent
from dongtai_models.models.project import IastProject
from dongtai_models.models.vul_level import IastVulLevel
from webapi.settings import MEDIA_ROOT


class ProjectReportExport(UserEndPoint):
    name = 'api-v1-word-maker'
    description = '漏洞word报告生成'

    @staticmethod
    def create_word():
        pass

    @staticmethod
    def get_agents_with_project_id(pid, auth_users):
        """
        通过项目ID查询有权限的agent
        :param pid:
        :param auth_users:
        :return:
        """
        relations = IastAgent.objects.filter(bind_project_id=pid, user__in=auth_users).values("id")
        agent_ids = [relation['id'] for relation in relations]
        return agent_ids

    @staticmethod
    def create_report():
        pass

    def get(self, request):
        timestamp = time.time()
        word_file_name = self.generate_word_report(request, timestamp)
        if word_file_name:
            report_file_path = word_file_name
            report_type = request.query_params.get('type', 'docx')
            if report_type == 'pdf':
                report_file_path = self.generate_pdf_report(word_file_name)
            report_filename = f'漏洞报告-{timestamp}.{report_type}'

            response = FileResponse(open(report_file_path, "rb"))
            response['content_type'] = 'application/octet-stream'
            response['Content-Disposition'] = f"attachment; filename={report_filename}"
            return response
        else:
            return R.failure(status=203, msg='no permission')

    def generate_word_report(self, request, timestamp):
        try:
            pid = int(request.query_params.get("pid", 0))
            pname = request.query_params.get('pname')
            vid = int(request.query_params.get("vid", 0))
        except:
            pid = 0
            vid = 0
            pname = ''
        if pid == 0 and pname == '':
            return R.failure(status=202, msg='参数错误')

        # 获取项目信息，获取agent信息，获取相应漏洞信息,写入漏洞信息
        user = request.user
        auth_users = self.get_auth_users(request.user)
        project = IastProject.objects.filter(Q(id=pid) | Q(name=pname), user__in=auth_users).first()

        if project:
            agent_ids = self.get_agents_with_project_id(project.id, auth_users)

            document = Document()
            document.styles.add_style('TitleOne', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleTwo', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleThree', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'
            document.styles.add_style('TitleFour', WD_STYLE_TYPE.PARAGRAPH).font.name = 'Arial'

            # 设置文档标题，中文要用unicode字符串 【项目名称】
            document.add_heading(u'%s' % project.name, 0)

            # 扫描模式
            document.add_heading(u'%s' % project.mode, 2)
            # 报告日期
            timeArray = time.localtime(project.latest_time)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

            pTime = document.add_paragraph(u'%s' % otherStyleTime)
            pTime.paragraph_format.space_before = Pt(400)
            pTime.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            pReport = document.add_paragraph(u'安全测试报告')
            pReport.paragraph_format.line_spacing = Pt(20)
            pReport.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            footer = document.sections[0].footer
            paragraph = footer.paragraphs[0]
            paragraph.add_run(u'北京安全共识科技有限公司')
            paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

            document.add_page_break()

            # 项目基础信息-table
            oneTitle = document.add_paragraph()
            oneTitle.add_run(u'一 、项目基础信息').font.name = 'Arial'
            oneTitle.style = "TitleOne"
            # 添加表格: 1行3列
            table = document.add_table(rows=1, cols=2, style='Table Grid')
            # 获取第一行的单元格列表对象
            hdr_cells = table.rows[0].cells
            # 为表格添加一行
            new_cells = table.add_row().cells
            new_cells[0].text = '项目名称'
            new_cells[1].text = project.name
            new_cells = table.add_row().cells
            new_cells[0].text = '创建人员'
            new_cells[1].text = user.username
            new_cells = table.add_row().cells
            new_cells[0].text = '项目类型'
            new_cells[1].text = project.mode
            new_cells = table.add_row().cells
            new_cells[0].text = '漏洞数量'
            new_cells[1].text = str(project.vul_count)
            new_cells = table.add_row().cells
            new_cells[0].text = 'Agent数量'
            new_cells[1].text = str(project.agent_count)
            new_cells = table.add_row().cells
            new_cells[0].text = '最新时间'
            new_cells[1].text = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            # 根据漏洞类型获取漏洞ID
            levelInfo = IastVulLevel.objects.all()

            levelNameArr = {}
            levelIdArr = {}
            if levelInfo:
                for level_item in levelInfo:
                    levelNameArr[level_item.name_value] = level_item.id
                    levelIdArr[level_item.id] = level_item.name_value
            # 结果分析
            count_result = get_vul_count_by_agent(agent_ids, vid, user)
            # 按漏洞等级汇总
            # 类型汇总
            type_summary = count_result['type_summary']
            # 等级汇总
            levelCount = count_result['levelCount']
            # 漏洞详情
            vulDetail = count_result['vulDetail']
            # 按漏洞类型汇总
            oneTitle = document.add_paragraph()
            oneTitle.add_run(u'二、结果分析')
            oneTitle.style = "TitleOne"

            twoTitle = document.add_paragraph()
            twoTitle.add_run(u'2.1  漏洞等级分布')
            twoTitle.style = "TitleTwo"
            levelCountArr = []
            if levelCount:
                for ind in levelCount.keys():
                    levelCountArr.append(str(levelIdArr[ind]) + str(levelCount[ind]))
            levelCountStr = ",".join(levelCountArr)
            document.add_paragraph(levelCountStr)

            twoTitle = document.add_paragraph()
            twoTitle.add_run(u'2.2  漏洞类型分布')
            twoTitle.style = "TitleTwo"
            # 添加表格: 1行3列
            table = document.add_table(rows=1, cols=3, style='Table Grid')
            # 获取第一行的单元格列表对象
            hdr_cells = table.rows[0].cells
            # 为每一个单元格赋值
            # 注：值都要为字符串类型
            hdr_cells[0].text = '漏洞等级'
            hdr_cells[1].text = '漏洞类型名称'
            hdr_cells[2].text = '数量'
            if type_summary:
                for type_item in type_summary:
                    # 为表格添加一行
                    new_cells = table.add_row().cells
                    new_cells[0].text = levelIdArr[type_item['type_level']]
                    new_cells[1].text = type_item['type_name']
                    new_cells[2].text = str(type_item['type_count'])

            # 添加分页符
            document.add_page_break()
            # 获取漏洞详情
            twoTitle = document.add_paragraph()
            twoTitle.add_run(u'2.3  漏洞详情')
            twoTitle.style = "TitleTwo"

            # rn = p_new.add_run(r_text, r.style)
            # self.copyFont(r, rn)
            # rn.font.name = 'Arial'
            # rn.font.size = Pt(10)

            # 获取第一行的单元格列表对象
            if vulDetail:
                type_ind = 1
                for vul in vulDetail.keys():
                    # 漏洞类型名称(数量）
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
                            document.add_heading(u'概要信息', level=4)
                            # 添加表格: 1行2列
                            table = document.add_table(rows=1, cols=2, style='Table Grid')
                            new_cells = table.add_row().cells
                            new_cells[0].text = "危害等级"
                            new_cells[1].text = levelIdArr[one['level_id']]

                            new_cells = table.add_row().cells
                            new_cells[0].text = "首次检测时间"
                            new_cells[1].text = one['first_time']

                            new_cells = table.add_row().cells
                            new_cells[0].text = "最近检测时间"
                            new_cells[1].text = one['latest_time']

                            new_cells = table.add_row().cells
                            new_cells[0].text = "开发语言"
                            new_cells[1].text = one['language']

                            new_cells = table.add_row().cells
                            new_cells[0].text = "漏洞url"
                            new_cells[1].text = one['url']
                            document.add_heading(u'漏洞描述', level=4)
                            if one['detail_data']:
                                for item in one['detail_data']:
                                    document.add_paragraph(u'%s' % item)
                    type_ind = type_ind + 1
            # 保存文档
            document.styles['TitleOne'].font.size = Pt(20)
            document.styles['TitleOne'].font.name = "Arial"
            document.styles['TitleTwo'].font.size = Pt(18)
            document.styles['TitleTwo'].font.name = "Arial"
            document.styles['TitleThree'].font.size = Pt(16)
            document.styles['TitleFour'].font.size = Pt(14)
            filename = f"{MEDIA_ROOT}/reports/vul-report-{user.id}-{timestamp}.docx"
            document.save(filename)
            return filename

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
