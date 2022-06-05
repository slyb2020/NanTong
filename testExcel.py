import pandas as pd
import openpyxl
import numpy as np
# pd.read_excel(open('Excel/test.xlsx', 'rb'),
#               sheet_name='Sheet1')

wb=openpyxl.load_workbook('Excel/220308-NT202203002-CPP03-EPCI6 MTO-panel & ceiling2.xlsx')
ws = wb.active
# sheets = wb.worksheets
# for sheet in sheets:
#     print(sheet.title)
# # print(sheet.sheet_view)
# # sheet = wb['吸入类']
# print(ws['A4'].value)
data = []
for row in ws.values:
    temp = []
    for value in row:
        temp.append(value)
        # print(value)
    data.append(temp)
data = np.array(data)
print(data.shape)