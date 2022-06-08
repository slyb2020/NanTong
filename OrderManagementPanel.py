import wx
import wx.grid as gridlib
from DBOperation import GetAllOrderAllInfo,GetAllOrderList,GetOrderDetailRecord,InsertNewOrder,GetStaffInfoWithID,\
    GetDraftOrderDetailByID,UpdateDraftOrderInfoByID,GetTechDrawingDataByID,GetPDF
from BluePrintManagementPanel import BluePrintShowPanel
from OrderDetailTree import OrderDetailTree
from ID_DEFINE import *
import numpy as np
import images
import copy
from SetupPropertyDialog import *
import datetime
from DateTimeConvert import *
import json
from operator import itemgetter

class OrderDetailGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, master, log):
        gridlib.Grid.__init__(self, parent, -1)
        ##mixins.GridAutoEditMixin.__init__(self)
        self.log = log
        self.master = master
        self.moveTo = None
        if self.master.showRange==[]:
            self.data = np.array(self.master.orderDetailData)[:,2:]
            self.titleList = orderDetailLabelList[2:]
            self.colSizeList = orderDetailColSizeList[2:]
        elif self.master.showRange[0]=="子订单":
            self.data=[]
            for data in self.master.orderDetailData:
                if str(data[2])==str(self.master.showRange[1]):
                    self.data.append(data)
            self.data = np.array(self.data)[:,3:]
            self.titleList = orderDetailLabelList[3:]
            self.colSizeList = orderDetailColSizeList[3:]
        elif self.master.showRange[0]=="甲板订单":
            self.data=[]
            for data in self.master.orderDetailData:
                if str(data[2])==str(self.master.showRange[1]) and str(data[3])==str(self.master.showRange[2]):
                    self.data.append(data)
            self.data = np.array(self.data)[:,4:]
            self.titleList = orderDetailLabelList[4:]
            self.colSizeList = orderDetailColSizeList[4:]
        elif self.master.showRange[0]=="区域订单":
            self.data=[]
            for data in self.master.orderDetailData:
                if str(data[2])==str(self.master.showRange[1]) and str(data[3])==str(self.master.showRange[2]) and str(data[4])==str(self.master.showRange[3]):
                    self.data.append(data)
            self.data = np.array(self.data)[:,5:]
            self.titleList = orderDetailLabelList[5:]
            self.colSizeList = orderDetailColSizeList[5:]
        elif self.master.showRange[0]=="房间订单":
            self.data=[]
            for data in self.master.orderDetailData:
                if str(data[2])==str(self.master.showRange[1]) and str(data[3])==str(self.master.showRange[2]) and str(data[4])==str(self.master.showRange[3]) and str(data[5])==str(self.master.showRange[4]):
                    self.data.append(data)
            self.data = np.array(self.data)[:,6:]
            self.titleList = orderDetailLabelList[6:]
            self.colSizeList = orderDetailColSizeList[6:]

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.CreateGrid(self.data.shape[0], self.data.shape[1])#, gridlib.Grid.SelectRows)
        for i in range(self.data.shape[1]):
            self.SetColLabelSize(25)
            self.SetColSize(i, self.colSizeList[i])
            self.SetColLabelValue(i,self.titleList[i])
        for rowNum,row in enumerate(self.data):
            self.SetRowLabelSize(40)
            self.SetRowLabelValue(rowNum,str(rowNum+1))
            for colNum,col in enumerate(row):
                self.SetCellAlignment(rowNum,colNum,wx.ALIGN_CENTRE,wx.ALIGN_CENTRE)
                self.SetCellValue(rowNum,colNum,str(col))
        ##self.EnableEditing(False)

        # # simple cell formatting
        # self.SetColSize(3, 200)
        # self.SetRowSize(4, 45)
        # self.SetCellValue(0, 0, "First cell")
        # self.SetCellValue(1, 1, "Another cell")
        # self.SetCellValue(2, 2, "Yet another cell")
        # self.SetCellValue(3, 3, "This cell is read-only")
        # self.SetCellFont(0, 0, wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        # self.SetCellTextColour(1, 1, wx.RED)
        # self.SetCellBackgroundColour(2, 2, wx.CYAN)
        # self.SetReadOnly(3, 3, True)
        #
        # self.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.SetCellValue(5, 0, "123")
        # self.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.SetCellValue(6, 0, "123.34")
        # self.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        #
        # self.SetCellValue(6, 3, "You can veto editing this cell")
        #
        # #self.SetRowLabelSize(0)
        # #self.SetColLabelSize(0)
        #
        # # attribute objects let you keep a set of formatting values
        # # in one spot, and reuse them if needed
        # attr = gridlib.GridCellAttr()
        # attr.SetTextColour(wx.BLACK)
        # attr.SetBackgroundColour(wx.RED)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #
        # # you can set cell attributes for the whole row (or column)
        # self.SetRowAttr(5, attr)
        #
        # self.SetColLabelValue(0, "Custom")
        # self.SetColLabelValue(1, "column")
        # self.SetColLabelValue(2, "labels")
        #
        # self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_BOTTOM)
        #
        # #self.SetDefaultCellOverflow(False)
        # #r = gridlib.GridCellAutoWrapStringRenderer()
        # #self.SetCellRenderer(9, 1, r)
        #
        # # overflow cells
        # self.SetCellValue( 9, 1, "This default cell will overflow into neighboring cells, but not if you turn overflow off.");
        # self.SetCellSize(11, 1, 3, 3);
        # self.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        # self.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns");
        #
        #
        # editor = gridlib.GridCellTextEditor()
        # editor.SetParameters('10')
        # self.SetCellEditor(0, 4, editor)
        # self.SetCellValue(0, 4, "Limited text")
        #
        # renderer = gridlib.GridCellAutoWrapStringRenderer()
        # self.SetCellRenderer(15,0, renderer)
        # self.SetCellValue(15,0, "The text in this cell will be rendered with word-wrapping")
        #
        #
        # # test all the events
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        # self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        # self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)
        #
        # self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        # self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        # self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        # self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)
        #
        # self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)
        #
        # self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        # self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)
        #
        # self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        # self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        # self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        # self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        # self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)


    def OnCellLeftClick(self, event):
        row = event.GetRow()
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.SelectRow(row)

    def OnCellRightClick(self, evt):
        evt.Skip()

    def OnCellLeftDClick(self, event):
        row = event.GetRow()
        col = event.GetCol()
        self.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.SelectRow(row)
        if self.GetColLabelValue(col)=="图纸":
            bluePrintName = self.GetCellValue(row,col)

    def OnCellRightDClick(self, evt):
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        evt.Skip()

    def OnLabelRightClick(self, evt):
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        evt.Skip()

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

    def OnRowSize(self, evt):
        evt.Skip()

    def OnColSize(self, evt):
        evt.Skip()

    def OnRangeSelect(self, evt):
        evt.Skip()


    def OnCellChange(self, evt):
        evt.Skip()


    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()


    def OnSelectCell(self, evt):
        evt.Skip()


    def OnEditorShown(self, evt):
        evt.Skip()


    def OnEditorCreated(self, evt):
        evt.Skip

