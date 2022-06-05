import os
import sys
import wx
import wx.lib.agw.xlsgrid as XG
import xlrd
_hasWin32 = False

_msg = "订单自动导入程序——测试版\n\n" + \
       "作者: 天津大学精仪四室 @ 2022年3月20日 \n\n" + \
       "Please report any bugs/requests of improvements\n" + \
       "to me at the following addresses:\n\n" + \
       "andrea.gavana@gmail.com\n" + "andrea.gavana@maerskoil.com\n\n" + \
       "欢迎使用智能生产管理系统!!"

class XLSGridFrame(wx.Frame):

    def __init__(self, parent,fileName, size=(950, 730)):

        wx.Frame.__init__(self, parent, title="伊纳克赛(南通)精致内饰材料有限公司智能生产管理系统 订单自动导入程序", size=size)
        panel = XLSGridPanel(self,fileName)

        self.CreateMenuAndStatusBar()
        self.CenterOnScreen()
        self.Show()


    def CreateMenuAndStatusBar(self):

        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()

        item = wx.MenuItem(fileMenu, wx.ID_ANY, "&E退出", "退出订单自动导入程序")
        self.Bind(wx.EVT_MENU, self.OnClose, item)
        fileMenu.Append(item)

        item = wx.MenuItem(helpMenu, wx.ID_ANY, "&H帮助...", "显示帮助对话框...")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        helpMenu.Append(item)

        menuBar.Append(fileMenu, "&F文件")
        menuBar.Append(helpMenu, "&H帮助")

        self.SetMenuBar(menuBar)

        statusbar = self.CreateStatusBar(2, wx.STB_SIZEGRIP)
        statusbar.SetStatusWidths([-2, -1])

        statusbar_fields = [("订单自动导入程序"),
                            ("欢迎您的使用")]

        for i in range(len(statusbar_fields)):
            statusbar.SetStatusText(statusbar_fields[i], i)


    def OnClose(self, event):

        wx.CallAfter(self.Destroy)


    def OnAbout(self, event):

        dlg = wx.MessageDialog(self, _msg, "订单自动导入程序",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

class XLSGridPanel(wx.Panel):

    def __init__(self, parent,filename):

        wx.Panel.__init__(self, parent)
        self.filename=filename
        self.start_button = wx.Button(self, -1, "Start")
        self.grid = XG.XLSGrid(self)

        self.grid.Hide()

        self.DoLayout()

        # self.Bind(wx.EVT_BUTTON, self.OnStart, self.start_button)

        # filename = os.path.join(os.path.abspath(dataDir), "Example_1.xls")

        if not os.path.isfile(self.filename):
            dlg = wx.MessageDialog(self, 'Error: the file "Example_1.xls" is not in the "data" directory',
                                   'XLSGridDemo Error', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return

        busy = wx.BusyInfo("Reading Excel file, please wait...")

        sheetname = "Example_1"
        book = xlrd.open_workbook(self.filename, formatting_info=1)

        sheet = book.sheet_by_name(sheetname)
        rows, cols = sheet.nrows, sheet.ncols

        comments, texts = XG.ReadExcelCOM(self.filename, sheetname, rows, cols)

        del busy

        self.grid.Show()
        self.grid.PopulateGrid(book, sheet, texts, comments)

        self.start_button.Enable(False)
        self.Layout()






    def DoLayout(self):

        xlrd_ver = xlrd.__VERSION__
        string_xlrd = "Version " + xlrd_ver

        if xlrd_ver <= "0.7.1":
            string_xlrd += ": hyperlink and rich-text functionalities will not work. xlrd 0.7.2 (SVN) is required for this."
        else:
            string_xlrd += ": hyperlink and rich-text functionalities will work!"

        if _hasWin32:
            string_pywin32 = "You have pywin32! XLSGrid cells should appear exactly as in Excel (WYSIWYG)."
        else:
            string_pywin32 = "You don't have pywin32. Cell string formatting will be severely limited."

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_right_sizer = wx.BoxSizer(wx.VERTICAL)
        top_center_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(self.start_button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 10)
        label_1 = wx.StaticText(self, -1, "xlrd:")
        label_1.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        top_center_sizer.Add(label_1, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        top_center_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_2 = wx.StaticText(self, -1, "pywin32:")
        label_2.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        top_center_sizer.Add(label_2, 0, wx.ALL|wx.ALIGN_RIGHT, 5)
        top_sizer.Add(top_center_sizer, 0, wx.EXPAND, 0)
        label_xlrd = wx.StaticText(self, -1, string_xlrd)
        top_right_sizer.Add(label_xlrd, 0, wx.ALL, 5)
        top_right_sizer.Add((0, 0), 1, wx.EXPAND, 0)
        label_pywin32 = wx.StaticText(self, -1, string_pywin32)
        top_right_sizer.Add(label_pywin32, 0, wx.ALL, 5)
        top_sizer.Add(top_right_sizer, 1, wx.EXPAND, 0)
        main_sizer.Add(top_sizer, 0, wx.ALL|wx.EXPAND, 5)
        main_sizer.Add((0, 10))
        main_sizer.Add(self.grid, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(main_sizer)

        main_sizer.Layout()

