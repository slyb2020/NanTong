# coding:utf-8
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import *
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
import pymysql as MySQLdb
import reportlab.rl_config

reportlab.rl_config.warnOnMissingFontGlyphs = 0
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# pdfmetrics.registerFont(TTFont('song', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
# pdfmetrics.registerFont(TTFont('hei', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
pdfmetrics.registerFont(TTFont('hei', 'Font/SimSun.ttf'))  #注册字体

from reportlab.lib import fonts, colors

# fonts.addMapping('song', 0, 0, 'song')
# fonts.addMapping('song', 0, 1, 'song')
fonts.addMapping('hei', 0, 0, 'hei')
fonts.addMapping('hei', 0, 1, 'hei')

stylesheet = getSampleStyleSheet()
elements = []

doc = SimpleDocTemplate('剪切任务单.pdf')

elements.append(Paragraph('<font name="hei">学 生 成 绩 单</font>', stylesheet['Title']))
elements.append(Spacer(1, 12))

stylesheet.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
stylesheet['Justify'].fontName = 'hei'

elements.append(flowables.Preformatted(
    '课程名称：_____________________    		              主讲教师签名：_____________________',
    stylesheet['Justify']))
elements.append(Spacer(1, 12))

data = []
data.append(['学号', '姓名', '成绩'])

import pymysql as MySQLdb

data=[['1','李一博','90']]*30
print(data)
# ts = [('ALIGN',(0,0),(-1,-1),'CENTER'),('FONT', (0,0), (-1,-1), 'hei')]
ts = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black), ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
      ('FONT', (0, 0), (-1, -1), 'hei')]
table = Table(data, 2.1 * inch, 0.24 * inch, ts)
elements.append(table)

doc.build(elements)