class OrderGrid(gridlib.Grid):  ##, mixins.GridAutoEditMixin):
    def __init__(self, parent, master, log):
        gridlib.Grid.__init__(self, parent, -1)
        self.Freeze()
        self.log = log
        self.master = master
        self.moveTo = None

        self.Bind(wx.EVT_IDLE, self.OnIdle)

        self.CreateGrid(self.master.dataArray.shape[0], len(self.master.colLabelValueList))  # , gridlib.Grid.SelectRows)
        self.EnableEditing(False)

        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i,title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)

        for i, order in enumerate(self.master.dataArray):
            self.SetRowSize(i, 25)
            print("order=",order)
            for j, item in enumerate(order):#z最后一列位子订单列表，不再grid上显示
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))
                if int(order[0])<2:
                    self.SetCellBackgroundColour(i,j,wx.RED)
                elif int(order[0])<5:
                    self.SetCellBackgroundColour(i,j,wx.YELLOW)

        # self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
        # self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        # self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        # self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        self.Thaw()

    def ReCreate(self):
        self.ClearGrid()
        self.EnableEditing(False)
        if self.GetNumberRows()<self.master.dataArray.shape[0]:
            self.InsertRows(0,self.master.dataArray.shape[0]-self.GetNumberRows())
        self.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)

        self.SetRowLabelSize(50)
        self.SetColLabelSize(25)

        for i, title in enumerate(self.master.colLabelValueList):
            self.SetColLabelValue(i,title)
        for i, width in enumerate(self.master.colWidthList):
            self.SetColSize(i, width)
        for i, order in enumerate(self.master.dataArray[:,:7]):
            self.SetRowSize(i, 25)
            print("order=",order)
            for j, item in enumerate(order):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))
                if int(order[0])<2:
                    self.SetCellBackgroundColour(i,j,wx.RED)
                elif int(order[0])<5:
                    self.SetCellBackgroundColour(i,j,wx.YELLOW)


    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

