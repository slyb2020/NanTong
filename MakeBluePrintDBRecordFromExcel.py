from ExcelOperation import GetSheetNameListFromExcelFileName,GetSheetDataFromExcelFileName
import numpy as np
from ID_DEFINE import *
import pymysql as MySQLdb
import time
import datetime


def InsertBluePrintInDB(log,whichDB,drawingNoList,aList,bList,cList,dList,eList,fList,cyList,sheetName,frontDelta,middleDelta,rearDelta):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接智能生产管理系统数据库!", "错误信息")
        if log:
            log.WriteText("无法连接智能生产管理系统数据库", colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    print(len(drawingNoList),len(aList),len(bList))
    for i,drawingNo in enumerate(drawingNoList):
        if len(aList)>0:
            aEnable = 'Y'
            a = aList[i]
        else:
            aEnable = 'N'
            a='0'
        if len(bList)>0:
            bEnable = 'Y'
            b = bList[i]
        else:
            bEnable = 'N'
            b='0'
        if len(cList)>0:
            cEnable = 'Y'
            c = cList[i]
        else:
            cEnable = 'N'
            c='0'
        if len(dList)>0:
            dEnable = 'Y'
            d = dList[i]
        else:
            dEnable = 'N'
            d='0'
        if len(eList)>0:
            eEnable = 'Y'
            e = eList[i]
        else:
            eEnable = 'N'
            e='0'
        if len(fList)>0:
            fEnable = 'Y'
            f = fList[i]
        else:
            fEnable = 'N'
            f ='0'
        if len(cyList)>0:
            cyEnable = 'Y'
            cy = ctList[i]
        else:
            cyEnable = 'N'
            cy='0'
        sql = "INSERT INTO 图纸信息(`图纸号`,`a使能`,`a`,`b使能`,`b`,`c使能`,`c`,`d使能`,`d`," \
              "`e使能`,`e`,`f使能`,`f`,`CY使能`,`CY`,`图纸名`,`面板增量`,`中板增量`,`背板增量`)" \
              "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"\
              % (drawingNo,aEnable,a,bEnable,b,cEnable,c,dEnable,d,eEnable,e,fEnable,f,cyEnable,cy,sheetName,frontDelta,middleDelta,rearDelta)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            db.rollback()
    db.close()


fileName = 'D:\\WorkSpace\\python\\NanTong_YNKS\\Excel\\Stena 生产图纸 2SG.xlsx'
aaa = GetSheetNameListFromExcelFileName(fileName)
for sheetName in aaa:
    print(sheetName)
    d = GetSheetDataFromExcelFileName(fileName,sheetName)
    sheetData = np.array(d)
    frontDelta = sheetData[1,0]
    middleDelta = sheetData[2,0]
    rearDelta = sheetData[3,0]
    sheetData = sheetData[:,1:]
    titleData = list(sheetData[0,:])
    title = []
    for i in titleData:
        try:
            i = i.strip()
        except:
            pass
        title.append(i)
    print(title)
    drawingNo = []
    if "Drawing no." in title:
        index = title.index("Drawing no.")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                drawingNo.append(i)
            except:
                pass
    aList = []
    if "a" in title:
        index = title.index("a")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                aList.append(i)
            except:
                aList.append(i)
    bList = []
    if "b" in title:
        index = title.index("b")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                bList.append(i)
            except:
                bList.append(i)
    cList=[]
    if "c" in title:
        index = title.index("c")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                cList.append(i)
            except:
                cList.append(i)
    dList=[]
    if "d" in title:
        index = title.index("d")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                dList.append(i)
            except:
                dList.append(i)
    eList=[]
    if "e" in title:
        index = title.index("e")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                eList.append(i)
            except:
                eList.append(i)
    fList=[]
    if "f" in title:
        index = title.index("f")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                fList.append(i)
            except:
                fList.append(i)
    cyList=[]
    if "CY" in title:
        index = title.index("CY")
        temp = sheetData[1:,index]
        for i in temp:
            try:
                i = i.strip()
                cyList.append(i)
            except:
                cyList.append(i)
    drawingNoList=[]
    for no in drawingNo:
        no = no.split('.')
        try:
            temp = int(no[2])
        except:
            temp = int(no[2][1:])
        no[2] = "%04d"%temp
        temp = "%s.%s.%s"%(no[0],no[1],no[2])
        drawingNoList.append(temp)
    print(drawingNoList,aList,bList,cList,dList,eList,fList,cyList,sheetName)
    InsertBluePrintInDB(None,1,drawingNoList,aList,bList,cList,dList,eList,fList,cyList,sheetName,frontDelta,middleDelta,rearDelta)



