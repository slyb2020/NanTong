from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.styles import getSampleStyleSheet
import datetime

# 调用模板，创建指定名称的PDF文档
doc = SimpleDocTemplate("Hello.pdf")
# 获得模板表格
styles = getSampleStyleSheet()
# 指定模板
style = styles['Normal']
# 初始化内容
story =[]

# 初始化表格内容
data= [['00', '01', '02', '03', '04'],
       ['10', '11', '12', '13', '14'],
       ['20', '21', '22', '23', '24'],
       ['30', '31', '32', '33', '34']]

# 根据内容创建表格
t = Table(data)
# 将表格添加到内容中
story.append(t)
# 将内容输出到PDF中
doc.build(story)

print(datetime.date.today())


