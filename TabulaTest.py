#-*- conding: utf-8 -*-

import tabula

df = tabula.read_pdf("42.pdf", encoding='gbk', pages='all')
print(df)
# for indexs in df.index:
#     # 遍历打印企业名称
#     print(df.loc[indexs].values[1].strip())