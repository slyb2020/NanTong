import wx
from ID_DEFINE import *
from DateTimeConvert import *
from DBOperation import GetDraftOrderDetailByID,GetDraftComponentInfoByID,GetMeterialPrice,SaveMeterialTodayPriceInDB
import wx.propgrid as wxpg
import sys
from SetupPropertyDialog import *
from OrderManagementPanel import TechDrawingButtonEditor
import wx.grid as gridlib
import copy

# class DraftOrderPanel(wx.Panel):
#     def __init__( self, parent, master,log ,size,mode="NEW",ID=None,character="设计员"):
#         wx.Panel.__init__(self, parent, wx.ID_ANY,size=size)
#         self.master = master
#         self.log = log
#         self.ID=ID
#         self.mode = mode
#         self.character = character
#         self.ReCreate()
#
#     def ReCreate(self):
#         self.Freeze()
#         self.DestroyChildren()
#         self.panel = panel = wx.Panel(self, wx.ID_ANY)
#         self.orderName = ""
#         self.customerName = ""
#         self.customerInfo = ""
#         self.contactsName = ""
#         self.phoneNumber = ""
#         self.email =""
#         self.bidMode = BIDMODE[0]
#         self.bidMethod = BIDMETHOD[0]
#         self.techDrawingName = ""
#         self.techDrawingName2 = ""
#         self.techDrawingName3 = ""
#         self.techDrawingName4 = ""
#         self.secureProtocolName = ""
#         self.bidDocName = ""
#         self.techRequireDocName = ""
#         self.makeOrderDate = wx.DateTime.Now()
#         self.bidDate = pydate2wxdate(datetime.date.today() + datetime.timedelta(days=7))
#         if self.ID != None:
#             self.ID = int(self.ID)
#
#         if self.mode=="NEW":
#             pass
#         else:
#             _,dic = GetDraftOrderDetailByID(self.log,WHICHDB,self.ID)
#             self.makeOrderDate = str2wxdate(dic["下单时间"])
#             self.bidDate = str2wxdate(dic["投标时间"])
#             self.orderName = dic["订单名称"]
#             self.customerName = dic["客户名称"]
#             self.customerInfo = dic["客户公司信息"]
#             self.contactsName = dic["联系人"]
#             self.phoneNumber = dic["联系人电话"]
#             self.email = dic["联系人邮箱"]
#             self.bidMode = dic["投标方式"]
#             self.bidMethod = dic["投标格式"]
#             self.techDrawingName = dic["客户原始技术图纸名"]
#             self.techDrawingName2 = dic["客户原始技术图纸名2"]
#             self.techDrawingName3 = dic["客户原始技术图纸名3"]
#             self.techDrawingName4 = dic["客户原始技术图纸名4"]
#             self.techCheckState = dic['设计审核状态']
#             self.techDrawingName = self.techDrawingName.strip("\"")
#             if self.techDrawingName2 == None:
#                 self.techDrawingName2 = ""
#             else:
#                 self.techDrawingName2 = self.techDrawingName2.strip("\"")
#             if self.techDrawingName3 == None:
#                 self.techDrawingName3 = ""
#             else:
#                 self.techDrawingName3 = self.techDrawingName3.strip("\"")
#             if self.techDrawingName4 == None:
#                 self.techDrawingName4 = ""
#             else:
#                 self.techDrawingName4 = self.techDrawingName4.strip("\"")
#
#         topsizer = wx.BoxSizer(wx.VERTICAL)
#
#         # Difference between using PropertyGridManager vs PropertyGrid is that
#         # the manager supports multiple pages and a description box.
#         self.pg = pg = wxpg.PropertyGridManager(panel,
#                         style=wxpg.PG_SPLITTER_AUTO_CENTER |
#                               wxpg.PG_AUTO_SORT |
#                               wxpg.PG_TOOLBAR)
#
#         # Show help as tooltips
#         pg.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS
#
#         # pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
#         # pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
#         # pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
#         # pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )
#
#
#
#         if not getattr(sys, '_PropGridEditorsRegistered', False):
#             pg.RegisterEditor(TrivialPropertyEditor)
#             pg.RegisterEditor(SampleMultiButtonEditor)
#             pg.RegisterEditor(TechDrawingButtonEditor)
#             pg.RegisterEditor(LargeImageEditor)
#             # ensure we only do it once
#             sys._PropGridEditorsRegistered = True
#
#         #
#         # Add properties
#         #
#         # NOTE: in this example the property names are used as variable names
#         # in one of the tests, so they need to be valid python identifiers.
#         #
#         pg.AddPage( "今日原材料价格" )
#         pg.Append( wxpg.PropertyCategory("1 - 基本原材料价格") )
#         pg.Append( wxpg.StringProperty("1. G",value=self.orderName) )
#         pg.Append( wxpg.StringProperty("2. PVC",value=self.customerName) )
#         pg.Append( wxpg.StringProperty("3. S.S (304)",value=self.customerInfo) )
#         pg.Append( wxpg.StringProperty("4. Painted",value=self.contactsName) )
#         pg.Append( wxpg.StringProperty("5. Rock wool (150Kg)",value=self.phoneNumber) )
#         pg.Append( wxpg.StringProperty("6. Rock wool (200Kg)",value=self.email))
#         pg.Append( wxpg.DateProperty("7. Glue (Jinjiang)",value=self.makeOrderDate) )
#         pg.Append( wxpg.DateProperty("8. Glue (Fuller)",value=self.makeOrderDate) )
#
#         pg.Append( wxpg.PropertyCategory("2 - 询价文件") )
#
#         pg.Append( wxpg.DateProperty("1.投标日期",value=self.bidDate) )
#         # pg.Append( wxpg.EnumProperty("2.投标方式","2.投标方式",
#         #                              BIDMODE,
#         #                              [0,1,2],
#         #                              BIDMODE.index(self.bidMode)) )
#         # pg.Append( wxpg.EnumProperty("3.投标格式","3.投标格式",
#         #                              BIDMETHOD,
#         #                              [0,1],
#         #                              BIDMETHOD.index(self.bidMethod)) )
#
#         pg.Append(wxpg.PropertyCategory("3 - 附件"))
#         if self.mode in ["NEW","EDIT"]:
#             pg.Append( wxpg.FileProperty("1.产品清单或图纸文件 *",value=self.techDrawingName) )
#             pg.Append( wxpg.FileProperty("2.产品清单或图纸文件",value=self.techDrawingName2) )
#             pg.Append( wxpg.FileProperty("3.产品清单或图纸文件",value=self.techDrawingName3) )
#             pg.Append( wxpg.FileProperty("4.产品清单或图纸文件",value=self.techDrawingName4) )
#
#             pg.SetPropertyAttribute( "1.产品清单或图纸文件 *", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
#             pg.SetPropertyAttribute( "2.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
#             pg.SetPropertyAttribute( "3.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
#             pg.SetPropertyAttribute( "4.产品清单或图纸文件", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
#             # pg.SetPropertyAttribute( "1.图纸文件 *", wxpg.PG_FILE_INITIAL_PATH,
#             #                          r"C:\Program Files\Internet Explorer" )
#             pg.SetPropertyAttribute( "1.投标日期", wxpg.PG_DATE_PICKER_STYLE,
#                                      wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY )
#             topsizer.Add(pg, 1, wx.EXPAND)
#             if self.character == "下单员":
#                 if self.ID != None:
#                     rowsizer = wx.BoxSizer(wx.HORIZONTAL)
#                     but = wx.Button(panel, -1, "保存修改", size=(-1, 35))
#                     but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditOkBTN)
#                     rowsizer.Add(but, 1)
#                     but = wx.Button(panel, -1, "取消修改", size=(-1, 35))
#                     but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditCancelBTN)
#                     rowsizer.Add(but, 1)
#                     topsizer.Add(rowsizer, 0, wx.EXPAND)
#                     rowsizer = wx.BoxSizer(wx.HORIZONTAL)
#                     but = wx.Button(panel, -1, "订单废弃", size=(-1, 35))
#                     but.Bind(wx.EVT_BUTTON, self.OnDraftOrderAbandonBTN)
#                     rowsizer.Add(but, 1)
#                     but = wx.Button(panel, -1, "订单投产", size=(-1, 35))
#                     # but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditCancelBTN)
#                     rowsizer.Add(but, 1)
#                     topsizer.Add(rowsizer, 0, wx.EXPAND)
#                     rowsizer = wx.BoxSizer(wx.HORIZONTAL)
#                     but = wx.Button(panel, -1, "生成报价单", size=(-1, 35))
#                     # but.Bind(wx.EVT_BUTTON, self.OnDraftOrderEditOkBTN)
#                     rowsizer.Add(but, 1)
#                     topsizer.Add(rowsizer, 0, wx.EXPAND)
#                     # btnsizer = wx.BoxSizer()
#                     # bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
#                     # bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
#                     # bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
#                     # btn_ok = wx.Button(self.orderEditPanel, wx.ID_OK, "确 认 修 改", size=(200, 50))
#                     # btn_ok.Bind(wx.EVT_BUTTON,self.OnDraftOrderEditOkBTN)
#                     # btn_ok.SetBitmap(bitmap1, wx.LEFT)
#                     # btnsizer.Add(btn_ok, 0)
#                     # btnsizer.Add((40, -1), 0)
#                     # sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
#                     # self.orderEditPanel.SetSizer(sizer)
#                     # sizer.Fit(self.orderEditPanel)
#         else:
#             techDrawingName = self.techDrawingName.split("\\")[-1]
#             techDrawingName = "%d."%self.ID+techDrawingName
#             techDrawingName2 = self.techDrawingName2.split("\\")[-1]
#             if techDrawingName2!="":
#                 techDrawingName2 = "%d."%self.ID+techDrawingName2
#             techDrawingName3 = self.techDrawingName3.split("\\")[-1]
#             if techDrawingName3!="":
#                 techDrawingName3 = "%d."%self.ID+techDrawingName3
#             techDrawingName4 = self.techDrawingName4.split("\\")[-1]
#             if techDrawingName4!="":
#                 techDrawingName4 = "%d."%self.ID+techDrawingName4
#             pg.Append( wxpg.LongStringProperty("1.产品清单或图纸文件 *",value=techDrawingName))
#             pg.SetPropertyEditor("1.产品清单或图纸文件 *", "TechDrawingButtonEditor")
#             pg.Append( wxpg.LongStringProperty("2.产品清单或图纸文件",value=techDrawingName2))
#             pg.SetPropertyEditor("2.产品清单或图纸文件", "SampleMultiButtonEditor")
#             pg.Append( wxpg.LongStringProperty("3.产品清单或图纸文件",value=techDrawingName3))
#             pg.SetPropertyEditor("3.产品清单或图纸文件", "SampleMultiButtonEditor")
#             pg.Append( wxpg.LongStringProperty("4.产品清单或图纸文件",value=techDrawingName4))
#             pg.SetPropertyEditor("4.产品清单或图纸文件", "SampleMultiButtonEditor")
#             topsizer.Add(pg, 1, wx.EXPAND)
#             rowsizer = wx.BoxSizer(wx.HORIZONTAL)
#             if self.character == "设计员":
#                 but = wx.Button(panel,-1,"开始设计部审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnStartTechCheck)
#                 rowsizer.Add(but,1)
#                 # but = wx.Button(panel,-1,"完成设计审核",size=(-1,35))
#                 # but.Bind( wx.EVT_BUTTON, self.OnFinishTechCheck)
#                 # rowsizer.Add(but,1)
#             elif self.character == "采购员":
#                 but = wx.Button(panel,-1,"开始采购部审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnStartPurchaseCheck)
#                 rowsizer.Add(but,1)
#                 but = wx.Button(panel,-1,"完成采购部审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnFinishPurchaseCheck)
#                 rowsizer.Add(but,1)
#             elif self.character == "财务":
#                 but = wx.Button(panel,-1,"开始财务部审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnStartFinancialCheck)
#                 rowsizer.Add(but,1)
#                 but = wx.Button(panel,-1,"完成财务部审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnFinishFinancialCheck)
#                 rowsizer.Add(but,1)
#             elif self.character == "经理":
#                 but = wx.Button(panel,-1,"开始经理审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnStartManagerCheck)
#                 rowsizer.Add(but,1)
#                 but = wx.Button(panel,-1,"完成经理审核",size=(-1,35))
#                 but.Bind( wx.EVT_BUTTON, self.OnFinishManagerCheck)
#                 rowsizer.Add(but,1)
#             topsizer.Add(rowsizer,0,wx.EXPAND)
#
#         panel.SetSizer(topsizer)
#         topsizer.SetSizeHints(panel)
#
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(panel, 1, wx.EXPAND)
#         self.SetSizer(sizer)
#         self.Layout()
#         self.Thaw()
#
#     def OnDraftOrderAbandonBTN(self,event):
#         dlg = wx.MessageDialog(self,"您确定要废弃此订单吗？","信息提示",style=wx.YES_NO)
#         if dlg.ShowModal() == wx.ID_YES:
#             pass
#             # if UpdateDraftOrderStateInDB(self.log,WHICHDB,self.ID,"废弃") == 0:
#             #     self.master.recreateEnable=True
#             #     self.master.ReCreate()
#             #     wx.MessageBox("订单已成功废弃，系统稍候刷新显示！","信息提示")
#             # else:
#             #     wx.MessageBox("订单废弃操作失败！","信息提示")
#         dlg.Destroy()
#
#     def OnDraftOrderEditCancelBTN(self,event):
#         self.ReCreate()
#
#
#     def OnFinishPurchaseCheck(self,event):
#         pass


