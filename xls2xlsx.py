import win32com.client as win32
def xls2xlsx(fname):
    # fname = "D:\\WorkSpace\\Python\\NanTong_YNKS\\Excel\\test.xls"
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(fname+"x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()
