# 引入所需要的基本包
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.platypus import Image
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def drawBitmap(c):
    I = Image("D:\\WorkSpace\\Python\\NanTong_YNKS\\bitmaps\\PVC.jpg")
    styleSheet = getSampleStyleSheet()
    I.drawHeight = 1.25 * inch * I.drawHeight / I.drawWidth
    I.drawWidth = 1.25 * inch
    P0 = Paragraph('''
         <b>A pa<font color=red>r</font>a<i>graph</i></b>
         <super><font color=yellow>1</font></super>''',
                   styleSheet["BodyText"])
    P = Paragraph('''
         <para align=center spaceb=3>The <b>ReportLab Left
         <font color=red>Logo</font></b>
         Image</para>''',
                  styleSheet["BodyText"])
    data = [['A', 'B', 'C', P0, 'D'],
            ['00', '01', '02', [I, P], '04'],
            ['10', '11', '12', [P, I], '14'],
            ['20', '21', '22', '23', '24'],
            ['30', '31', '32', '33', '34']]
    t = Table(data, style=[('GRID', (1, 1), (-2, -2), 1, colors.green),
                           ('BOX', (0, 0), (1, -1), 2, colors.red),
                           ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                           ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                           ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                           ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                           ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                           ('BOX', (0, 0), (-1, -1), 2, colors.black),
                           ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                           ('VALIGN', (3, 0), (3, 0), 'BOTTOM'),
                           ('BACKGROUND', (3, 0), (3, 0), colors.limegreen),
                           ('BACKGROUND', (3, 1), (3, 1), colors.khaki),
                           ('ALIGN', (3, 1), (3, 1), 'CENTER'),
                           ('BACKGROUND', (3, 2), (3, 2), colors.beige),
                           ('ALIGN', (3, 2), (3, 2), 'LEFT'),
                           ])
    t._argW[3] = 1.5 * inch
    t.wrapOn(c, 176.7 * mm, 200 * mm)
    t.drawOn(c, 15 * mm, 75.6 * mm)


# 定义要生成的pdf的名称
c = canvas.Canvas("image.pdf")
# 调用函数生成条形码和二维码，并将canvas对象作为参数传递
drawBitmap(c)
# showPage函数：保存当前页的canvas
# c.showPage()
# save函数：保存文件并关闭canvas
c.save()
