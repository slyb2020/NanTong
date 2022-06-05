import wx
import os
import wx.lib.scrolledpanel as scrolled
from ID_DEFINE import *
from DBOperation import GetSubOrderPackageState,UpdateSubOrderPackageState,GetSubOrderPanelsForPackage,\
    CreatePackagePanelSheetForOrder,InsertPanelDetailIntoPackageDB,GetSubOrderPanelsForPackageFromPackageDB
import numpy as np
from operator import itemgetter
import wx.lib.agw.pygauge as PG

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps')

class BoxDetailViewPanel(wx.Panel):
    def __init__(self, parent, master,info=[],direction=wx.LEFT,size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.master = master
        self.direction = direction
        self.state=""
        self.seperateSelectionNum=0
        vvbox=wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        self.topDownloadBTN = wx.Button(self, label="▼ 将选定托盘下载到左侧工作区", size=(100, 50))
        self.topDownloadBTN.Bind(wx.EVT_BUTTON, self.OnTopDownloadBTN)
        self.topDownloadBTN.Enable(False)
        self.topUploadBTN = wx.Button(self, label="▲ 将左侧工作区中的托盘上传到完成区", size=(100, 50))
        self.topUploadBTN.Enable(False)
        hhbox.Add(self.topDownloadBTN, 1)
        hhbox.Add(self.topUploadBTN, 1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.frontViewPanel = FrontViewPanel(self,size=(100,100))
        self.topViewPanel = TopViewPanel(self,size=(100,100))
        if direction == wx.LEFT:
            hhbox.Add(self.frontViewPanel,1,wx.EXPAND)
            hhbox.Add(self.topViewPanel,1,wx.EXPAND)
        else:
            hhbox.Add(self.topViewPanel,1,wx.EXPAND)
            hhbox.Add(self.frontViewPanel,1,wx.EXPAND)
        vvbox.Add(hhbox,1,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.bottomDownloadBTN = wx.Button(self, label="▼将所选面板打散至散板区", size=(100, 50))
        self.bottomDownloadBTN.Enable(False)
        self.bottonUploadBTN = wx.Button(self, label="▲将所选面板打包至当前托盘", size=(100, 50))
        self.bottonUploadBTN.Enable(False)
        hhbox.Add(self.bottomDownloadBTN, 1)
        hhbox.Add(self.bottonUploadBTN, 1)
        vvbox.Add(hhbox,0,wx.EXPAND)
        self.SetSizer(vvbox)

    def SetValue(self,info):
        self.name = info[0]
        self.length = info[1]
        self.width = info[2]
        self.height = info[3]
        self.layer = info[4]
        self.weight = info[5]
        self.amount = info[6]
        self.square = info[7]
        self.suborder = info[8]
        self.deck = info[9]
        self.zone = info[10]
        self.room= info[11]
        self.mode = info[12]
        self.boxState = info[13]
        self.data = info[14]
        self.frontViewPanel.SetValue(info)
        self.topViewPanel.SetValue((0,0),[])

    def OnTopDownloadBTN(self, event):
        error=True
        for i, box in enumerate(self.master.boxList):
            if box.state=='选定':
                error=False
                if self.direction == wx.LEFT:
                    box.SetBackgroundColour(wx.Colour(234,124,233))
                else:
                    box.SetBackgroundColour(wx.Colour(234,233,124))
                self.state="占用"
                self.master.boxList[i].state="左"
                box.Refresh()
                self.topDownloadBTN.Enable(False)
                self.topUploadBTN.Enable(True)
        if error:
            wx.MessageBox("您还没有选择要移入左侧工作区的托盘！")
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()


class TopViewPanel(wx.Panel):
    def __init__(self,parent,data=[],size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.data=data
        self.size=(0,0)
        # self.data = [
        #                 [(800,200),(500,200),(400,200)],
        #                 [(1000,200),(500,200),(500,200)],
        #                 [(1800,200),(1000,200)]
        #             ]
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.nameTXT = wx.TextCtrl(self,size=(10,40))
        vbox.Add(self.nameTXT,0,wx.EXPAND)
        topPanel = wx.Panel(self,size=(10,20))
        self.lengthTXT = wx.StaticText(topPanel,label="2280mm",pos=(200,3))
        vbox.Add(topPanel,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        self.panel = wx.Panel(self,style=wx.BORDER_SUNKEN)
        self.panel.SetBackgroundColour(wx.WHITE)
        rightPanel=wx.Panel(self,size=(20,-1))
        self.widthTXT = wx.StaticText(rightPanel,label="600mm",pos=(0,100))
        hhbox.Add(self.panel,1,wx.EXPAND)
        hhbox.Add(rightPanel,0,wx.EXPAND)
        vbox.Add(hhbox,1,wx.EXPAND)
        self.SetSizer(vbox)
        self.ReCreate()

    def ReCreate(self):
        self.panel.DestroyChildren()
        (lengthPixel,widthPixel) = self.panel.GetClientSize()
        lengthCoef = float(self.size[0]/lengthPixel)
        widthCoef = float(self.size[1]/widthPixel)
        if self.size[0]==0 and self.size[1]==0:
            self.lengthTXT.SetLabel("")
            self.widthTXT.SetLabel("")
        else:
            self.lengthTXT.SetLabel(str(self.size[0]))
            self.widthTXT.SetLabel(str(self.size[1]))
        vbox = wx.BoxSizer(wx.VERTICAL)
        totalRow = len(self.data)
        self.buttonList=[]
        if totalRow>0:
            for row in range(totalRow):
                hbox = wx.BoxSizer()
                for col in range(len(self.data[row])):
                    button = wx.Button(self.panel,label="%sX%sx%s"%(self.data[row][col][9],self.data[row][col][10],self.data[row][col][11]),size=(int(float(self.data[row][col][9])/lengthCoef),int(float(self.data[row][col][10])/widthCoef)),name="%s,%s"%(row,col))
                    button.SetBackgroundColour(wx.Colour(210,210,210))
                    button.SetToolTip("面板编号: %d  订单号: %s-%s  甲板: %s  区域: %s  房间: %s\r\n图纸：%s  面板长：%s   "
                                      "面板宽：%s    面板厚：%s\r\nX面颜色：%s      Y面颜色：%s    胶水单号：%s"%(self.data[row][col][0],
                self.data[row][col][1],self.data[row][col][2],self.data[row][col][3],self.data[row][col][4],self.data[row][col][5],self.data[row][col][6],
                self.data[row][col][9],self.data[row][col][10],self.data[row][col][11],self.data[row][col][12],self.data[row][col][13],self.data[row][col][16]))
                    hbox.Add(button,0)
                    self.buttonList.append(button)
                # vbox.Add(hbox,int(self.data[row][0][10]),wx.EXPAND)
                vbox.Add(hbox,0)
        self.panel.SetSizer(vbox)
        self.panel.Refresh()
        self.panel.Layout()
        self.Bind(wx.EVT_BUTTON,self.OnButton)

    def OnButton(self,event):
        obj = event.GetEventObject()
        name = obj.GetName()
        name = name.split(',')
        data = self.data[int(name[0])][int(name[1])]
        for button in self.buttonList:
            button.SetBackgroundColour(wx.Colour(210,210,210))
        obj.SetBackgroundColour(wx.Colour(150,150,150))
        self.parent.bottomDownloadBTN.Enable(True)

    def SetValue(self,size,data):
        self.size=size
        self.data=data
        self.ReCreate()
        self.Refresh()

class FrontViewPanel(wx.Panel):
    def __init__(self,parent,data=[],size=wx.DefaultSize):
        wx.Panel.__init__(self, parent, size=size)
        self.parent = parent
        self.state=""
        self.data = data
        self.selectionNum=None
        # self.data = [
        #                 [
        #                     25,[
        #                             [(800,200),(500,200)],
        #                             [(800,200),(500,200)],
        #                        ]
        #                 ],
        #                 [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
        #                 [50,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
        #                 [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
        #                 [25,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
        #                 [50,[[(800,200),(500,200)]],[[(800,200),(500,200)]]],
        #             ]
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        bmp = wx.Bitmap(bitmapDir + '/lbnews.png')
        btn = wx.Button(self, -1, size=(40, 40), name="增加一个新的层")
        btn.SetBackgroundColour(wx.Colour(240,240,240))
        btn.SetToolTip("增加一个新的层")
        btn.SetBitmap(bmp)
        hhbox.Add(btn,0)
        bmp = wx.Bitmap(bitmapDir + '/new_folder.png')
        btn = wx.Button(self, -1, size=(40, 40), name="删除空的层")
        btn.SetBackgroundColour(wx.Colour(240,240,240))
        btn.SetToolTip("删除空的层")
        btn.SetBitmap(bmp)
        hhbox.Add(btn,0)
        bmp = wx.Bitmap(bitmapDir + '/lbdecrypted.png')
        btn = wx.Button(self, -1, size=(40, 40), name="整层打撒")
        btn.SetBackgroundColour(wx.Colour(240,240,240))
        btn.SetToolTip("整层打撒")
        btn.SetBitmap(bmp)
        hhbox.Add(btn,0)

        self.nameTXT = wx.TextCtrl(self,size=(10,40))
        self.nameTXT.SetBackgroundColour(wx.Colour(240,240,240))
        hhbox.Add(self.nameTXT,1)
        vbox.Add(hhbox,0,wx.EXPAND)
        self.panel = scrolled.ScrolledPanel(self)
        vbox.Add(self.panel,1,wx.EXPAND)
        self.SetSizer(vbox)
        self.panel.SetAutoLayout(1)
        self.panel.SetupScrolling()
        self.Bind(wx.EVT_BUTTON,self.OnButton)


    def OnButton(self,event):
        obj = event.GetEventObject()
        name = obj.GetName()
        if str(name).isdigit():
            self.selectionNum = int(name)
            for button in self.occupyButtonList:
                button.SetBackgroundColour(wx.Colour(111, 123, 245))
            for button in self.freeButtonList:
                button.SetBackgroundColour(wx.Colour(240,240,240))
            self.occupyButtonList[self.selectionNum].SetBackgroundColour(wx.RED)
            self.freeButtonList[self.selectionNum].SetBackgroundColour(wx.RED)
            boxSize=(self.length,self.width)
            self.parent.topViewPanel.SetValue(boxSize,self.data[self.selectionNum])


    def ReCreate(self):
        self.panel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        totalLayer = len(self.data)
        self.occupyButtonList=[]
        self.freeButtonList=[]
        (L,W)=self.panel.GetClientSize()
        L=L-20#流出右侧滚动条的宽度
        if totalLayer>0:
            for i in range(totalLayer):
                hhbox = wx.BoxSizer()
                square=0
                for row in self.data[i]:
                    for col in row:
                        square += (int(col[9])*int(col[10]))
                percent = float(square/self.boxSquare)
                occupyButton = wx.Button(self.panel,label="第%d层"%(i),size=(L*percent,-1),name="%s"%(i))
                occupyButton.SetForegroundColour(wx.Colour(wx.WHITE))
                occupyButton.SetBackgroundColour(wx.Colour(111, 123, 245))
                freeButton = wx.Button(self.panel,size=(L*(1-percent),-1),name="%s"%(i))
                freeButton.SetBackgroundColour(wx.Colour(240,240,240))
                # int(self.data[i][9])*int(self.data[i][10])
                hhbox.Add(occupyButton,0,wx.EXPAND)
                hhbox.Add(freeButton,0,wx.EXPAND)
                vbox.Add(hhbox,1,wx.EXPAND)
                self.occupyButtonList.append(occupyButton)
                self.freeButtonList.append(freeButton)
        self.panel.SetSizer(vbox)
        self.panel.Refresh()
        self.panel.SetAutoLayout(1)
        self.panel.SetupScrolling()

    def SetValue(self,info):
        print("info=",info)
        self.selectionNum = None
        self.name = info[0]
        self.length = info[1]
        self.width = info[2]
        self.height = info[3]
        self.layer = info[4]
        self.weight = info[5]
        self.amount = info[6]
        self.square = info[7]
        self.suborder = info[8]
        self.deck = info[9]
        self.zone = info[10]
        self.room= info[11]
        self.mode = info[12]
        self.boxState = info[13]
        self.data = info[14]
        self.boxSquare = float(self.length)*float(self.width)
        self.ReCreate()


class MyGauge(PG.PyGauge):
    def __init__(self,parent,master,name=""):
        PG.PyGauge.__init__(self, parent,  size=(1, 1), style = wx.GA_HORIZONTAL)
        self.master = master
        self.name = name
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)

    def GetName(self):
        return self.name

    def OnLeftClick(self, event):
        obj = event.GetEventObject()
        name = obj.GetName()
        for i, box in enumerate(self.master.boxList):
            if box.GetName() == name:
                if box.state == "":
                    if self.master.leftWorkingPackagePanel.state != "占用" or self.master.rightWorkingPackagePanel.state != "占用":
                        self.master.selectionBoxIDTXT.SetValue(str(self.master.packageList[i].info[0]))
                        self.master.selectionPanelTotalAmountTXT.SetValue(str(self.master.packageList[i].info[6]))
                        self.master.selectionPanelTotalWeightTXT.SetValue(str(self.master.packageList[i].info[5]))
                        self.master.boxLayerNumTXT.SetValue(str(self.master.packageList[i].info[4]))
                        self.master.boxLengthTXT.SetValue(str(self.master.packageList[i].info[1]))
                        self.master.boxWidthTXT.SetValue(str(self.master.packageList[i].info[2]))
                        self.master.boxHeightTXT.SetValue(str(self.master.packageList[i].info[3]))
                        box.SetBackgroundColour(wx.Colour(124, 234, 233))
                        self.master.boxList[i].state = '选定'
                        if self.master.leftWorkingPackagePanel.state != "占用":
                            self.master.leftWorkingPackagePanel.topDownloadBTN.Enable(True)
                            self.master.leftWorkingPackagePanel.SetValue(self.master.packageList[i].info)
                        else:
                            self.master.rightWorkingPackagePanel.SetValue(self.master.packageList[i].info)
                        if self.master.rightWorkingPackagePanel.state != "占用":
                            self.master.rightWorkingPackagePanel.topDownloadBTN.Enable(True)
            elif box.state == "选定":
                self.master.boxList[i].state = ""
                box.SetBackgroundColour(wx.Colour(240, 240, 240))
            box.Refresh()
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()


class PackagePanel(wx.Panel):
    def __init__(self,parent,master,info=[]):
        self.info = info
        self.master = master
        self.name = info[0]
        self.length = info[1]
        self.width = info[2]
        self.height = info[3]
        self.layer = info[4]
        self.weight = info[5]
        self.amount = info[6]
        self.square = info[7]
        self.suborder = info[8]
        self.deck = info[9]
        self.zone = info[10]
        self.room= info[11]
        self.mode = info[12]
        self.state = info[13]
        # self.data = info[14]
        self.size = (120,self.layer*10)
        wx.Panel.__init__(self, parent, size=self.size)
        # self.data = data
        self.data = [
                        [
                            [[522, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2280', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', '']],
                            [[523, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2280', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', '']],
                        ],
                        [
                            [[524, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2280', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', '']],
                            [[525, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[526, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[527, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[528, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[529, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[530, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[531, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[532, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[532, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[534, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[535, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                        ],
                        [
                            [[536, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IAA', '2195', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0085', '', '3.95', '64731-0085', '', '']],
                            [[537, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                        ],
                        [
                            [[538, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                            [[539, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                        ],
                        [
                            [[540, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                            [[541, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                        ],
                        [
                            [[542, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30IOA', '2125', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0086', '', '3.82', '64731-0086', '', '']],
                            [[1073, 64731, '1', '3', '9', 'Corridor', 'C.C72.0006', 'C72', 'J30KTA', '1885', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0103', '', '3.39', '64731-0103', '', '']],
                        ],
                    ]
        self.info[14]= self.data
        self.layer=len(self.data)
        self.panel = wx.Panel(self)
        hbox = wx.BoxSizer()
        hbox.Add(self.panel,1,wx.EXPAND|wx.ALL,10)
        self.SetSizer(hbox)
        self.ReCreate()

    def ReCreate(self):
        self.panel.DestroyChildren()
        self.SetBackgroundColour(wx.Colour(240,240,240))
        self.state = ""
        self.layerGaugeList=[]
        vvbox = wx.BoxSizer(wx.VERTICAL)
        boxSquare = float(self.length) * float(self.width)

        for i, layer in enumerate(self.data[::-1]):
            square = 0
            gauge = MyGauge(self.panel,self.master,self.name)
            for j, row in enumerate(layer):
                for k, col in enumerate(row):
                    length= float(col[9])
                    width = float(col[10])
                    square+=(length*width)
            percent = 100.0*square/boxSquare
            gauge.SetValue(percent)
            gauge.SetBackgroundColour(wx.WHITE)
            gauge.SetBorderColor(wx.BLACK)
            self.layerGaugeList.append(gauge)
            temp = int(layer[0][0][11])/25
            vvbox.Add(gauge,int(temp),wx.EXPAND)
        self.panel.SetSizer(vvbox)
        self.panel.Refresh()

    def GetName(self):
        return self.name


class PackageDialog(wx.Dialog):
    def __init__(self, parent, log, data, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self)
        self.orderID = data[0]
        self.suborderID = data[8]
        self.log = log
        self.parent = parent
        self.panelTotalAmount=0
        self.panelTotalWeight=0
        self.panelTotalSquare=0
        self.boxTotalAmount=0
        self.boxList = []
        self.separatePanelList=[
            [522, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2280', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [523, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2100', '400', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [525, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1980', '350', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [526, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1980', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [527, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1500', '550', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [528, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1500', '600', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [529, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '2280', '400', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [530, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1480', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [531, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1300', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [532, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1280', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [533, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1180', '400', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [534, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '1080', '300', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [535, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '780', '500', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [536, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '680', '700', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [537, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '680', '600', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [538, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '680', '370', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [539, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '680', '450', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
            [540, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D30HDA', '680', '550', '50', 'RAL9010', 'G', 'None', 'None', '64731-0084', '', '4.10', '64731-0084', '', ''],
        ]
        dbName = "p%s"%self.orderID
        from DBOperation import GetTableListFromDB
        _,dbNameList = GetTableListFromDB(self.log,WHICHDB)
        if dbName not in dbNameList:
            CreatePackagePanelSheetForOrder(log,WHICHDB,dbName)
            _, self.panelList = GetSubOrderPanelsForPackage(self.log, WHICHDB, self.orderID)#读取订单中所有子订单数据
            self.data=[]
            for record in self.panelList:
                # print("recor",record)
                # [93, 64731, '1', '3', '9', 'Corridor', 'C.C72.0001', 'C72', 'D40RLA', 1, '1240', '400', '50', 'RAL9010','G', 'None', 'None', '64731-0093', '2.98', '']
                for i in range(int(record[9])):
                    #       `订单号`, `子订单号`, `甲板`,   `区域`,    `房间`,       `图纸`,   `产品类型`,`面板代码`,    `宽度`, `高度`, `厚度`, `X面颜色`, `Y面颜色`, `Z面颜色`, `V面颜色`, `数量`, `面板代码`
                #          [1, 64731, '1'      , '3',      '9',  'Corridor', 'A.2SA.0900', '2SA',  'A5KBWBG',2, '2160'  ,  '550',      '50',     'YC74H',   'YQ73D',   'None',    'None', '64731-0001', '7.13', '']                for i in range(int(record[9])):
                    temp=[record[1],record[2],record[3],record[4],record[5]    ,record[6],record[7],record[8],record[10],record[11],record[12],record[13],record[14],record[15],record[16],record[17],'',record[18],record[17],'',record[19],'']
                    self.data.append(temp)
            InsertPanelDetailIntoPackageDB(self.log,WHICHDB,dbName,self.data)
        _, self.packageState = GetSubOrderPackageState(self.log,WHICHDB,dbName,self.suborderID)
        if self.packageState not in ["按房间打包","按区域打包"]:
            self.packageState = "未打包"
        _, self.panelList = GetSubOrderPanelsForPackageFromPackageDB(self.log,WHICHDB,self.orderID,self.suborderID)
        self.panelTotalAmount = len(self.panelList)
        self.panelList.sort(key=itemgetter(11,10,9), reverse=True)#先将墙板按厚度，宽度，长度排序
        #角墙板怎么打包？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
        for record in self.panelList:
            # [1, 64731, '1', '3', '9', 'Corridor', 'A.2SA.0900', '2SA', 'A5KBWBG', '2160', '550', '50', 'YC74H', 'YQ73D',
            #  'None', 'None', '64731-0001', '', '7.13', '64731-0001', '', '']
            self.panelTotalWeight+=float(record[18])
            self.panelTotalSquare+= (float(record[9])*float(record[10]))
        self.panelTotalSquare = self.panelTotalSquare/1.E6
        self.SetExtraStyle(wx.DIALOG_EX_METAL)
        self.Create(parent, -1, "产品打包操作对话框", pos, size, style)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = wx.Panel(self, -1, size=(1800, 900))
        self.topPanel = wx.Panel(self.panel,size=(100,100))
        self.ReCreateTopPanel()
        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.topPanel,0,wx.EXPAND)
        vbox.Add(wx.StaticLine(self.panel,size=(10,2),style=wx.HORIZONTAL),0,wx.EXPAND)

        hhbox=wx.BoxSizer()
        panel = wx.Panel(self.panel,size=(40,-1))
        hhbox.Add(panel,0,wx.EXPAND)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        bmp = wx.Bitmap(bitmapDir + '/lbnews.png')
        btn = wx.Button(panel, -1, size=(40, 40), name="新建托盘")
        btn.SetBackgroundColour(wx.Colour(240,240,240))
        btn.SetToolTip("新建托盘")
        btn.SetBitmap(bmp)
        vvbox.Add(btn,0)

        bmp = wx.Bitmap(bitmapDir + '/view2.png')
        btn = wx.Button(panel, -1, size=(40, 40), name="打散托盘")
        btn.SetBackgroundColour(wx.Colour(240,240,240))
        btn.SetToolTip("打散托盘")
        btn.SetBitmap(bmp)
        vvbox.Add(btn,0)
        panel.SetSizer(vvbox)
        self.finishPackagePanel = scrolled.ScrolledPanel(self.panel,size=(100,200))
        hhbox.Add(self.finishPackagePanel,1,wx.EXPAND)
        vbox.Add(hhbox,1,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        self.leftWorkingPackagePanel = BoxDetailViewPanel(self.panel,self,direction=wx.LEFT,size=(100,400))
        hhbox.Add(self.leftWorkingPackagePanel,1,wx.EXPAND)
        self.middleControlPanel = wx.Panel(self.panel,size=(50,-1))
        self.middleControlPanel.SetBackgroundColour(wx.Colour(220,220,220))
        hhbox.Add(self.middleControlPanel,0,wx.EXPAND)
        self.rightWorkingPackagePanel = BoxDetailViewPanel(self.panel,self,direction=wx.RIGHT,size=(100,400))
        hhbox.Add(self.rightWorkingPackagePanel,1,wx.EXPAND)
        hhbox.Add((10,-1))
        vbox.Add(hhbox,0,wx.EXPAND)
        # self.bottomPackagePanel = scrolled.ScrolledPanel(self.panel,size=(100,150))
        self.bottomPackagePanel = wx.Panel(self.panel,size=(100,150))
        vbox.Add(self.bottomPackagePanel,0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM,10)

        self.middleLeftAddBTN = wx.Button(self.middleControlPanel,label="<<+",size=(10,50))
        self.middleRightAddBTN = wx.Button(self.middleControlPanel,label="+>>",size=(10,50))
        self.middleLeftBTN = wx.Button(self.middleControlPanel,label=">>",size=(10,20))
        self.middleRightBTN = wx.Button(self.middleControlPanel,label="<<",size=(10,20))
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add(self.middleLeftAddBTN,0,wx.EXPAND)
        vvbox.Add(self.middleRightBTN,1,wx.EXPAND)
        vvbox.Add(self.middleLeftBTN,1,wx.EXPAND)
        vvbox.Add(self.middleRightAddBTN,0,wx.EXPAND)
        self.middleControlPanel.SetSizer(vvbox)


        hbox=wx.BoxSizer()
        self.packageList=[]
        for i in range(20):
            temp = ["托盘%s"%i,2280,600,600,11,'345','100','2000','1','3','9','Corridor','房间','','']
            package = PackagePanel(self.finishPackagePanel,self,info=temp)
            self.packageList.append(package)
            self.boxList.append(package)
            hbox.Add(package)
        self.finishPackagePanel.SetSizer(hbox)
        self.finishPackagePanel.SetAutoLayout(1)
        self.finishPackagePanel.SetupScrolling()

        hbox=wx.BoxSizer()
        vvbox = wx.BoxSizer(wx.VERTICAL)
        bmp = wx.Bitmap(bitmapDir + '/e6.png')
        self.SeperateRePackageBTN = wx.Button(self.bottomPackagePanel,size=(50,50))
        self.SeperateRePackageBTN.SetToolTip("将所有散板自动打包")
        self.SeperateRePackageBTN.SetBitmap(bmp)
        vvbox.Add(self.SeperateRePackageBTN,0)
        bmp = wx.Bitmap(bitmapDir + '/e4.png')
        btn = wx.Button(self.bottomPackagePanel, -1, size=(50, 50), name="上移一层")
        btn.SetToolTip("散板重新排序")
        btn.SetBitmap(bmp)
        vvbox.Add(btn,0)
        bmp = wx.Bitmap(bitmapDir + '/e5.png')
        btn = wx.Button(self.bottomPackagePanel, -1, size=(50, 50), name="下移一层")
        btn.SetToolTip("参数设置")
        btn.SetBitmap(bmp)
        vvbox.Add(btn,0)
        hbox.Add(vvbox,0)
        hbox.Add((5,-1))
        # bmp = wx.Bitmap(bitmapDir + '/icon4.jpg')
        # btn = wx.Button(self, -1, size=(40, 40), name="上移一层")
        # btn.SetBackgroundColour(wx.Colour(240,240,240))
        # btn.SetToolTip("上移一层")
        # btn.SetBitmap(bmp)
        # hhbox.Add(btn,0)
        # bmp = wx.Bitmap(bitmapDir + '/icon5.jpg')
        # btn = wx.Button(self, -1, size=(40, 40), name="下移一层")
        # btn.SetBackgroundColour(wx.Colour(240,240,240))
        # btn.SetToolTip("下移一层")
        # btn.SetBitmap(bmp)
        # hhbox.Add(btn,0)
        self.seperatePackagePanel = scrolled.ScrolledPanel(self.bottomPackagePanel)
        hbox.Add(self.seperatePackagePanel,1,wx.EXPAND)
        self.bottomPackagePanel.SetSizer(hbox)
        self.SeperatePackagePanelReCreate()

        # self.panel.SetBackgroundColour(wx.Colour(234,219,212))
        self.panel.SetSizer(vbox)
        sizer.Add(self.panel, 0, wx.EXPAND)
        line = wx.StaticLine(self, -1, size=(30, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.RIGHT | wx.TOP, 5)

        btnsizer = wx.BoxSizer()
        bitmap1 = wx.Bitmap("bitmaps/ok3.png", wx.BITMAP_TYPE_PNG)
        bitmap2 = wx.Bitmap("bitmaps/cancel1.png", wx.BITMAP_TYPE_PNG)
        bitmap3 = wx.Bitmap("bitmaps/33.png", wx.BITMAP_TYPE_PNG)
        btn_repack = wx.Button(self, label="全部重新打包", size=(200, 50))
        btn_repack.SetBitmap(bitmap1, wx.LEFT)
        btn_save = wx.Button(self, label="保存 (Save)", size=(200, 50))
        btn_save.SetBitmap(bitmap2, wx.LEFT)
        btn_ok = wx.Button(self, wx.ID_OK, "确  定", size=(200, 50))
        btn_ok.SetBitmap(bitmap1, wx.LEFT)
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "取  消", size=(200, 50))
        btn_cancel.SetBitmap(bitmap2, wx.LEFT)
        btnsizer.Add(btn_repack, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_save, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_ok, 0)
        btnsizer.Add((40, -1), 0)
        btnsizer.Add(btn_cancel, 0)
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.Bind(wx.EVT_BUTTON,self.OnButton)
        # btn_ok.Bind(wx.EVT_BUTTON, self.OnOk)
        # btn_cancel.Bind(wx.EVT_BUTTON, self.OnCancel)
        # manualInputBTN.Bind(wx.EVT_BUTTON, self.OnCancel)

    # def OnOk(self, event):
    #     event.Skip()
    #
    # def OnCancel(self, event):
    #     # self.log.WriteText("操作员：'%s' 取消库存参数设置操作\r\n"%(self.parent.operator_name))
    #     event.Skip()
    def OnButton(self,event):
        obj = event.GetEventObject()
        name = obj.GetName()
        for i,button in enumerate(self.separatePanelCtrlList):
            if button.GetName()==name:
                self.seperateSelectionNum = i
                button.SetBackgroundColour(wx.Colour(240,150,150))
            else:
                button.SetBackgroundColour(wx.Colour(240,240,240))


    def SeperatePackagePanelReCreate(self):
        self.seperatePackagePanel.DestroyChildren()
        hbox=wx.BoxSizer()
        self.separatePanelCtrlList=[]
        for i,board in enumerate(self.separatePanelList):
            button=wx.Button(self.seperatePackagePanel,label="%sX%sX%s"%(board[9],board[10],board[11]),size=(int(board[9])/12,int(board[10])/7),name=str(board[0]))
            button.SetToolTip("面板编号: %d  订单号: %s-%s  甲板: %s  区域: %s  房间: %s\r\n图纸：%s  面板长：%s   "
                              "面板宽：%s    面板厚：%s\r\nX面颜色：%s      Y面颜色：%s    胶水单号：%s" %
                              (board[0],board[1],board[2],board[3],board[4],board[5],board[6],board[9],board[10],board[11],board[12],board[13],board[16]))
            hbox.Add(button,0,wx.ALL,2)
            self.separatePanelCtrlList.append(button)
        self.seperatePackagePanel.SetSizer(hbox)
        self.seperatePackagePanel.SetAutoLayout(1)
        self.seperatePackagePanel.SetupScrolling()

    def ReCreateTopPanel(self):
        self.topPanel.DestroyChildren()
        hbox = wx.BoxSizer()
        hbox.Add(10, -1)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        vvbox.Add((-1,20))
        hhbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='订单号：',size=(67,-1)), 0, wx.TOP, 5)
        self.orderIDTXT = wx.TextCtrl(self.topPanel, size=(70, 25), style=wx.TE_READONLY)
        self.orderIDTXT.SetValue('%05d-%03d' % (int(self.orderID),int(self.suborderID)))
        # self.orderIDTXT.SetBackgroundColour(wx.GREEN)
        hhbox.Add(self.orderIDTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='订单名称：',size=(64,-1)), 0, wx.TOP, 5)
        self.orderNameTXT = wx.TextCtrl(self.topPanel, size=(90, 25), style=wx.TE_READONLY)
        self.orderNameTXT.SetValue("需处理")
        self.orderNameTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.orderNameTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='打包状态'), 0, wx.TOP, 5)
        self.packageStateTXT = wx.TextCtrl(self.topPanel, size=(80, 25), style=wx.TE_READONLY)
        self.packageStateTXT.SetValue(self.packageState)
        if self.packageState=='未打包':
            self.packageStateTXT.SetBackgroundColour(wx.RED)
        else:
            self.packageStateTXT.SetBackgroundColour(wx.GREEN)
        hhbox.Add(self.packageStateTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add(hhbox,0,wx.EXPAND)
        hhbox = wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='面板总数'), 0, wx.TOP, 5)
        self.panelTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(45, 25), style=wx.TE_READONLY)
        self.panelTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='总重量'), 0, wx.TOP, 5)
        self.panelTotalWeightTXT = wx.TextCtrl(self.topPanel, size=(60, 25), style=wx.TE_READONLY)
        self.panelTotalWeightTXT.SetValue("%.2f" % self.panelTotalWeight)
        self.panelTotalWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotalWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='面板总面积'), 0, wx.TOP, 5)
        self.panelTotalSquareTXT = wx.TextCtrl(self.topPanel, size=(60, 25), style=wx.TE_READONLY)
        self.panelTotalSquareTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.panelTotalSquareTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add(wx.StaticText(self.topPanel, label='托盘总数'), 0, wx.TOP, 5)
        self.boxTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(40, 25), style=wx.TE_READONLY)
        self.boxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)
        self.panelTotalAmountTXT.SetValue(str(self.panelTotalAmount))
        self.panelTotalSquareTXT.SetValue("%.2f"%self.panelTotalSquare)
        self.boxTotalAmountTXT.SetValue(str(self.boxTotalAmount))

        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0)

        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        hbox.Add((10,-1))

        vvbox =wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='当前甲板'), 0, wx.TOP, 5)
        temp=np.array(self.panelList)[:,3]
        choiceList = list(set(temp))
        if len(choiceList)>1:
            choiceList.insert(0,"全部")
        self.deckCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.deckCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.deckCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前区域'), 0, wx.TOP, 5)
        deck = self.deckCOMBO.GetValue()
        if deck == "全部":
            temp = np.array(self.panelList)[:, 4]
        else:
            temp = []
            for record in self.panelList:
                if str(record[3])==deck:
                    temp.append(str(record[4]))
        choiceList = list(set(temp))
        if len(choiceList)>1:
            choiceList.insert(0,"全部")
        self.zoneCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(40, 25),choices=choiceList, style=wx.TE_READONLY)
        self.zoneCOMBO.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.zoneCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        if self.packageState!="按区域打包": #当按区域打包时，不应该显示房间Combobox
            hhbox.Add((10,-1))
            hhbox.Add(wx.StaticText(self.topPanel, label='当前房间'), 0, wx.TOP, 5)
            deck = self.deckCOMBO.GetValue()
            zone = self.zoneCOMBO.GetValue()
            temp=[]
            if deck == "全部":
                if zone == "全部":
                    temp = np.array(self.panelList)[:, 5]
                else:
                    for record in self.panelList:
                        if str(record[4])==zone:
                            temp.append(str(record[5]))
            else:
                if zone == "全部":
                    for record in self.panelList:
                        if str(record[3])==deck:
                            temp.append(str(record[5]))
                else:
                    for record in self.panelList:
                        if str(record[4])==zone and str(record[3])==deck:
                            temp.append(str(record[5]))
            choiceList = list(set(temp))
            if len(choiceList)>1:
                choiceList.insert(0,"全部")
            self.roomCOMBO = wx.ComboBox(self.topPanel, value=choiceList[0], size=(80, 25),choices=choiceList, style=wx.TE_READONLY)
            self.roomCOMBO.SetBackgroundColour(wx.WHITE)
            hhbox.Add(self.roomCOMBO, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘数'), 0, wx.TOP, 5)
        self.currentBoxTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(32, 25), style=wx.TE_READONLY)
        self.currentBoxTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentBoxTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,20))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板数'), 0, wx.TOP, 5)
        self.currentPanelTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotalAmountTXT.SetValue(str(self.panelTotalAmount))
        self.currentPanelTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板重量'), 0, wx.TOP, 5)
        self.currentPanelTotalWeightTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotalWeightTXT.SetValue("%.2f"%self.panelTotalWeight)
        self.currentPanelTotalWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotalWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='当前面板面积'), 0, wx.TOP, 5)
        self.currentPanelTotalSquareTXT = wx.TextCtrl(self.topPanel, size=(67, 25), style=wx.TE_READONLY)
        self.currentPanelTotalSquareTXT.SetValue("")
        self.currentPanelTotalSquareTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.currentPanelTotalSquareTXT, 0, wx.LEFT | wx.RIGHT, 10)
        self.CalculateAndShowCurrentValue()
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0,wx.EXPAND)

        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT|wx.RIGHT,10)

        vvbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add(wx.StaticText(self.topPanel, label='选中托盘名'), 0, wx.TOP, 5)
        self.selectionBoxIDTXT = wx.TextCtrl(self.topPanel, size=(57, 25), style=wx.TE_READONLY)
        self.selectionBoxIDTXT.SetValue("")
        self.selectionBoxIDTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionBoxIDTXT, 0, wx.LEFT | wx.RIGHT, 10)
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘内面板总数'), 0, wx.TOP, 5)
        self.selectionPanelTotalAmountTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.selectionPanelTotalAmountTXT.SetValue("")
        self.selectionPanelTotalAmountTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotalAmountTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘内面板总重量'), 0, wx.TOP, 5)
        self.selectionPanelTotalWeightTXT = wx.TextCtrl(self.topPanel, size=(60, 25), style=wx.TE_READONLY)
        self.selectionPanelTotalWeightTXT.SetValue("")
        self.selectionPanelTotalWeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.selectionPanelTotalWeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,20))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hhbox=wx.BoxSizer()
        hbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘层数'), 0, wx.TOP, 5)
        self.boxLayerNumTXT = wx.TextCtrl(self.topPanel, size=(40, 25), style=wx.TE_READONLY)
        self.boxLayerNumTXT.SetValue(str(10))
        self.boxLayerNumTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxLayerNumTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘长'), 0, wx.TOP, 5)
        self.boxLengthTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxLengthTXT.SetValue(str(2345))
        self.boxLengthTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxLengthTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘宽'), 0, wx.TOP, 5)
        self.boxWidthTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxWidthTXT.SetValue(str(550))
        self.boxWidthTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxWidthTXT, 0, wx.LEFT | wx.RIGHT, 10)

        hhbox.Add((20,-1))
        hhbox.Add(wx.StaticText(self.topPanel, label='托盘高'), 0, wx.TOP, 5)
        self.boxHeightTXT = wx.TextCtrl(self.topPanel, size=(50, 25), style=wx.TE_READONLY)
        self.boxHeightTXT.SetValue(str(1500))
        self.boxHeightTXT.SetBackgroundColour(wx.WHITE)
        hhbox.Add(self.boxHeightTXT, 0, wx.LEFT | wx.RIGHT, 10)

        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)

        hbox.Add(vvbox,0)
        hbox.Add(wx.StaticLine(self.topPanel,style=wx.VERTICAL),0,wx.EXPAND|wx.LEFT,10)

        bitmap = wx.Bitmap("bitmaps/box.jpg", wx.BITMAP_TYPE_JPEG)
        # startAutoPackageBTN.SetFont()
        startAutoPackageBTN = wx.Button(self.topPanel,label="运行自动打包")
        # startAutoPackageBTN.SetAuthNeeded()
        startAutoPackageBTN.SetBitmap(bitmap, wx.RIGHT)
        # startAutoPackageBTN.SetBitmapMargins(10,10)

        hbox.Add(startAutoPackageBTN,1,wx.EXPAND|wx.ALL,10)
        self.topPanel.SetSizer(hbox)

    def CalculateAndShowCurrentValue(self):
        self.currentPanelTotalAmount = 0
        self.currentPanelTotalWeight = 0
        self.currentPanelTotalSquare = 0
        for record in self.panelList:
            if record[3]==self.deckCOMBO.GetValue() and record[4]==self.zoneCOMBO.GetValue() and record[5]==self.roomCOMBO.GetValue():
                self.currentPanelTotalAmount += 1
                self.currentPanelTotalWeight += float(record[18])
                self.currentPanelTotalSquare += float(record[9])*float(record[10])
        self.currentPanelTotalAmountTXT.SetValue(str(self.currentPanelTotalAmount))
        self.currentPanelTotalWeightTXT.SetValue("%.2f"%self.currentPanelTotalWeight)
        self.currentPanelTotalSquareTXT.SetValue("%.2f"%(self.currentPanelTotalSquare/1.0E6))
        self.currentBoxTotalAmountTXT.SetValue('0')

    def CalculateSubOrderPackage(self):
        _,self.panelList=GetSubOrderPanelsForPackage(self.log,WHICHDB,self.orderID,self.suborderID)
        for panel in self.panelList:
            print("panel=",panel)

    # def OnLeftTopDownloadBTN(self, event):
    #     error=True
    #     for i, box in enumerate(self.boxList):
    #         if box.state=='选定':
    #             error=False
    #             box.SetBackgroundColour(wx.Colour(234,124,233))
    #             self.leftFrontViewPanel.state="占用"
    #             self.boxList[i].state="左"
    #             box.Refresh()
    #             self.leftTopDownloadBTN.Enable(False)
    #             self.leftTopUploadBTN.Enable(True)
    #     if error:
    #         wx.MessageBox("您还没有选择要移入左侧工作区的托盘！")
    #     # self.frame.SetBackgroundColour(wx.GREEN)
    #     # self.frame.Refresh()
    #     event.Skip()
    def OnRightTopDownloadBTN(self, event):
        error=True
        for i, box in enumerate(self.boxList):
            if box.state=='选定':
                error=False
                box.SetBackgroundColour(wx.Colour(189,174,233))
                self.rightFrontViewPanel.state="占用"
                self.boxList[i].state="右"
                box.Refresh()
                self.rightTopDownloadBTN.Enable(False)
                self.rightTopUploadBTN.Enable(True)
        if error:
            wx.MessageBox("您还没有选择要移入左侧工作区的托盘！")
        # self.frame.SetBackgroundColour(wx.GREEN)
        # self.frame.Refresh()
        event.Skip()