class InputTodayPriceGrid(gridlib.Grid):
    def __init__(self, parent, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.parent = parent
        self.log = log
        data=GetMeterialPrice(self.log,WHICHDB)
        self.data=[]
        for dic in data:
            temp = []
            for section in MeterialCharacterList:
                temp.append(dic[section])
            self.data.append(temp)
        self.SetDefaultRowSize(30)
        self.colLabels = MeterialCharacterList
        self.colWidths = MeterialCharacterWidthList
        self.CreateGrid(len(self.data), len(self.colLabels))#, gridlib.Grid.SelectRows)
        self.SetRowLabelSize(80)
        self.SetColLabelSize(40)
        self.SetMargins(0,0)
        self.AutoSizeColumns(False)
        # self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChanged)
        font = self.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        attr = gridlib.GridCellAttr()
        attr.SetFont(font)
        attr.SetBackgroundColour(wx.LIGHT_GREY)
        attr.SetReadOnly(True)
        attr.SetAlignment(wx.RIGHT, -1)

        for i, title in enumerate(self.colLabels):
            self.SetColSize(i,self.colWidths[i])
            self.SetColLabelValue(i,title)
        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                self.SetCellAlignment(i,j,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
                # self.SetCellFont(i, j, wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
                if col == None:
                    col = ""
                self.SetCellValue(i,j,col)
                if j == 8:
                    self.SetCellEditor(i,j, gridlib.GridCellFloatEditor(-1,2))
                # self.SetCellBackgroundColour(i, j, wx.BLUE)
        for j in range(len(self.colLabels)):
            self.SetCellAlignment(len(self.data),j,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
            if j!= 3:
                self.SetColAttr(j, attr)
        # attr.IncRef()

    def OnCellChanged(self,event):
        row = event.GetRow()
        col = event.GetCol()
        # event.Skip()
        a = float(self.GetCellValue(row,col-1))
        b = float(self.GetCellValue(row,col))
        self.SetCellValue(row,col+1,str(a*b))
    # def OnLeftDClick(self, evt):
    #     if self.CanEnableCellControl():
    #         self.EnableCellEditControl()


class MeterialPriceManagementPanel(wx.Panel):
    def __init__(self, parent, log):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        self.log = log


class InputTodayPriceDialog(wx.Dialog):
    def __init__(self, parent, log):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "录入原材料今日价格对话框", pos=wx.DefaultPosition ,size=(1000,600))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self,size=(1000,500))
        sizer.Add(self.panel,1,wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.Bind(wx.EVT_BUTTON,self.OnOK)
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        hbox=wx.BoxSizer()
        self.todayPriceGrid = InputTodayPriceGrid(self.panel, self.log)
        hbox.Add(self.todayPriceGrid,1,wx.EXPAND)
        self.panel.SetSizer(hbox)

    def OnOK(self,event):
        self.Save()
        event.Skip()

    def Save(self):
        data=[]
        error=False
        rowNum = self.todayPriceGrid.GetNumberRows()
        colNum = self.todayPriceGrid.GetNumberCols()
        print("rowNum=",rowNum)
        for i in range(rowNum):
            temp = []
            for j in range(colNum):
                temp.append(self.todayPriceGrid.GetCellValue(i,j))
            data.append(temp)
        print("data=",data)
        self.meterialPriceDicList = self.MakeDicListData(data)
        SaveMeterialTodayPriceInDB(self.log,WHICHDB,self.meterialPriceDicList)
        return False

    def MakeDicListData(self,data):
        dicList=[]
        sectionList=copy.deepcopy(MeterialCharacterList)
        dicList = [dict(zip(sectionList, row)) for row in data]
        return dicList

