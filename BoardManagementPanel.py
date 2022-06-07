import wx
import wx.grid as gridlib
from DBOperation import GetAllBoardList, GetRGBWithRalID,GetAllColor
from ManufactureManagementPanel import OrderGrid
import numpy as np
import images
import wx.lib.scrolledpanel as scrolled
from ID_DEFINE import *


class ColorPalettePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, log):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.log = log
        # self.ReCreate()

    def ReCreate(self):
        self.Freeze()
        self.DestroyChildren()
        _, colorList = GetAllColor(self.log, 1)
        wsizer = wx.WrapSizer(orient=wx.VERTICAL)
        for color in colorList:
            btn = wx.Button(self, label=color[0], size=(70,30),name=str(color[1:4]))
            btn.SetBackgroundColour(wx.Colour(color[1],color[2],color[3]))
            btn.SetForegroundColour(wx.Colour(255-color[1],255-color[2],255-color[3]))
            btn.SetToolTip(color[4]+'('+color[5]+')')
            wsizer.Add(btn, 0)
        self.SetSizer(wsizer)
        self.SetAutoLayout(1)
        self.SetupScrolling()
        self.Thaw()

class PicShowPanel(wx.Panel):
    def __init__(self, parent,boardType,size):
        wx.Panel.__init__(self, parent, size=size, style=wx.BORDER_THEME)
        self.boardType = boardType
        self.SetAutoLayout(True)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnResize)

    def OnResize(self, evt):
        self.Refresh()

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.Brush("WHITE"))
        dc.Clear()
        x,y = self.GetClientSize()
        bmp = wx.Image(bitmapDir+'/%s.jpg'%self.boardType).Scale(width=x, height=y,
                                                  quality=wx.IMAGE_QUALITY_BOX_AVERAGE).ConvertToBitmap()
        dc.DrawBitmap(bmp, 0, 0, True)

class BoardGrid(OrderGrid):
    def __init__(self, parent, master, log):
        super(BoardGrid, self).__init__(parent, master, log)
        self.Render()

    def Render(self):
        for i in range(self.GetNumberRows()):
            self.SetCellBackgroundColour(i, 6, wx.Colour(255, 255, 255))#清第6列（RAL色卡列）
            self.SetCellBackgroundColour(i, 8, wx.Colour(255, 255, 255))#清第8列（编辑按钮列）
            self.SetCellBackgroundColour(i, 9, wx.Colour(255, 255, 255))#清第9列（编辑按钮列）

        for i, item in enumerate(self.master.dataArray):
            RalID = item[6]
            _, color = GetRGBWithRalID(self.log, 1, RalID)
            self.SetCellBackgroundColour(i, 6, wx.Colour(color[0], color[1], color[2]))
            self.SetCellTextColour(i, 6,wx.Colour( 255-color[0], 255-color[1], 255-color[2]))
            self.SetCellAlignment(i, 7, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE_VERTICAL)
            self.SetCellValue(i, 7, color[3])
            if item[7]=='在用':
                self.SetCellBackgroundColour(i, 8, wx.Colour(240,240,240))
            else:
                self.SetCellBackgroundColour(i, 8, wx.RED)
            self.SetCellAlignment(i, 8, wx.ALIGN_CENTER, wx.ALIGN_CENTRE_VERTICAL)
            self.SetCellValue(i, 8, item[7])
            self.SetCellBackgroundColour(i, 9, wx.Colour(210,210,210))
            self.SetCellAlignment(i, 9, wx.ALIGN_CENTER, wx.ALIGN_CENTRE_VERTICAL)
            self.SetCellValue(i, 9, '编辑')

