import wx
import wx.grid as gridlib
from DBOperation import GetAllOrderList,GetOrderDetailRecord
from OrderDetailTree import OrderDetailTree
from ID_DEFINE import *
import numpy as np
import images
import copy

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
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)

        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)


    def OnCellLeftClick(self, evt):
        evt.Skip()

    def OnCellRightClick(self, evt):
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        evt.Skip()

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
            for j, item in enumerate(order[:8]):#z最后一列位子订单列表，不再grid上显示
                # self.SetCellBackgroundColour(i,j,wx.Colour(250, 250, 250))
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))

        # self.SetCellValue(2, 2, "Yet another cell")
        # self.SetCellValue(3, 3, "This cell is read-only")
        # self.SetCellFont(0, 0, wx.Font(12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        # self.SetCellTextColour(1, 1, wx.RED)
        # self.SetCellBackgroundColour(2, 2, wx.CYAN)
        # self.SetReadOnly(3, 3, True)

        # self.SetCellEditor(5, 0, gridlib.GridCellNumberEditor(1,1000))
        # self.SetCellValue(5, 0, "123")
        # self.SetCellEditor(6, 0, gridlib.GridCellFloatEditor())
        # self.SetCellValue(6, 0, "123.34")
        # self.SetCellEditor(7, 0, gridlib.GridCellNumberEditor())
        #
        # self.SetCellValue(6, 3, "You can veto editing this cell")

        # attribute objects let you keep a set of formatting values
        # in one spot, and reuse them if needed
        # attr = gridlib.GridCellAttr()
        # attr.SetTextColour(wx.BLACK)
        # attr.SetBackgroundColour(wx.RED)
        # attr.SetFont(wx.Font(10, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        #
        # # you can set cell attributes for the whole row (or column)
        # self.SetRowAttr(5, attr)

        # self.SetDefaultCellOverflow(False)
        # r = gridlib.GridCellAutoWrapStringRenderer()
        # self.SetCellRenderer(9, 1, r)

        # overflow cells
        # self.SetCellValue( 9, 1, "This default cell will overflow into neighboring cells, but not if you turn overflow off.");
        # self.SetCellSize(11, 1, 3, 3);
        # self.SetCellAlignment(11, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE);
        # self.SetCellValue(11, 1, "This cell is set to span 3 rows and 3 columns");

        # editor = gridlib.GridCellTextEditor()
        # editor.SetParameters('10')
        # self.SetCellEditor(0, 4, editor)
        # self.SetCellValue(0, 4, "Limited text")
        #
        # renderer = gridlib.GridCellAutoWrapStringRenderer()
        # self.SetCellRenderer(15,0, renderer)
        # self.SetCellValue(15,0, "The text in this cell will be rendered with word-wrapping")

        # test all the events
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.OnCellRightClick)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Bind(gridlib.EVT_GRID_CELL_RIGHT_DCLICK, self.OnCellRightDClick)

        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_CLICK, self.OnLabelRightClick)
        self.Bind(gridlib.EVT_GRID_LABEL_LEFT_DCLICK, self.OnLabelLeftDClick)
        self.Bind(gridlib.EVT_GRID_LABEL_RIGHT_DCLICK, self.OnLabelRightDClick)

        self.Bind(gridlib.EVT_GRID_COL_SORT, self.OnGridColSort)

        self.Bind(gridlib.EVT_GRID_ROW_SIZE, self.OnRowSize)
        self.Bind(gridlib.EVT_GRID_COL_SIZE, self.OnColSize)

        self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnRangeSelect)
        self.Bind(gridlib.EVT_GRID_CELL_CHANGED, self.OnCellChange)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)

        self.Bind(gridlib.EVT_GRID_EDITOR_SHOWN, self.OnEditorShown)
        self.Bind(gridlib.EVT_GRID_EDITOR_HIDDEN, self.OnEditorHidden)
        self.Bind(gridlib.EVT_GRID_EDITOR_CREATED, self.OnEditorCreated)
        self.Thaw()

    def ReCreate(self):
        self.Freeze()
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
            for j, item in enumerate(order):
                self.SetCellAlignment(i, j, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
                self.SetCellValue(i, j, str(item))
        self.Thaw()

    def OnCellLeftClick(self, evt):
        self.log.write("OnCellLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightClick(self, evt):
        self.log.write("OnCellRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellLeftDClick(self, evt):
        self.log.write("OnCellLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnCellRightDClick(self, evt):
        self.log.write("OnCellRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftClick(self, evt):
        self.log.write("OnLabelLeftClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightClick(self, evt):
        self.log.write("OnLabelRightClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelLeftDClick(self, evt):
        self.log.write("OnLabelLeftDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnLabelRightDClick(self, evt):
        self.log.write("OnLabelRightDClick: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnGridColSort(self, evt):
        self.log.write("OnGridColSort: %s %s" % (evt.GetCol(), self.GetSortingColumn()))
        self.SetSortingColumn(evt.GetCol())

    def OnRowSize(self, evt):
        self.log.write("OnRowSize: row %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnColSize(self, evt):
        self.log.write("OnColSize: col %d, %s\n" %
                       (evt.GetRowOrCol(), evt.GetPosition()))
        evt.Skip()

    def OnRangeSelect(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnRangeSelect: %s  top-left %s, bottom-right %s\n" %
                       (msg, evt.GetTopLeftCoords(), evt.GetBottomRightCoords()))
        evt.Skip()

    def OnCellChange(self, evt):
        self.log.write("OnCellChange: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Show how to stay in a cell that has bad data.  We can't just
        # call SetGridCursor here since we are nested inside one so it
        # won't have any effect.  Instead, set coordinates to move to in
        # idle time.
        value = self.GetCellValue(evt.GetRow(), evt.GetCol())

        if value == 'no good':
            self.moveTo = evt.GetRow(), evt.GetCol()

    def OnIdle(self, evt):
        if self.moveTo is not None:
            self.SetGridCursor(self.moveTo[0], self.moveTo[1])
            self.moveTo = None

        evt.Skip()

    def OnSelectCell(self, evt):
        if evt.Selecting():
            msg = 'Selected'
        else:
            msg = 'Deselected'
        self.log.write("OnSelectCell: %s (%d,%d) %s\n" %
                       (msg, evt.GetRow(), evt.GetCol(), evt.GetPosition()))

        # Another way to stay in a cell that has a bad value...
        row = self.GetGridCursorRow()
        col = self.GetGridCursorCol()

        if self.IsCellEditControlEnabled():
            self.HideCellEditControl()
            self.DisableCellEditControl()

        value = self.GetCellValue(row, col)

        if value == 'no good 2':
            return  # cancels the cell selection

        evt.Skip()

    def OnEditorShown(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to edit this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorShown: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorHidden(self, evt):
        if evt.GetRow() == 6 and evt.GetCol() == 3 and \
                wx.MessageBox("Are you sure you wish to  finish editing this cell?",
                              "Checking", wx.YES_NO) == wx.NO:
            evt.Veto()
            return

        self.log.write("OnEditorHidden: (%d,%d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetPosition()))
        evt.Skip()

    def OnEditorCreated(self, evt):
        self.log.write("OnEditorCreated: (%d, %d) %s\n" %
                       (evt.GetRow(), evt.GetCol(), evt.GetControl()))

class OrderManagementPanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.Freeze()
        self.master = master
        self.log = log
        self.busy = False
        self.showRange=[]
        self.colLabelValueList = ["订单编号","订单名称","总价","产品数量","订单交货日期","下单时间","下单员","订单状态"]
        self.colWidthList = [60, 65,50, 60, 85, 75, 60, 60]
        self.orderDetailData = []
        _, orderList = GetAllOrderList(self.log, 1)
        self.dataArray = np.array(orderList)
        self.data = []
        self.orderIDSearch=''
        self.orderStateSearch=''
        self.productNameSearch=''
        self.operatorSearch=''
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(580, -1))
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
        self.Thaw()

    def ReCreateOrderDetailTree(self):
        self.Freeze()
        self.orderDetailTreePanel.Freeze()
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
        self.orderDetailTree.Thaw()
        self.Thaw()

    def OnCellLeftClick(self,event):
        if self.busy == False:
            row = event.GetRow()
            self.orderGrid.SetSelectionMode(wx.grid.Grid.GridSelectRows)
            self.orderGrid.SelectRow(row)
            self.data=self.dataArray[row]
            # self.ReCreateMiddlePanel(self.type, self.editState)
            self.ReCreateRightPanel()
            _,self.orderDetailData = GetOrderDetailRecord(self.log,1,self.data[0])
            if len(self.orderDetailData)==0:
                self.treeStructure =[]
            else:
                self.treeStructure = self.TreeDataTransform()
            self.ReCreateOrderDetailTree()
            self.master.mainPANEL.orderData = self.dataArray[row]
            self.master.mainPANEL.orderState = "接单"
            self.master.mainPANEL.ReCreateOrderInfoPanel()
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
        self.orderDetailPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.orderDetailPanel,"订单详情")
        self.orderExcelPanel = wx.Panel(self.notebook)
        self.notebook.AddPage(self.orderExcelPanel,"订单原始Excel")
        self.rightPanel.Layout()
        self.orderDetailTreePanel=wx.Panel(self.orderDetailPanel,size=(260,-1))
        self.orderDetailGridPanel=wx.Panel(self.orderDetailPanel,size=(100,-1),style=wx.BORDER_THEME)
        hbox = wx.BoxSizer()
        hbox.Add(self.orderDetailTreePanel,0,wx.EXPAND)
        hbox.Add(self.orderDetailGridPanel,1,wx.EXPAND)
        self.orderDetailPanel.SetSizer(hbox)
        self.orderDetailPanel.Layout()
        self.rightPanel.Thaw()

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