class OrderManagementPanel(wx.Panel):
    def __init__(self, parent, master, log,type="草稿"):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
        self.type = type

    def ReCreate(self):
        self.Freeze()
        self.DestroyChildren()
        self.busy = False
        self.showRange=[]
        # if self.parent.master.operatorCharacter=="下单员":
        if self.type == "草稿":
            self.colLabelValueList = ["剩余时间","订单编号","订单名称","总价","产品数量","投标日期","下单日期","下单员","订单状态","技术审核","采购审核","财务审核","经理审核"]
            self.colWidthList =      [60,    60,          80,      70,    60,      85,       85,      60,     60,      60,       60,       60,       60]
        elif self.type =="在产":
            self.colLabelValueList = ["序号","订单编号","订单名称","总价","产品数量","订单交货日期","下单时间","下单员","订单状态"]
            self.colWidthList =      [60,    60,       80,       70,   60,      85,          85,       85,    60]
        elif self.type =="完工":
            self.colLabelValueList = ["序号","订单编号","订单名称","总价","产品数量","订单交货日期","下单时间","下单员","订单状态"]
            self.colWidthList =      [60,    60,       80,       70,   60,      85,          85,       85,    60]
        elif self.type =="废弃":
            self.colLabelValueList = ["剩余时间","订单编号","订单名称","总价","产品数量","投标日期","下单日期","下单员","订单状态","技术审核","采购审核","财务审核","经理审核"]
            self.colWidthList =      [60,    60,          80,      70,    60,      85,       85,      60,     60,      60,       60,       60,       60]
        self.orderDetailData = []
        _, dataList = GetAllOrderAllInfo(self.log, WHICHDB,self.type)
        orderList=[]
        for record in dataList:#这个循环是吧要在grid中显示的数据排序，对其，内容规整好
            record = list(record)
            startDay = datetime.date.today()
            temp = record[4].split('-')
            endDay = datetime.date(year=int(temp[0]),month=int(temp[1]),day=int(temp[2]))
            # endDay = wxdate2pydate(json.loads(record[4]))
            # endDay = datetime.date.today()+datetime.timedelta(days=5)
            record.insert(0,(endDay-startDay).days)
            record[1]="%05d"%int(record[1])
            if record[3]=="":
                record[3]="暂无报价"
            if record[4]=='0':
                record[4]=""
            _, staffInfo = GetStaffInfoWithID(self.log, WHICHDB, record[7])
            record[7] = staffInfo[3]
            if self.type in ["草稿","废弃"]:
                record[9]="未审核" if record[9]=='N' else "审核通过"
                record[10]="未审核" if record[10]=='N' else "审核通过"
                record[11]="未审核" if record[11]=='N' else "审核通过"
                record[12]="未审核" if record[12]=='N' else "审核通过"
            orderList.append(record)
        orderList.sort(key=itemgetter(0), reverse=False)

        self.dataArray = np.array(orderList)
        self.data = []
        self.orderIDSearch=''
        self.orderStateSearch=''
        self.productNameSearch=''
        self.operatorSearch=''
        hbox = wx.BoxSizer()
        size=(1000,-1)
        if self.type in ["草稿","废弃"]:
            size=(920,-1)
        elif self.type in ["在产","完工"]:
            size=(710,-1)
        self.leftPanel = wx.Panel(self, size=size)
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.rightPanel = wx.Panel(self, style=wx.BORDER_THEME)
        hbox.Add(self.rightPanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.orderGrid = OrderGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.orderGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)
        self.orderIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER )
        self.orderIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnOrderIDSearch)
        hhbox.Add(self.orderIDSearchCtrl, 0, wx.EXPAND)
        self.customerNameSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1))
        # self.customerNameSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOrderStateSearch)
        hhbox.Add(self.customerNameSearchCtrl, 0, wx.EXPAND)
        self.productNameSearchCtrl = wx.ComboBox(searchPanel, choices=['A1', 'B0', 'B1', 'B5', 'B7'],
                                                 size=(self.colWidthList[2], -1))
        self.productNameSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnProductNameSearch)
        hhbox.Add(self.productNameSearchCtrl, 0, wx.EXPAND)
        self.productAmountSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1))
        hhbox.Add(self.productAmountSearchCtrl, 0, wx.EXPAND)
        self.deliverDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1))
        hhbox.Add(self.deliverDateSearchCtrl, 0, wx.EXPAND)
        self.orderDateSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[5], -1))
        hhbox.Add(self.orderDateSearchCtrl, 0, wx.EXPAND)
        self.operatorSearchCtrl = wx.ComboBox(searchPanel, choices=["1803089"], size=(self.colWidthList[6], -1))
        self.operatorSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOperatorSearch)
        hhbox.Add(self.operatorSearchCtrl, 0, wx.EXPAND)
        self.orderStateSearchCtrl = wx.ComboBox(searchPanel, choices=["接单","排产","下料","加工","打包","发货"], size=(self.colWidthList[7], -1))
        self.orderStateSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnOrderStateSearch)
        hhbox.Add(self.orderStateSearchCtrl, 0, wx.EXPAND)

        # for i,width in enumerate(self.colWidthList):
        #     if i==6:
        #         width+=55
        #     searchTXT = wx.TextCtrl(searchPanel, size=(width,-1))
        #     hhbox.Add(searchTXT, 0, wx.EXPAND)
        searchPanel.SetSizer(hhbox)
        # self.filter = wx.SearchCtrl(self.leftPanel, size=(200,-1), style=wx.TE_PROCESS_ENTER)
        # self.filter.ShowCancelButton(True)
        # hhbox.Add((1,-1))
        # hhbox.Add(self.filter,0)
        # vvbox.Add(hhbox,0,wx.EXPAND)
        self.leftPanel.SetSizer(vvbox)
        # self.filter.Bind(wx.EVT_TEXT, self.RecreateTree)
        # self.filter.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
        #                  lambda e: self.filter.SetValue(''))
        # self.filter.Bind(wx.EVT_TEXT_ENTER, self.OnSearch)
        # self.ReCreateRightPanel()
        self.orderGrid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Layout()
        self.Thaw()

    def ReCreateOrderDetailTree(self):
        self.orderDetailTreePanel.DestroyChildren()
        _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, self.data[0])
        if len(self.orderDetailData) == 0:
            self.treeStructure = []
        else:
            self.treeStructure = self.TreeDataTransform()
        self.orderDetailTree = OrderDetailTree(self.orderDetailTreePanel,self,self.log,self.data[0],self.treeStructure)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.orderDetailTree,1,wx.EXPAND)
        self.orderDetailTreePanel.SetSizer(vbox)
        self.orderDetailTreePanel.Layout()

    def ReCreateTechCheckPanel(self):
        self.orderTechCheckPanel.DestroyChildren()
        hbox = wx.BoxSizer()
        # self.techCheckInfoPanel = TechCheckInfoPanel(self.orderTechCheckPanel, self.log, size=(300, 100))
        self.techCheckInfoPanel = DraftOrderPanel(self.orderTechCheckPanel, self.log, size=(300, 600), mode="USE", ID = self.data[1])
        hbox.Add(self.techCheckInfoPanel,0,wx.EXPAND)
        self.orderTechCheckPanel.SetSizer(hbox)
        self.orderTechCheckPanel.Layout()

    def ReCreatePurchaseCheckPanel(self):
        self.orderPurchaseCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.orderPurchaseCheckPanel.SetSizer(vbox)
        self.orderPurchaseCheckPanel.Layout()

    def ReCreateFinancialCheckPanel(self):
        self.orderFinancialCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.orderFinancialCheckPanel.SetSizer(vbox)
        self.orderFinancialCheckPanel.Layout()

    def ReCreateManagerCheckPanel(self):
        self.orderManagerCheckPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.orderManagerCheckPanel.SetSizer(vbox)
        self.orderManagerCheckPanel.Layout()

    def OnCellLeftClick(self,event):
        row = event.GetRow()
        self.orderGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
        self.orderGrid.SelectRow(row)
        self.data = self.dataArray[row]
        if self.type == "草稿":
            self.ReCreateRightPanel()
            self.ReCreateTechCheckPanel()
            self.ReCreatePurchaseCheckPanel()
            self.ReCreateFinancialCheckPanel()
            self.ReCreateManagerCheckPanel()
        elif self.type in orderWorkingStateList:
            if self.busy == False:
                # self.ReCreateMiddlePanel(self.type, self.editState)
                self.ReCreateRightPanel()
                _,self.orderDetailData = GetOrderDetailRecord(self.log,1,self.data[0])
                if len(self.orderDetailData)==0:
                    self.treeStructure =[]
                else:
                    self.treeStructure = self.TreeDataTransform()
                self.ReCreateOrderDetailTree()
        event.Skip()

    def TreeDataTransform(self):
        orderTreeData = np.array(self.orderDetailData)
        subOrderIDList = list(orderTreeData[:,2])#提出所有子订单号组成列表
        subOrderIDList = list(set(subOrderIDList))#得到所有不重复的子订单号
        subOrderIDList.sort()
        result=copy.deepcopy(subOrderIDList)
        for subNum, subOrderID in enumerate(result):
            deckOrderIDList = []
            for data in orderTreeData:
                if str(data[2])==str(subOrderID):
                    deckOrderIDList.append(data[3])
            deckOrderIDList = list(set(deckOrderIDList))
            deckOrderIDList.sort()
            result[subNum]=deckOrderIDList
        deckOrderIDList = result
        result=copy.deepcopy(deckOrderIDList)
        for subNum,subOrderID in enumerate(result):
            for deckNum,deckOrderID in enumerate(subOrderID):
                zoneOrderIDList=[]
                for data in orderTreeData:
                    if str(data[2])==str(subOrderIDList[subNum]) and str(data[3])==str(deckOrderID):
                        zoneOrderIDList.append(data[4])
                zoneOrderIDList = list(set(zoneOrderIDList))
                zoneOrderIDList.sort()
                result[subNum][deckNum]=zoneOrderIDList
        zoneOrderIDList=result
        result=copy.deepcopy(zoneOrderIDList)
        for subNum,subOrderID in enumerate(result):
            for deckNum,deckOrderID in enumerate(subOrderID):
                for zoneNum,zoneOrderID in enumerate(deckOrderID):
                    roomOrderIDList=[]
                    for data in orderTreeData:
                        if str(data[2])==str(subOrderIDList[subNum]) and str(data[3])==str(deckOrderIDList[subNum][deckNum]) and str(data[4])==str(zoneOrderID):
                            roomOrderIDList.append(data[5])
                    roomOrderIDList = list(set(roomOrderIDList))
                    roomOrderIDList.sort()
                    result[subNum][deckNum][zoneNum]=roomOrderIDList
        roomOrderIDList=result
        return subOrderIDList,deckOrderIDList,zoneOrderIDList,roomOrderIDList

    def ReCreateRightPanel(self):
        self.rightPanel.Freeze()
        self.rightPanel.DestroyChildren()
        self.notebook = wx.Notebook(self.rightPanel, -1, size=(21, 21), style=
                                    # wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    # | wx.NB_MULTILINE
                                    )
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        hbox = wx.BoxSizer()
        hbox.Add(self.notebook, 1, wx.EXPAND)
        self.rightPanel.SetSizer(hbox)
        self.rightPanel.Layout()
        if self.type in orderWorkingStateList:
            self.orderDetailPanel = wx.Panel(self.notebook)
            self.notebook.AddPage(self.orderDetailPanel, "订单详情")
            self.orderExcelPanel = wx.Panel(self.notebook)
            self.notebook.AddPage(self.orderExcelPanel, "订单原始Excel")
            hbox = wx.BoxSizer()
            self.orderDetailTreePanel=wx.Panel(self.orderDetailPanel,size=(260,-1))
            self.orderDetailGridPanel=wx.Panel(self.orderDetailPanel,size=(100,-1),style=wx.BORDER_THEME)
            hbox.Add(self.orderDetailTreePanel,0,wx.EXPAND)
            hbox.Add(self.orderDetailGridPanel,1,wx.EXPAND)
            self.orderDetailPanel.SetSizer(hbox)
            self.orderDetailPanel.Layout()
        elif self.type=="草稿":
            if self.master.operatorCharacter=="下单员":
                self.orderEditPanel = wx.Panel(self.notebook,size=(260,-1))
                self.notebook.AddPage(self.orderEditPanel, "订单编辑")
                self.orderCheckPanel = wx.Panel(self.notebook,size=(260,-1))
                self.notebook.AddPage(self.orderCheckPanel, "订单部审核")
                self.ReCreateOrderEditPanel()
            self.orderTechCheckPanel = wx.Panel(self.notebook,size=(260,-1))
            self.notebook.AddPage(self.orderTechCheckPanel, "技术部审核")
            self.orderPurchaseCheckPanel = wx.Panel(self.notebook,size=(260,-1))
            self.notebook.AddPage(self.orderPurchaseCheckPanel, "采购部审核")
            self.orderFinancialCheckPanel = wx.Panel(self.notebook,size=(260,-1))
            self.notebook.AddPage(self.orderFinancialCheckPanel, "财务部审核")
            self.orderManagerCheckPanel = wx.Panel(self.notebook,size=(260,-1))
            self.notebook.AddPage(self.orderManagerCheckPanel, "经理审核")
        self.rightPanel.Thaw()

    def ReCreateOrderEditPanel(self):
        self.orderEditPanel.Freeze()
        self.orderEditPanel.DestroyChildren()
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.draftOrderEditPanel = DraftOrderPanel(self.orderEditPanel, self.log, size=(600, 600), mode="EDIT", ID = self.data[1])
        sizer.Add(self.draftOrderEditPanel, 1, wx.EXPAND)
        line = wx.StaticLine(self.orderEditPanel, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self.orderEditPanel, wx.ID_OK, "确 认 修 改", size=(200, 50))
        btn_ok.Bind(wx.EVT_BUTTON,self.OnDraftOrderEditOkBTN)
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.orderEditPanel.SetSizer(sizer)
        sizer.Fit(self.orderEditPanel)
        self.orderEditPanel.Thaw()

    def OnDraftOrderEditOkBTN(self,event):
        d = self.draftOrderEditPanel.pg.GetPropertyValues(inc_attributes=True)
        dic = {}
        for k, v in d.items():
            dic[k] = v

        # operatorID = self.parent.parent.operatorID
        for key in dic.keys():
            if dic[key]=="" and '*' in key:
                wx.MessageBox("%s不能为空，请重新输入！"%key)
                return
        code = UpdateDraftOrderInfoByID(self.log,WHICHDB,dic,self.data[1])
        if code>0:
            wx.MessageBox("更新成功！")
        else:
            wx.MessageBox("更新失败！")
        self.ReCreate()

    def ReCreteOrderDetailGridPanel(self):
        self.orderDetailGridPanel.Freeze()
        self.orderDetailGridPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.orderDetailGrid = OrderDetailGrid(self.orderDetailGridPanel,self,self.log)
        vbox.Add(self.orderDetailGrid,1,wx.EXPAND)
        self.orderDetailGridPanel.SetSizer(vbox)
        self.orderDetailGridPanel.Layout()
        self.orderDetailGridPanel.Thaw()

    def OnOrderStateSearch(self, event):
        self.orderStateSearch = self.orderStateSearchCtrl.GetValue()
        self.ReSearch()

    def OnOperatorSearch(self, event):
        self.operatorSearch = self.operatorSearchCtrl.GetValue()
        self.ReSearch()

    def OnOrderIDSearch(self, event):
        self.orderIDSearch = self.orderIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnProductNameSearch(self, event):
        self.productNameSearch=self.productNameSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, orderList = GetAllOrderList(self.log, 1)
        self.dataArray = np.array(orderList)
        if self.productNameSearch != '':
            orderList = []
            for order in self.dataArray:
                if order[2] == self.productNameSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.orderIDSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[0]) == self.orderIDSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.operatorSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[6]) == self.operatorSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        if self.orderStateSearch != '':
            orderList = []
            for order in self.dataArray:
                if str(order[7]) == self.orderStateSearch:
                    orderList.append(order)
            self.dataArray = np.array(orderList)
        self.orderGrid.ReCreate()

    def OnResetSearchItem(self,event):
        self.orderIDSearch=''
        self.orderIDSearchCtrl.SetValue('')
        self.productNameSearch= ''
        self.productNameSearchCtrl.SetValue('')
        self.productAmountSearchCtrl.SetValue('')
        self.deliverDateSearchCtrl.SetValue('')
        self.orderDateSearchCtrl.SetValue('')
        self.operatorSearch=''
        self.operatorSearchCtrl.SetValue('')
        self.orderStateSearch=''
        self.orderStateSearchCtrl.SetValue('')
        self.ReSearch()