class SpecificBoardManagementPanel(wx.Panel):
    def __init__(self, parent, master, log, boardType,state='在用'):
        wx.Panel.__init__(self, parent)
        self.Freeze()
        self.master = master
        self.log = log
        self.boardType = boardType
        self.state = state
        self.colWidthList = [50, 52, 51, 60, 110, 55, 75, 60, 35, 35]
        self.colLabelValueList = ['材质', '厚度', '规格', '单位重量', '支持部件', '支持宽度', 'RAL色号', '颜色名','状态','']
        _, boardList = GetAllBoardList(self.log, 1, self.boardType,state=self.state)
        self.dataArray = np.array(boardList)
        self.orderIDSearch = ''
        self.boardFormatSearch = ''
        self.boardMaterialSearch = ''
        self.boardDensitySearch = ''
        self.boardSupportComponentSearch=''
        self.boardSupportWidthSearch=''
        self.boardRALIDSearch = ''
        self.editBoardPanelOccupied = False
        hbox = wx.BoxSizer()
        self.leftPanel = wx.Panel(self, size=(650, -1))
        hbox.Add(self.leftPanel, 0, wx.EXPAND)
        self.middlePanel = wx.Panel(self, size=(260,-1), style=wx.BORDER_THEME)
        hbox.Add(self.middlePanel, 0, wx.EXPAND)
        self.colorPalettePanel = ColorPalettePanel(self, self.log)
        hbox.Add(self.colorPalettePanel, 1, wx.EXPAND)
        self.SetSizer(hbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.boardGrid = BoardGrid(self.leftPanel, self, self.log)
        vvbox.Add(self.boardGrid, 1, wx.EXPAND)
        hhbox = wx.BoxSizer()
        searchPanel = wx.Panel(self.leftPanel, size=(-1, 30), style=wx.BORDER_DOUBLE)
        vvbox.Add(searchPanel, 0, wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.searchResetBTN = wx.Button(searchPanel, label='Rest', size=(48, -1))
        self.searchResetBTN.Bind(wx.EVT_BUTTON, self.OnResetSearchItem)
        hhbox.Add(self.searchResetBTN, 0, wx.EXPAND)

        self.boardSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[0], -1), style=wx.TE_PROCESS_ENTER)
        self.boardSearchCtrl.Enable(False)
        hhbox.Add(self.boardSearchCtrl, 0, wx.EXPAND)

        self.boardFormatSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[1], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardFormatSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardFormatSearch)
        hhbox.Add(self.boardFormatSearchCtrl, 0, wx.EXPAND)

        self.boardMaterialSearchCtrl = wx.ComboBox(searchPanel, choices=['A1', 'B0', 'B1', 'B5', 'B7'],
                                                   size=(self.colWidthList[2], -1))
        self.boardMaterialSearchCtrl.Bind(wx.EVT_COMBOBOX, self.OnBoardMaterailSearch)
        hhbox.Add(self.boardMaterialSearchCtrl, 0, wx.EXPAND)

        self.boardDensitySearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[3], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardDensitySearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardDensitySearch)
        hhbox.Add(self.boardDensitySearchCtrl, 0, wx.EXPAND)

        self.boardSupportComponentSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[4], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardSupportComponentSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardSupportComponentSearch)
        hhbox.Add(self.boardSupportComponentSearchCtrl, 0, wx.EXPAND)

        self.boardSupportWidthSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[5], -1),
                                                 style=wx.TE_PROCESS_ENTER)
        self.boardSupportWidthSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardSupportWidthSearch)
        hhbox.Add(self.boardSupportWidthSearchCtrl, 0, wx.EXPAND)

        self.boardRALIDSearchCtrl = wx.TextCtrl(searchPanel, size=(self.colWidthList[6], -1), style=wx.TE_PROCESS_ENTER)
        self.boardRALIDSearchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnBoardRALIDSearch)
        hhbox.Add(self.boardRALIDSearchCtrl, 0, wx.EXPAND)

        self.newBoardBTN = wx.Button(searchPanel, label='新建%s基材' % self.boardType)
        self.newBoardBTN.SetBackgroundColour(wx.Colour(22, 211, 111))
        self.newBoardBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewBoard)
        hhbox.Add(self.newBoardBTN, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 1)

        self.changeStateBTN = wx.Button(searchPanel, size=(15,-1))
        self.changeStateBTN.Bind(wx.EVT_BUTTON, self.OnChangeState)
        if self.state == '在用':
            self.changeStateBTN.SetBackgroundColour(wx.GREEN)
        else:
            self.changeStateBTN.SetBackgroundColour(wx.RED)
        hhbox.Add(self.changeStateBTN,0,wx.EXPAND)
        # self.newBoardBTN.SetBackgroundColour(wx.Colour(22, 211, 111))
        # self.newBoardBTN.Bind(wx.EVT_BUTTON, self.OnCreateNewBoard)
        # hhbox.Add(self.newBoardBTN, 1, wx.EXPAND | wx.RIGHT | wx.LEFT, 1)
        searchPanel.SetSizer(hhbox)
        self.leftPanel.SetSizer(vvbox)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        self.picPanel = PicShowPanel(self.middlePanel, self.boardType,size=(300,200))
        vvbox.Add(self.picPanel,1,wx.EXPAND)
        self.editBoardPanel=wx.Panel(self.middlePanel,size=(300,290))
        vvbox.Add(self.editBoardPanel, 0, wx.EXPAND)
        self.middlePanel.SetSizer(vvbox)
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_DCLICK, self.OnCellLeftDClick)
        self.Thaw()

    def OnCellLeftDClick(self, evt):
        row = evt.GetRow()
        col = evt.GetCol()
        if col == 9:
            if self.editBoardPanelOccupied == False:
                self.editBoardPanelOccupied=True
                self.ReCreateEditBoardPanel(self.boardType,state='编辑')
            else:
                wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！","信息提示")
        # evt.Skip()

    def ReCreateEditBoardPanel(self,type, state='新建'):
        self.editBoardPanel.Freeze()
        self.editBoardPanel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        frame = wx.StaticBox(self.editBoardPanel, label="%s基材"%state,size=(200,200))
        vbox.Add(frame,1,wx.EXPAND|wx.ALL,5)
        self.editBoardPanel.SetSizer(vbox)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add((-1,20))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材类型：", size=(70,-1))
        self.editBoardTypeCombo = wx.ComboBox(frame,choices=["PVC",'不锈钢'],size=(130,-1))
        self.editBoardTypeCombo.SetValue(self.boardType)
        self.editBoardTypeCombo.Enable(False)
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardTypeCombo,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材厚度：", size=(70,-1))
        self.editBoardFormatTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardFormatTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="基材规格：", size=(70,-1))
        self.editBoardMaterialTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardMaterialTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="单位重量：", size=(70,-1))
        self.editBoardDensityTXT = wx.TextCtrl(frame,size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardDensityTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="支持组件：", size=(60,-1))
        self.editBoardSupportWallCHeck = wx.CheckBox(frame,label="墙板")
        self.editBoardSupportCeilingCHeck = wx.CheckBox(frame,label="天花板")
        self.editBoardSupportConnecterCHeck = wx.CheckBox(frame,label="构件")
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSupportWallCHeck, 1, wx.TOP,5)
        hhbox.Add(self.editBoardSupportCeilingCHeck, 1, wx.TOP,5)
        hhbox.Add(self.editBoardSupportConnecterCHeck, 1, wx.TOP,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="支持宽度：", size=(70,-1))
        self.editBoardSupportWidthTXT = wx.TextCtrl(frame, size=(130,-1))
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSupportWidthTXT,1,wx.RIGHT,5)
        vvbox.Add(hhbox)

        vvbox.Add((-1,5))
        hhbox = wx.BoxSizer()
        label = wx.StaticText(frame, label="颜色：", size=(40,-1))
        self.editBoardSelectColorBTN = wx.Button(frame, size=(80,26))
        self.editBoardSelectColorBTN.Bind(wx.EVT_BUTTON, self.OnSelectColorBTN)
        hhbox.Add((20,-1))
        hhbox.Add(label,0,wx.TOP,5)
        hhbox.Add(self.editBoardSelectColorBTN,0,wx.RIGHT,5)
        self.editBoardStateCombo = wx.ComboBox(frame,choices=["在用","停用"],size=(75,25))
        self.editBoardStateCombo.SetValue("在用")
        if state=='新建':
            self.editBoardStateCombo.Enable(False)
        hhbox.Add(self.editBoardStateCombo,0,wx.RIGHT,5)
        vvbox.Add(hhbox)
        vvbox.Add(wx.StaticLine(frame,size=(100,-1), style=wx.HORIZONTAL), 0,wx.EXPAND|wx.TOP|wx.BOTTOM,5)

        self.editBoardOkButton = wx.Button(frame, label="确定", size=(100,30))
        self.editBoardOkButton.Bind(wx.EVT_BUTTON, self.OnEditBoardOkButton)
        self.editBoardCancelButton = wx.Button(frame, label="取消", size=(100,30))
        self.editBoardCancelButton.Bind(wx.EVT_BUTTON, self.OnEditBoardCancelButton)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        hhbox.Add(self.editBoardOkButton)
        hhbox.Add((20,-1))
        hhbox.Add(self.editBoardCancelButton)
        vvbox.Add((-1,3))
        vvbox.Add(hhbox,0,wx.EXPAND)

        frame.SetSizer(vvbox)
        self.editBoardPanel.Layout()
        # self.colorPalettePanel.ReCreate()
        self.editBoardPanel.Thaw()

    def OnSelectColorBTN(self, event):
        self.colorPalettePanel.ReCreate()
        self.colorPalettePanel.Bind(wx.EVT_BUTTON, self.OnColorBTN)

    def OnColorBTN(self, event):
        obj = event.GetEventObject()
        ralCode = obj.GetLabel()
        color = eval(obj.GetName())
        self.editBoardSelectColorBTN.SetBackgroundColour(wx.Colour(color))
        self.editBoardSelectColorBTN.SetForegroundColour(wx.Colour(255-color[0],255-color[1],255-color[2]))
        self.editBoardSelectColorBTN.SetLabel(ralCode)


    def OnEditBoardCancelButton(self,event):
        dlg = wx.MessageDialog(self,"取消操作将导致之前的输入工作全部作废，您是否确认？",'信息提示',style=wx.YES_NO)
        if dlg.ShowModal() == wx.ID_YES:
            self.editBoardPanel.DestroyChildren()
            self.colorPalettePanel.DestroyChildren()
            self.editBoardPanelOccupied = False
        dlg.Destroy()

    def OnEditBoardOkButton(self,event):
        self.editBoardPanel.DestroyChildren()
        self.colorPalettePanel.DestroyChildren()
        self.editBoardPanelOccupied = False

    def OnChangeState(self,event):
        if self.state == '在用':
            self.state = '停用'
            self.changeStateBTN.SetBackgroundColour(wx.RED)
        elif self.state == '停用':
            self.state = '全部'
            self.changeStateBTN.SetBackgroundColour(wx.YELLOW)
        else:
            self.state = '在用'
            self.changeStateBTN.SetBackgroundColour(wx.GREEN)
        _, orderList = GetAllBoardList(self.log, 1, self.boardType,state=self.state)
        self.dataArray = np.array(orderList)
        self.boardGrid.ReCreate()
        self.boardGrid.Render()

    def OnCreateNewBoard(self,event):
        if self.editBoardPanelOccupied == False:
            self.editBoardPanelOccupied = True
            self.ReCreateEditBoardPanel(self.boardType)
        else:
            wx.MessageBox("请先结束当前编辑工作后，再进行新的编辑操作！", "信息提示")
        # hhbox = wx.BoxSizer()
        # self.finishNewBoardBTN = wx.Button(self.editBoardPanel)
        # self.finishNewBoardBTN.Bind(wx.EVT_BUTTON,self.OnFinishNewBoard)
        # hhbox.Add(self.finishNewBoardBTN,0)
        # self.editBoardPanel.SetSizer(hhbox)
        # self.editBoardPanel.Layout()
        # self.colorPalettePanel.ReCreate()

    # def OnFinishNewBoard(self,event):
    #     self.colorPalettePanel.DestroyChildren()
    #     self.editBoardPanel.DestroyChildren()
    #     self.editBoardPanelOccupied = False

    def OnBoardDensitySearch(self, event):
        self.boardDensitySearch = self.boardDensitySearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardFormatSearch(self, event):
        self.boardFormatSearch = self.boardFormatSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardMaterailSearch(self, event):
        self.boardMaterialSearch = self.boardMaterialSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardRALIDSearch(self, event):
        self.boardRALIDSearch = self.boardRALIDSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportComponentSearch(self,event):
        self.boardSupportComponentSearch = self.boardSupportComponentSearchCtrl.GetValue()
        self.ReSearch()

    def OnBoardSupportWidthSearch(self,event):
        self.boardSupportWidthSearch = self.boardSupportWidthSearchCtrl.GetValue()
        self.ReSearch()

    def ReSearch(self):
        _, boardList = GetAllBoardList(self.log, 1, self.boardType, state=self.state)
        self.dataArray = np.array(boardList)
        if self.boardFormatSearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardFormatSearch in str(board[1]):
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        if self.boardMaterialSearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardMaterialSearch in board[2]:
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        if self.boardDensitySearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardDensitySearch in str(board[3]):
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        if self.boardSupportComponentSearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardSupportComponentSearch in str(board[4]):
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        if self.boardSupportWidthSearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardSupportWidthSearch == str(board[5]):
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        if self.boardRALIDSearch != '':
            boardList = []
            for board in self.dataArray:
                if self.boardRALIDSearch in str(board[6]):
                    boardList.append(board)
            self.dataArray = np.array(boardList)
        self.boardGrid.ReCreate()
        self.boardGrid.Render()

    def OnResetSearchItem(self, event):
        self.boardFormatSearch = ''
        self.boardFormatSearchCtrl.SetValue('')
        self.boardMaterialSearch = ''
        self.boardMaterialSearchCtrl.SetValue('')
        self.boardDensitySearch = ''
        self.boardDensitySearchCtrl.SetValue('')
        self.boardRALIDSearch = ''
        self.boardSupportComponentSearchCtrl.SetValue('')
        self.boardSupportComponentSearch = ''
        self.boardSupportWidthSearchCtrl.SetValue('')
        self.boardSupportWidthSearch = ''
        self.boardRALIDSearchCtrl.SetValue('')
        self.ReSearch()


class BoardManagementPanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
    def ReCreate(self):
        self.Freeze()
        self.DestroyChildren()
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
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
        self.SetSizer(hbox)
        self.pvcManagementPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, 'PVC')
        self.notebook.AddPage(self.pvcManagementPanel, "PVC板管理")
        self.galvanizedSheetManagmentPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, '镀锌板')
        self.notebook.AddPage(self.galvanizedSheetManagmentPanel, "镀锌板管理")
        self.colorCoatManagementPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, '彩涂板')
        self.notebook.AddPage(self.colorCoatManagementPanel, "彩涂板管理")
        self.stainlessSheetManagmentPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, '不锈钢')
        self.notebook.AddPage(self.stainlessSheetManagmentPanel, "不锈钢板管理")
        self.sparyBoardManagementPanel = SpecificBoardManagementPanel(self.notebook, self, self.log, '喷涂板')
        self.notebook.AddPage(self.sparyBoardManagementPanel, "喷涂板管理")

        self.notebook.SetSelection(0)
        self.Layout()
        self.Thaw()
