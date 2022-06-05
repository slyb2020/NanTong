import copy
import wx
from DBOperation import GetOrderDetailRecord,GetDeltaWithBluePrintNo,GetConstructionDetailWithDrawingNo,\
    GetPropertyVerticalCuttingParameter,UpdatePanelGlueNoInDB,UpdatePanelWeightInDB
import numpy as np
from operator import itemgetter

class ProductionScheduleAlgorithm(object):
    def __init__(self,log,orderID,suborderNum=None):
        super(ProductionScheduleAlgorithm, self).__init__()
        self.log = log
        self.orderID = orderID
        self.suborderNum = suborderNum
        _, self.orderDetailData = GetOrderDetailRecord(self.log, 1, orderID,suborderNum)
        self.wrongNumber = 0
        self.materialBoard=[]#0:订单号，1：
        self.missList=[]
        self.wallOrderData=[]
        self.ceilingOrderData=[]
        self.constructionOrderData=[]
        self.DisassembleOrderData()#将全部订单数据拆分成墙板，天花板，构件等3个数据列表
        self.CreateGlueNoForOrder()#未全部订单生成胶水单号码
        self.CalculateWeightForOrder()#计算子订单中全部面板的重量，为打包做准备
        for record in self.wallOrderData:
            #record->0:ID,1:订单号,2:子订单号,3:甲板号,4:区域,5:房间,6:图纸号,7:胶水单号,8:X面颜色,9:Y面颜色,10:长,11:宽,12:厚,13:数量,14:Z面颜色,15:V面颜色
            errorCode,delta = self.GetWalllBoardDelta(record)
            if errorCode:
                self.missList.append(record[6])
                self.wrongNumber += 1
            else:
                wallType = record[6].split('.')[1]
                if record[8]=='S.S':
                    boardThickness = 0.7
                elif wallType=='2SP':
                    boardThickness=0.7
                else:
                    boardThickness=0.56
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],boardThickness,int(record[13]),'墙板',record[10],record[11]]#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],boardThickness,int(record[13]),'墙板',record[10],record[11]]
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], boardThickness,int(record[13]),'墙板',record[10],record[11]]
                    self.materialBoard.append(temp)
                if record[15] != 'None'and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], boardThickness,int(record[13]),'墙板',record[10],record[11]]
                    self.materialBoard.append(temp)
        # for record in self.constructionOrderData:
        #     drawingNo = record[6]
        #     errorCode,data = self.CalculateConstructionBoardNeeded(drawingNo)
        #     if errorCode:
        #         self.wrongNumber += 1
        #         self.missList.append(drawingNo)
        #     else:
        #         if data[2]=='L':
        #             temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
        #                     record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
        #         else:
        #             temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'Co',
        #                     record[8], int(record[10]), int(data[1]), float(data[3]), int(record[13]), '构件']
        #         self.materialBoard.append(temp)
        for record in self.ceilingOrderData:
            #record->0:ID,1:订单号,2:子订单号,3:甲板号,4:区域,5:房间,6:图纸号,7:胶水单号,8:X面颜色,9:Y面颜色,10:长,11:宽,12:厚,13:数量,14:Z面颜色,15:V面颜色
            errorCode,delta = self.GetCeilingDelta(record)
            if errorCode:
                self.missList.append(record[6])
                self.wrongNumber += 1
            else:
                boardThickness=0.56
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'X',record[8],
                        int(record[10])+delta[0],int(record[11])+delta[1],boardThickness,int(record[13]),'天花板',record[10],record[11]]#现在的record[12]还是墙板厚，而不是基材厚
                self.materialBoard.append(temp)
                temp = [record[0],record[1],record[2],record[3],record[4],record[5],record[6],"%04d-%04d"%(int(record[1]),int(record[0])),'Y',record[9],
                        int(record[10])+delta[6],int(record[11])+delta[7],boardThickness,int(record[13]),'天花板',record[10],record[11]]
                self.materialBoard.append(temp)
                if record[14] != 'None' and record[14] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'Z',
                            record[14], int(record[10]) + delta[2], int(record[11]) + delta[3], boardThickness,int(record[13]),'天花板',record[10],record[11]]
                    self.materialBoard.append(temp)
                if record[15] != 'None' and record[15] != '0':
                    temp = [record[0], record[1], record[2], record[3], record[4], record[5], record[6],"%04d-%04d"%(int(record[1]),int(record[0])), 'V',
                            record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], boardThickness,int(record[13]),'天花板',record[10],record[11]]
                    self.materialBoard.append(temp)
        self.materialBoard.sort(key=itemgetter(9), reverse=True)
        self.materialBoardList=[]
        kind = []
        temp = []
        thisKind=self.materialBoard[0][9]
        temp.append(self.materialBoard[0])
        for record in self.materialBoard[1:]:
            if thisKind != record[9]:
                kind.append(thisKind)
                self.materialBoardList.append(temp)
                temp = []
            temp.append(record)
            thisKind = record[9]
        kind.append(thisKind)
        self.materialBoardList.append(temp)#把待裁切的板材按原材料的不同分开到不同的列表

        self.cuttingScheduleList=[]
        self.horizontalCuttingScheduleList=[]
        # self.verticalCuttingMaterialBoardList=[[]*len(self.materialBoardList)]
        # self.cuttingMaterialBoardList=[[]*len(self.materialBoardList)]
        # print("self.verticalCuttingMaterialBoardList",self.verticalCuttingMaterialBoardList)
        # print("self.cuttingMaterialBoardList",self.cuttingMaterialBoardList)
        for i in range(len(self.materialBoardList)):
            self.materialBoardList[i].sort(key=itemgetter(12,11,10),reverse=True)#对同一种材料的待裁切板材按厚度度（第一序）、宽度（第二序）及长度（第三序）排序，这一步已验证正确性
            #下面的代码用于统计厚度相同时，各宽度的板材个数，当板材个数超过系统设定的最小启动纵切个数时，将这个厚度的板材都移到纵切计划里
            countList=[]
            currentBoard=self.materialBoardList[i][0]
            amount=currentBoard[13]
            for board in self.materialBoardList[i][1:]:
                if currentBoard[12]==board[12] and currentBoard[11]==board[11]:
                    amount += board[13]
                else:
                    countList.append([currentBoard[9],currentBoard[12],currentBoard[11],amount])
                    currentBoard = board
                    amount = currentBoard[13]
            countList.append([currentBoard[9],currentBoard[12],currentBoard[11],amount])
            #先造出哪些宽度的板材需要移入纵切计划：
            _, minNum = GetPropertyVerticalCuttingParameter(self.log, 1)
            verticalList=[]
            for item in countList:
                if item[3]>=minNum:
                    verticalList.append(item)
            # 下面的代码用于将数量大于设定阈值的板材移入纵切计划，剩余板材移入剪切计划
            if len(verticalList)==0:
                cuttingMaterialBoardList=self.materialBoardList[i]
                horizontalCuttingMaterialBoardList=[]
            else:
                horizontalCuttingMaterialBoardList=[]
                cuttingMaterialBoardList = self.materialBoardList[i]
                for item in verticalList:
                    temp = []
                    for board in cuttingMaterialBoardList:
                        if item[0]==board[9] and item[1]==board[12]:
                            if item[0]==board[9] and item[1]==board[12] and item[2]==board[11]:
                                horizontalCuttingMaterialBoardList.append(board)
                            else:
                                temp.append(board)
                    cuttingMaterialBoardList=temp
            # 下面的代码对需要剪切计划的板子进行剪切计划计算
            # if len(needCuttingBoardList)>0:
            #     needCuttingBoardList.sort(key=itemgetter(12,10,11),reverse=True)#对同一种材料的待裁切板材按厚度度（第一序）、长度（第二序）及宽度（第三序）排序，这一步已验证正确性
            #     mergeMaterialBoardList=[]
            #     currentBoard=needCuttingBoardList[0]
            #     for board in needCuttingBoardList[1:]:
            #         if currentBoard[9]==board[9] and currentBoard[10]==board[10] and currentBoard[11]==board[11] and currentBoard[12]==board[12]:
            #             currentBoard[13] += board[13]
            #         else:
            #             mergeMaterialBoardList.append(currentBoard)
            #             currentBoard = board
            #     mergeMaterialBoardList.append(currentBoard)
            #
            # verticalCuttingMaterialBoardList=[]
            # cuttingMaterialBoardList=[]
            # for board in mergeMaterialBoardList:
            #     # board = [238, 64730, '2', '1', '9', 'Change Room', 'N.2SF.0852', '64730-0238', 'X', 'YQ73D', 2045, 662, 0.56, 1, '墙板', '2045', '605']
            #     _,minNum = GetPropertyVerticalCuttingParameter(self.log,1)
            #     if int(board[13])>=minNum:
            #         verticalCuttingMaterialBoardList.append(board)
            #     else:
            #         cuttingMaterialBoardList.append(board)
            # print("verticalCuttingMaterialBoardList",verticalCuttingMaterialBoardList)
            # print("cuttingMaterialBoardList",cuttingMaterialBoardList)
            if len(cuttingMaterialBoardList)>0:
                cuttingMaterialBoardList.sort(key=itemgetter(12,10,11),reverse=True)
                cuttingSchedule = self.CalculateCuttingSchedule(cuttingMaterialBoardList)#用排列好的板材计算裁切计划，这一步已验证正确性
                cuttingSchedule = self.MergeSameSchedule(cuttingSchedule)#cuttingSchedule是合并之前的裁切计划，如果以此直接打印生成裁切任务单的话，会是很多行。所以还要进行合并同类项处理
                self.cuttingScheduleList.append(cuttingSchedule)

            if len(horizontalCuttingMaterialBoardList)>0:
                horizontalCuttingMaterialBoardList.sort(key=itemgetter(12, 11, 10), reverse=True)
                horizontalCuttingSchedule = self.CalculateVerticalCuttingSchedule(horizontalCuttingMaterialBoardList)
                self.horizontalCuttingScheduleList.append(horizontalCuttingSchedule)

            # verticalCuttingSchedule = self.CalculateVerticalCuttingSchedule(verticalCuttingMaterialBoardList)
            # self.verticalCuttingScheduleList.append(verticalCuttingSchedule)
        # print(self.cuttingScheduleList)
        # self.bendingScheduleList=[]
        self.bendingScheduleList=[]#折弯
        self.S2FormingScheduleList=[]#2S成型
        self.ceilingFormingScheduleList=[]#天花板成型
        self.prScheduleList=[]#PR热压
        self.vacuumScheduleList=[]#特制品热压
        NEED_BEND_PANEL_LIST = ["2SG",'2SA']
        S2FORMING_CEILING_LIST =['C64']
        SOUND_PROOF_PANEL_LIST = ['2SM']
        COLOUR_PLATE_LIST = ['YC94E']
        for i, panel in enumerate(self.wallOrderData):
            #[121, 64730, '2', '1', '9', 'CREW  MESS', 'N.2SF.0867', '0', 'YC08E', 'G', '2160', '200', '25', 1, 'None', 'None']
            if panel[6].split('.')[1] in NEED_BEND_PANEL_LIST:
                self.bendingScheduleList.append(panel)  #角墙板都走折弯
                self.vacuumScheduleList.append(panel) #折弯的都走特制品
            else:
                self.S2FormingScheduleList.append(panel) #平墙板都走2S成型
                if int(panel[11])<=200 or panel[6].split('.')[1] in SOUND_PROOF_PANEL_LIST:#宽度小于200的平墙板，隔音板，双面带颜色板也走特质平
                    self.vacuumScheduleList.append(panel)
                else:
                    if panel[8] in COLOUR_PLATE_LIST and panel[9] in COLOUR_PLATE_LIST:
                        self.vacuumScheduleList.append(panel)
                    else:
                        self.prScheduleList.append(panel)

        for i, panel in enumerate(self.ceilingOrderData):
            #[121, 64730, '2', '1', '9', 'CREW  MESS', 'N.2SF.0867', '0', 'YC08E', 'G', '2160', '200', '25', 1, 'None', 'None']
            self.prScheduleList.append(panel)#所有天花板都走PR热压
            if panel[6].split('.')[1] in S2FORMING_CEILING_LIST:
                self.S2FormingScheduleList.append(panel)  #C64天花板走2S成型
            else:
                self.ceilingFormingScheduleList.append(panel) #其它所有天花板都走2S天花板成型

        # print("bendScheduleList", self.bendingScheduleList)#折弯
        # print("S2RFormingScheduleList", self.S2FormingScheduleList)#2S成型
        # print("ceilingFormingScheduleList",self.ceilingFormingScheduleList)#天花板成型
        # print("prScheduleList",self.prScheduleList)#PR热压
        # print("vacuumScheduleList",self.vacuumScheduleList)#特制品热压

        # self.orticFormingScheduleList=[] #构件成型

    def CalculateVerticalCuttingSchedule(self,data):
        # board = [11, 64730, '1', '3', '9', 'Corridor', 'A.2SF.0900', '64730-0011', 'X', 'YC74H', 2160, 213, 0.56, 29,'墙板', '2160', '205']
        result = []
        exBoard = data[0]
        temp = [exBoard[9],exBoard[12],exBoard[11],[[exBoard[10],exBoard[13]]]]
        for board in data[1:]:
            if board[9]==exBoard[9] and board[12]==exBoard[12] and board[11]==exBoard[11]:
                if board[10]==exBoard[10]:
                    temp[-1][-1][-1] += int(board[13])
                else:
                    temp[-1].append([board[10],board[13]])
                    exBoard=board
            else:
                result.append(temp)
                exBoard = board
                temp = [exBoard[9],exBoard[12],exBoard[11],[[exBoard[10],exBoard[13]]]]
        result.append(temp)
        return result



    def CalculateCuttingSchedule(self, data):
        # boardName = data[0][9]  #获得板材名称
        # boardThickness = data[0][12]#获得板材厚度
        dataList = []
        for record in data:  # 将待裁切板材按单块列表
            for i in range(int(record[13])):
                temp = record[:13]
                temp.append(1)
                dataList.append(temp)
        sameLenthBoardListSet = []
        temp = []
        thisLength = dataList[0][10]
        temp.append(dataList[0])
        for record in dataList[1:]:  # 把同一种板材，按相同长度分堆
            if thisLength != record[10]:
                sameLenthBoardListSet.append(temp)
                temp = []
            temp.append(record)
            thisLength = record[10]
        sameLenthBoardListSet.append(temp)
        result = []
        for sameLenthBoardList in sameLenthBoardListSet:
            CuttingFinish = False
            while not CuttingFinish:  # 循环调用直到将所有待裁切板材全部裁切完毕
                result, sameLenthBoardList = self.MakeHorizontalCutting(result,
                                                                        sameLenthBoardList)  # 每次待用都开始一次新的横切
                temp = []
                for record in sameLenthBoardList:
                    if record[-1] > 0:
                        temp.append(record)
                sameLenthBoardList = temp
                CuttingFinish = False if len(sameLenthBoardList) > 0 else True
        return result

    def MergeSameSchedule(self,data):
        # [['YQ73D', 2160, 1234], [553, 553]]
        result = []
        exBoard = data[0][0]
        horizentalCuttingBoard = exBoard
        horizentalCuttingBoard.append(1)
        verticalCuttingBoard = [data[0][1]]
        for horizentalCutting,verticalCutting in data[1:]:#第一步合并相同的横切
            if horizentalCutting[1]==exBoard[1] and horizentalCutting[2]==exBoard[2] and horizentalCutting[3]==exBoard[3]:
                horizentalCuttingBoard[-1] = horizentalCuttingBoard[-1]+1
                verticalCuttingBoard.append(verticalCutting)
            else:
                result.append([horizentalCuttingBoard,verticalCuttingBoard])
                exBoard=horizentalCutting
                horizentalCuttingBoard = horizentalCutting
                horizentalCuttingBoard.append(1)
                verticalCuttingBoard=[verticalCutting]
        result.append([horizentalCuttingBoard,verticalCuttingBoard])
        # for record in result:
        #     print("after Merge step1:",record)
        for i, schedule in enumerate(result):#第二部再合并相同的纵切
            verticalCuttingList=[]
            exVerticalCutting=schedule[1][0]
            amount=1
            for verticalCutting in schedule[1][1:]:
                # print("verticalCutting",verticalCutting,exVerticalCutting)
                if verticalCutting == exVerticalCutting:
                    amount+=1
                else:
                    verticalCuttingList.append([exVerticalCutting,amount])
                    exVerticalCutting=verticalCutting
                    amount=1
            verticalCuttingList.append([exVerticalCutting,amount])
            result[i] = [schedule[0],verticalCuttingList]
        return result

    def MakeHorizontalCutting(self,result,data):
        verticalCutting = [] #用于存储本次的纵切计划
        verticalCutting.append(data[0][11])
        restWidth=1234-data[0][11]   #剩余板材宽度，长度由第一块板确定
        data[0][13]=0
        for i,board in enumerate(data[1:]):
            if board[11] <= restWidth:
                restWidth -= board[11]
                verticalCutting.append(board[11])
                data[i+1][-1]=0#因为是从data[1]开始循环的，所以这里i要加一*******
                if restWidth<data[-1][11]:
                    break
        result.append([[data[0][9],data[0][12],1234,data[0][10]],verticalCutting])#第一部分位横切板材，第二部分位纵切计划
        return result,data

    def CreateGlueNoForOrder(self):
        self.panelList=[]
        for data in self.wallOrderData:
            glueNo="%05d-%04d"%(data[1],data[0])
            temp = list(data)
            temp[-1]=glueNo
            self.panelList.append(temp)
            UpdatePanelGlueNoInDB(self.log, 1, self.orderID, data[0], glueNo)
        for data in self.ceilingOrderData:
            glueNo="%05d-%04d"%(data[1],data[0])
            temp = list(data)
            temp[-1]=glueNo
            self.panelList.append(temp)
            UpdatePanelGlueNoInDB(self.log, 1, self.orderID, data[0], glueNo)

    def CalculateWeightForOrder(self):#这里计算的是单板重量，并没有乘以Amount
        for i, data in enumerate(self.panelList):
            if data[6][2:5]=='C55':
                weight = float(data[10])*float(data[11])/1.0E6*12.0
            else:
                if int(data[12])==25:
                    weight = float(data[10]) * float(data[11]) / 1.0E6 * 12.0
                elif int(data[12])==50:
                    weight = float(data[10]) * float(data[11]) / 1.0E6 * 17
                else:
                    weight = float(data[10]) * float(data[11]) / 1.0E6 * 20.0 #100的板子应该还有一个新的重量系数,暂时取20.0
            UpdatePanelWeightInDB(self.log, 1, self.orderID, data[0], weight)

    def DisassembleOrderData(self):
        for data in self.orderDetailData:
            temp = str(data[6])
            if '.' not in temp:
                index = temp[0]+'.'+temp[1:4]+'.'+temp[4:]
            else:
                index = temp
            temp = index.split('.')
            if str(temp[1]).isdigit():
                self.constructionOrderData.append(data)
            elif temp[1][0]=='C':
                self.ceilingOrderData.append(data)
            else:
                self.wallOrderData.append(data)

    def GetWalllBoardDelta(self, orderRecord):
        delta = self.GetDeltaWithBluePrintNo(orderRecord[6])
        if delta!=None:#说明返回了有效的增减量
            frontLengthDelta = int(delta[0].split(',')[0])
            frontWidthDelta = int(delta[0].split(',')[1])
            m1LengthDelta = int(delta[1].split(',')[0])
            m1WidthDelta = int(delta[1].split(',')[1])
            m2LengthDelta = int(delta[1].split(',')[2])
            m2WidthDelta = int(delta[1].split(',')[3])
            rearLengthDelta = int(delta[2].split(',')[0])
            rearWidthDelta = int(delta[2].split(',')[1])
            return 0,[frontLengthDelta,frontWidthDelta,m1LengthDelta,m1WidthDelta,m2LengthDelta,m2WidthDelta,rearLengthDelta,rearWidthDelta]
        else:
            return 1,[]

    def GetCeilingDelta(self, orderRecord):
        delta = self.GetDeltaWithBluePrintNo(orderRecord[6])
        if delta!=None:#说明返回了有效的增减量
            frontLengthDelta = int(delta[0].split(',')[0])
            frontWidthDelta = int(delta[0].split(',')[1])
            m1LengthDelta = int(delta[1].split(',')[0])
            m1WidthDelta = int(delta[1].split(',')[1])
            m2LengthDelta = int(delta[1].split(',')[2])
            m2WidthDelta = int(delta[1].split(',')[3])
            rearLengthDelta = int(delta[2].split(',')[0])
            rearWidthDelta = int(delta[2].split(',')[1])
            return 0,[frontLengthDelta,frontWidthDelta,m1LengthDelta,m1WidthDelta,m2LengthDelta,m2WidthDelta,rearLengthDelta,rearWidthDelta]
        else:
            return 1,[]

    def CalculateConstructionBoardNeeded(self, drawingNo):
        """record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], 'V',
        record[15], int(record[10]) + delta[4], int(record[11]) + delta[5], int(record[12])]"""
        error,data = GetConstructionDetailWithDrawingNo(self.log,1,drawingNo)
        if data!=None:#说明返回了有效的构件数据
            return False,data
        return True,data

    def GetDeltaWithBluePrintNo(self,bluePrintNo):
        if '.' not in bluePrintNo:
            if len(bluePrintNo)<10:
                try:
                    index = int(bluePrintNo[4:])
                except:
                    index = int(bluePrintNo[5:])
                bluePrintNo = bluePrintNo[0]+'.'+bluePrintNo[1:4]+'.%04d'%index
        _,delta = GetDeltaWithBluePrintNo(self.log,1,bluePrintNo)
        return delta