class DraftOrderPanel(wx.Panel):
    def __init__( self, parent, log ,size,mode="NEW",ID=None):
        wx.Panel.__init__(self, parent, wx.ID_ANY,size=size)
        self.log = log
        self.mode = mode
        self.panel = panel = wx.Panel(self, wx.ID_ANY)

        self.orderName = ""
        self.customerName = ""
        self.customerInfo = ""
        self.contactsName = ""
        self.phoneNumber = ""
        self.email =""
        self.bidMode = BIDMODE[0]
        self.bidMethod = BIDMETHOD[0]
        self.techDrawingName = ""
        self.secureProtocolName = ""
        self.bidDocName = ""
        self.techRequireDocName = ""
        self.makeOrderDate = wx.DateTime.Now()
        self.bidDate = pydate2wxdate(datetime.date.today() + datetime.timedelta(days=7))
        if ID != None:
            ID = int(ID)

        if self.mode=="NEW":
            pass
        else:
            _,dic = GetDraftOrderDetailByID(self.log,WHICHDB,ID)
            self.makeOrderDate = str2wxdate(dic["下单时间"])
            self.bidDate = str2wxdate(dic["投标时间"])
            self.orderName = dic["订单名称"]
            self.customerName = dic["客户名称"]
            self.customerInfo = dic["客户公司信息"]
            self.contactsName = dic["联系人"]
            self.phoneNumber = dic["联系人电话"]
            self.email = dic["联系人邮箱"]
            self.bidMode = dic["投标方式"]
            self.bidMethod = dic["投标格式"]
            self.techDrawingName = dic["客户原始技术图纸名"]
            self.techDrawingName = self.techDrawingName.strip("\"")
            self.secureProtocolName = ""
            self.bidDocName = ""
            self.techRequireDocName = ""

        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.ExtraStyle |= wxpg.PG_EX_HELP_AS_TOOLTIPS

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )



        if not getattr(sys, '_PropGridEditorsRegistered', False):
            pg.RegisterEditor(TrivialPropertyEditor)
            pg.RegisterEditor(SampleMultiButtonEditor)
            pg.RegisterEditor(TechDrawingButtonEditor)
            pg.RegisterEditor(LargeImageEditor)
            # ensure we only do it once
            sys._PropGridEditorsRegistered = True

        #
        # Add properties
        #
        # NOTE: in this example the property names are used as variable names
        # in one of the tests, so they need to be valid python identifiers.
        #
        pg.AddPage( "订单部录入信息" )
        pg.Append( wxpg.PropertyCategory("1 - 订单基本信息") )
        pg.Append( wxpg.StringProperty("1.订单名称 *",value=self.orderName) )
        pg.Append( wxpg.StringProperty("2.客户单位名称",value=self.customerName) )
        pg.Append( wxpg.StringProperty("3.客户公司信息",value=self.customerInfo) )
        pg.Append( wxpg.StringProperty("4.联系人姓名",value=self.contactsName) )
        pg.Append( wxpg.StringProperty("5.联系人电话",value=self.phoneNumber) )
        pg.Append( wxpg.StringProperty("6.联系人email",value=self.email))
        pg.Append( wxpg.DateProperty("7.下单日期",value=self.makeOrderDate) )

        pg.Append( wxpg.PropertyCategory("2 - 询价文件") )

        pg.Append( wxpg.DateProperty("1.投标日期",value=self.bidDate) )
        pg.Append( wxpg.EnumProperty("2.投标方式","2.投标方式",
                                     BIDMODE,
                                     [0,1,2],
                                     BIDMODE.index(self.bidMode)) )
        pg.Append( wxpg.EnumProperty("3.投标格式","3.投标格式",
                                     BIDMETHOD,
                                     [0,1],
                                     BIDMETHOD.index(self.bidMethod)) )

        pg.Append(wxpg.PropertyCategory("3 - 附件"))
        if self.mode in ["NEW","EDIT"]:
            pg.Append( wxpg.FileProperty("1.图纸文件 *",value=self.techDrawingName) )
            pg.Append( wxpg.FileProperty("2.保密协议文档",value=self.secureProtocolName) )
            pg.Append( wxpg.FileProperty("3.邀标信息文档",value=self.bidDocName) )
            pg.Append( wxpg.FileProperty("4.技术要求文档",value=self.techRequireDocName) )

            pg.SetPropertyAttribute( "1.图纸文件 *", wxpg.PG_FILE_SHOW_FULL_PATH, 0 )
            # pg.SetPropertyAttribute( "1.图纸文件 *", wxpg.PG_FILE_INITIAL_PATH,
            #                          r"C:\Program Files\Internet Explorer" )
            pg.SetPropertyAttribute( "1.投标日期", wxpg.PG_DATE_PICKER_STYLE,
                                     wx.adv.DP_DROPDOWN|wx.adv.DP_SHOWCENTURY )
            topsizer.Add(pg, 1, wx.EXPAND)
        else:
            techDrawingName = self.techDrawingName.split("\\")[-1]
            techDrawingName = "%d."%ID+techDrawingName
            pg.Append( wxpg.LongStringProperty("1.技术图纸文件",value=techDrawingName))
            pg.SetPropertyEditor("1.技术图纸文件", "TechDrawingButtonEditor")
            pg.Append( wxpg.LongStringProperty("2.保密协议文档",value="1234.pdf"))
            pg.SetPropertyEditor("2.保密协议文档", "SampleMultiButtonEditor")
            pg.Append( wxpg.LongStringProperty("3.邀标信息文档",value="1234.pdf"))
            pg.SetPropertyEditor("3.邀标信息文档", "SampleMultiButtonEditor")
            pg.Append( wxpg.LongStringProperty("4.技术要求文档",value="1234.pdf"))
            pg.SetPropertyEditor("4.技术要求文档", "SampleMultiButtonEditor")
            topsizer.Add(pg, 1, wx.EXPAND)

        # pg.AddPage( "技术部审核信息" )
        # pg.Append( wxpg.PropertyCategory("1 - 订单基本信息2") )
        # sp = pg.Append( wxpg.StringProperty('StringProperty_as_Password', value='ABadPassword') )
        # sp.SetAttribute('Hint', 'This is a hint')
        # sp.SetAttribute('Password', True)
        #
        # pg.Append( wxpg.IntProperty("Int", value=100) )
        # self.fprop = pg.Append( wxpg.FloatProperty("Float", value=123.456) )
        # pg.Append( wxpg.BoolProperty("Bool", value=True) )
        # boolprop = pg.Append( wxpg.BoolProperty("Bool_with_Checkbox", value=True) )
        # pg.SetPropertyAttribute(
        #     "Bool_with_Checkbox",    # You can find the property by name,
        #     #boolprop,               # or give the property object itself.
        #     "UseCheckbox", True)     # The attribute name and value
        #
        # pg.Append( wxpg.PropertyCategory("2 - 询价文件2") )
        # _,minNum=GetPropertyVerticalCuttingParameter(self.log,1)
        # pg.Append( wxpg.IntProperty("启动纵切最小板材数",value=minNum) )
        # pg.SetPropertyEditor("启动纵切最小板材数","SpinCtrl")
        # _,pageRowNum=GetPropertySchedulePageRowNumber(self.log,1)
        # pg.Append( wxpg.IntProperty("任务单每页行数",value=pageRowNum) )
        # pg.SetPropertyEditor("任务单每页行数","SpinCtrl")
        # pg.Append( DirsProperty("墙角板型号列表",value=['2SG','2SD','2SE','2SH']) )
        #
        # pg.Append( wxpg.PropertyCategory("3 - 附件") )
        # pg.Append( wxpg.LongStringProperty("LongString",
        #     value="This is a\nmulti-line string\nwith\ttabs\nmixed\tin."))
        # pg.Append( wxpg.ArrayStringProperty("ArrayString",value=['A','B','C']) )
        #
        # pg.Append( wxpg.EnumProperty("Enum","Enum",
        #                              ['wxPython Rules',
        #                               'wxPython Rocks',
        #                               'wxPython Is The Best'],
        #                              [10,11,12],
        #                              0) )
        # pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
        #                                  ['A','B','C'],
        #                                  [0,1,2],
        #                                  "Text Not in List") )
        #
        # pg.Append( wxpg.DateProperty("Date",value=wx.DateTime.Now()) )
        # pg.Append( wxpg.FontProperty("Font",value=panel.GetFont()) )
        # pg.Append( wxpg.ColourProperty("Colour",
        #                                value=panel.GetBackgroundColour()) )
        # pg.Append( wxpg.SystemColourProperty("SystemColour") )
        # pg.Append( wxpg.ImageFileProperty("ImageFile") )
        # pg.Append( wxpg.MultiChoiceProperty("MultiChoice",
        #             choices=['wxWidgets','QT','GTK+']) )
        #
        # pg.Append( wxpg.PropertyCategory("4 - 财务部审核信息2") )
        # #pg.Append( wxpg.PointProperty("Point",value=panel.GetPosition()) )
        # pg.Append( SizeProperty("Size", value=panel.GetSize()) )
        # #pg.Append( wxpg.FontDataProperty("FontData") )
        # pg.Append( wxpg.IntProperty("IntWithSpin",value=256) )
        # pg.SetPropertyEditor("IntWithSpin","SpinCtrl")
        #
        # pg.Append( wxpg.PropertyCategory("5 - 经理审核信息2") )
        # pg.Append( IntProperty2("IntProperty2", value=1024) )
        #
        # pg.Append( PyObjectProperty("PyObjectProperty") )
        #
        # pg.Append( DirsProperty("Dirs1",value=['C:/Lib','C:/Bin']) )
        # pg.Append( DirsProperty("Dirs2",value=['/lib','/bin']) )
        #
        # # Test another type of delimiter
        # pg.SetPropertyAttribute("Dirs2", "Delimiter", '"')
        #
        # # SampleMultiButtonEditor
        # pg.Append( wxpg.LongStringProperty("MultipleButtons") )
        # pg.SetPropertyEditor("MultipleButtons", "SampleMultiButtonEditor")
        # pg.Append( SingleChoiceProperty("SingleChoiceProperty") )
        #
        # # Custom editor samples
        # prop = pg.Append( wxpg.StringProperty("StringWithCustomEditor",
        #                                       value="test value") )
        # pg.SetPropertyEditor(prop, "TrivialPropertyEditor")
        #
        # pg.Append( wxpg.ImageFileProperty("ImageFileWithLargeEditor") )
        # pg.SetPropertyEditor("ImageFileWithLargeEditor", "LargeImageEditor")




        # rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        # but = wx.Button(panel,-1,"SetPropertyValues")
        # but.Bind( wx.EVT_BUTTON, self.OnSetPropertyValues )
        # rowsizer.Add(but,1)
        # but = wx.Button(panel,-1,"GetPropertyValues")
        # but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues )
        # rowsizer.Add(but,1)
        # topsizer.Add(rowsizer,0,wx.EXPAND)
        # rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        # but = wx.Button(panel,-1,"GetPropertyValues(as_strings=True)")
        # but.Bind( wx.EVT_BUTTON, self.OnGetPropertyValues2 )
        # rowsizer.Add(but,1)
        # but = wx.Button(panel,-1,"AutoFill")
        # but.Bind( wx.EVT_BUTTON, self.OnAutoFill )
        # rowsizer.Add(but,1)
        # topsizer.Add(rowsizer,0,wx.EXPAND)
        # rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        # but = wx.Button(panel,-1,"Delete")
        # but.Bind( wx.EVT_BUTTON, self.OnDeleteProperty )
        # rowsizer.Add(but,1)
        # but = wx.Button(panel,-1,"Run Tests")
        # but.Bind( wx.EVT_BUTTON, self.RunTests )
        # rowsizer.Add(but,1)
        # topsizer.Add(rowsizer,0,wx.EXPAND)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def OnPropGridChange(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s changed to "%s"\n' % (p.GetName(),p.GetValueAsString()))

    def OnPropGridSelect(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s selected\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing selected\n')

    def OnDeleteProperty(self, event):
        p = self.pg.GetSelectedProperty()
        if p:
            self.pg.DeleteProperty(p)
        else:
            wx.MessageBox("First select a property to delete")

    def OnReserved(self, event):
        pass

    def OnSetPropertyValues(self,event):
        try:
            d = self.pg.GetPropertyValues(inc_attributes=True)

            ss = []
            for k,v in d.items():
                v = repr(v)
                if not v or v[0] != '<':
                    if k.startswith('@'):
                        ss.append('setattr(obj, "%s", %s)'%(k,v))
                    else:
                        ss.append('obj.%s = %s'%(k,v))

            with MemoDialog(self,
                    "Enter Content for Object Used in SetPropertyValues",
                    '\n'.join(ss)) as dlg:  # default_object_content1

                if dlg.ShowModal() == wx.ID_OK:
                    import datetime
                    sandbox = {'obj':ValueObject(),
                               'wx':wx,
                               'datetime':datetime}
                    exec_(dlg.tc.GetValue(), sandbox)
                    t_start = time.time()
                    #print(sandbox['obj'].__dict__)
                    self.pg.SetPropertyValues(sandbox['obj'])
                    t_end = time.time()
                    self.log.write('SetPropertyValues finished in %.0fms\n' %
                                   ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(inc_attributes=True)
            t_end = time.time()
            self.log.write('GetPropertyValues finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.items()]
            self.propertyDic={}
            for k,v in d.items():
                self.propertyDic[k]=v
            with MemoDialog(self,"GetPropertyValues Result",
                           'Contents of resulting dictionary:\n\n'+'\n'.join(ss)) as dlg:
                dlg.ShowModal()

        except:
            import traceback
            traceback.print_exc()

    def OnGetPropertyValues2(self,event):
        try:
            t_start = time.time()
            d = self.pg.GetPropertyValues(as_strings=True)
            t_end = time.time()
            self.log.write('GetPropertyValues(as_strings=True) finished in %.0fms\n' %
                           ((t_end-t_start)*1000.0))
            ss = ['%s: %s'%(k,repr(v)) for k,v in d.items()]
            with MemoDialog(self,"GetPropertyValues Result",
                           'Contents of resulting dictionary:\n\n'+'\n'.join(ss)) as dlg:
                dlg.ShowModal()
        except:
            import traceback
            traceback.print_exc()

    def OnAutoFill(self,event):
        try:
            with MemoDialog(self,"Enter Content for Object Used for AutoFill",default_object_content1) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    sandbox = {'object':ValueObject(),'wx':wx}
                    exec_(dlg.tc.GetValue(), sandbox)
                    t_start = time.time()
                    self.pg.AutoFill(sandbox['object'])
                    t_end = time.time()
                    self.log.write('AutoFill finished in %.0fms\n' %
                                   ((t_end-t_start)*1000.0))
        except:
            import traceback
            traceback.print_exc()

    def OnPropGridRightClick(self, event):
        p = event.GetProperty()
        if p:
            self.log.write('%s right clicked\n' % (event.GetProperty().GetName()))
        else:
            self.log.write('Nothing right clicked\n')

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()
        self.log.write('Page Changed to \'%s\'\n' % (self.pg.GetPageName(index)))

    def RunTests(self, event):
        pg = self.pg
        log = self.log

        # Validate client data
        log.write('Testing client data set/get')
        pg.SetPropertyClientData( "Bool", 1234 )
        if pg.GetPropertyClientData( "Bool" ) != 1234:
            raise ValueError("Set/GetPropertyClientData() failed")

        # Test setting unicode string
        log.write('Testing setting an unicode string value')
        pg.GetPropertyByName("String").SetValue(u"Some Unicode Text")

        #
        # Test some code that *should* fail (but not crash)
        try:
            if wx.GetApp().GetAssertionMode() == wx.PYAPP_ASSERT_EXCEPTION:
                log.write('Testing exception handling compliancy')
                a_ = pg.GetPropertyValue( "NotARealProperty" )
                pg.EnableProperty( "NotAtAllRealProperty", False )
                pg.SetPropertyHelpString("AgaintNotARealProperty",
                                         "Dummy Help String" )
        except:
            pass

        # GetPyIterator
        log.write('GetPage(0).GetPyIterator()\n')
        it = pg.GetPage(0).GetPyIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # VIterator
        log.write('GetPyVIterator()\n')
        it = pg.GetPyVIterator(wxpg.PG_ITERATE_ALL)
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Properties
        log.write('GetPage(0).Properties\n')
        it = pg.GetPage(0).Properties
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

        # Items
        log.write('GetPage(0).Items\n')
        it = pg.GetPage(0).Items
        for prop in it:
            log.write('Iterating \'%s\'\n' % (prop.GetName()))

class CreateNewOrderDialog(wx.Dialog):
    def __init__(self, parent,log, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.parent = parent
        self.log = log
        # self.log.WriteText("操作员：'%s' 开始执行库存参数设置操作。。。\r\n"%(self.parent.operator_name))
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "新建订单对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.propertyPanel = DraftOrderPanel(self, self.log, size=(600, 600))
        sizer.Add(self.propertyPanel,1,wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap(bitmapDir+"/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap(bitmapDir+"/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap(bitmapDir+"/33.png", wx.BITMAP_TYPE_PNG)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)

        btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()


    def OnOk(self, event):
        d = self.propertyPanel.pg.GetPropertyValues(inc_attributes=True)
        self.propertyDic = {}
        for k, v in d.items():
            self.propertyDic[k] = v

        operatorID = self.parent.parent.operatorID
        for key in self.propertyDic.keys():
            if self.propertyDic[key]=="" and '*' in key:
                wx.MessageBox("%s不能为空，请重新输入！"%key)
                return
        startDate = wxdate2pydate(self.propertyDic["7.下单日期"])
        endDate = wxdate2pydate(self.propertyDic["1.投标日期"])
        delta = (endDate-startDate).days
        if delta<5:
            wx.MessageBox("投标日期与下单日期太近，请修改后再试！")
            return
        # elif
        result = InsertNewOrder(self.log,1,self.propertyDic,operatorID)
        if result<0:
            wx.MessageBox("存储出错，请检查后重试！","系统提示")
        else:
            wx.MessageBox("操作成功！")

        # GetPDF(self.log,1)
        event.Skip()

class TechDrawingButtonEditor(wxpg.PGTextCtrlEditor):
    def __init__(self):
        wxpg.PGTextCtrlEditor.__init__(self)

    def CreateControls(self, propGrid, property, pos, sz):
        self.fileType = property.GetValue().split('.')[-1]
        self.fileName = property.GetValue().split('.')[-2]+'.'+self.fileType
        self.id = property.GetValue().split('.')[0]
        self.fileData = GetTechDrawingDataByID(None,WHICHDB,self.id)
        print("id=",self.id)
        # Create and populate buttons-subwindow
        buttons = wxpg.PGMultiButton(propGrid, sz)
        # Add two regular buttons
        buttons.AddButton("...")
        buttons.AddButton("A")
        # Add a bitmap button
        buttons.AddBitmapButton(wx.ArtProvider.GetBitmap(wx.ART_FOLDER))

        # Create the 'primary' editor control (textctrl in this case)
        wnd = super(TechDrawingButtonEditor, self).CreateControls(
                                   propGrid,
                                   property,
                                   pos,
                                   buttons.GetPrimarySize())
        wnd = wnd.GetPrimary()
        # Finally, move buttons-subwindow to correct position and make sure
        # returned wxPGWindowList contains our custom button list.
        buttons.Finalize(propGrid, pos);

        # We must maintain a reference to any editor objects we created
        # ourselves. Otherwise they might be freed prematurely. Also,
        # we need it in OnEvent() below, because in Python we cannot "cast"
        # result of wxPropertyGrid.GetEditorControlSecondary() into
        # PGMultiButton instance.
        self.buttons = buttons

        return wxpg.PGWindowList(wnd, buttons)

    def OnEvent(self, propGrid, prop, ctrl, event):
        if event.GetEventType() == wx.wxEVT_COMMAND_BUTTON_CLICKED:
            buttons = self.buttons
            evtId = event.GetId()

            if evtId == buttons.GetButtonId(0):
                # Do something when the first button is pressed
                wx.LogDebug("First button pressed")
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(1):
                # Do something when the second button is pressed
                with open("tmp.pdf", 'wb') as fp:
                    fp.write(self.fileData)
                    fp.close()
                if self.fileType == "pdf":
                    dlg = wx.Dialog(None,title="技术图纸",size=(1800,1000))
                    BluePrintShowPanel(dlg,None,"temp.pdf")
                    dlg.CenterOnScreen()
                    dlg.ShowModal()
                    dlg.Destroy()
                return False  # Return false since value did not change
            if evtId == buttons.GetButtonId(2):
                # Do something when the third button is pressed
                dlg = wx.DirDialog(None, "Choose a directory:",
                                   style=wx.DD_DEFAULT_STYLE
                                   # | wx.DD_DIR_MUST_EXIST
                                   # | wx.DD_CHANGE_DIR
                                   )

                # If the user selects OK, then we process the dialog's data.
                # This is done by getting the path data from the dialog - BEFORE
                # we destroy it.
                if dlg.ShowModal() == wx.ID_OK:
                    print('You selected: %s\n' % dlg.GetPath())
                    with open(dlg.GetPath()+"\\"+self.fileName, 'wb') as fp:
                        fp.write(self.fileData)
                        fp.close
                    wx.MessageBox("技术图纸已存储于%s"%(dlg.GetPath()+"\\"+self.fileName),"信息提示")
                # Only destroy a dialog after you're done with it.
                dlg.Destroy()
                return False  # Return false since value did not change

        return super(TechDrawingButtonEditor, self).OnEvent(propGrid, prop, ctrl, event)
