import datetime
import pymysql as MySQLdb
import requests
import re

from ID_DEFINE import *

def GetAllMeterialUnitPriceInDB(log, whichDB, Date):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `材料名`,`规格`,`供应商`,`单位`,`价格`,`密度`,`备注`,`市价更新日期`  from `原材料单价表` where `市价更新日期` = '%s' """%(Date)
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    result=[]
    for item in temp:
        item = dict(zip(['材料名','规格','供应商','单位','价格','密度','备注','市价更新日期'], item))
        result.append(item)
    db.close()
    return 0, result

def GetLastUnitPriceInDB(log,whichDB):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("5无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("5无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1
    cursor = db.cursor()
    # sql = """SELECT `材料名`,`单位`,`价格`,`密度`  from `原材料单价表` where `市价更新日期` = '%s' """%(Date)
    sql = """select `市价更新日期` from `原材料单价表` WHERE  `Index`=(select MAX(`Index`) from `原材料单价表`)"""
    cursor.execute(sql)
    temp = cursor.fetchone()
    db.close()
    return temp[0]

def SaveExchangeRateInDB(log,whichDB,exchangeRate,myDate):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql ="SELECT `日期` FROM `美元汇率表` ORDER BY `Index` DESC LIMIT 1"
    cursor.execute(sql)
    Date = cursor.fetchone()
    if Date != None:
        Date = Date[0]
        if Date == myDate:
            sql = """DELETE from `美元汇率表` where `日期`='%s' """ % (Date)
            try:
                cursor.execute(sql)
                db.commit()  # 必须有，没有的话插入语句不会执行
            except:
                print("error new2")
                db.rollback()
    sql = """insert `美元汇率表` (`汇率`,`日期`) values ('%s','%s')"""%(exchangeRate,myDate)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        print("error new2")
        db.rollback()
    db.close()

def SaveMeterialPriceInDB(log,whichDB,dicList,myDate):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return []
    cursor = db.cursor()
    sql ="SELECT `市价更新日期` FROM `原材料单价表` ORDER BY `Index` DESC LIMIT 1"
    cursor.execute(sql)
    Date = cursor.fetchone()[0]
    if Date == myDate:
        sql = """DELETE from `原材料单价表` where `市价更新日期`='%s' """ % (Date)
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error new2")
            db.rollback()
    id = "原材料单价表"
    for dic in dicList:
        dic["市价更新日期"]=myDate
        ls = [(k,dic[k]) for k in dic if dic[k] is not None]
        sql = 'insert `%s` (' %id + ','.join(i[0] for i in ls)+') values ('+','.join('%r' %i[1] for i in ls)+')'
        try:
            cursor.execute(sql)
            db.commit()  # 必须有，没有的话插入语句不会执行
        except:
            print("error new2")
            db.rollback()
    db.close()

def GetExchangeRate():
    global  minimum
    url = 'http://www.boc.cn/sourcedb/whpj/index.html'  # 网址
    html = requests.get(url).content.decode('utf8')  # 获取网页源码（中间涉及到编码问题,这是个大坑，你得自己摸索）
    # 方式一：正则匹配
    a = html.index('<td>美元</td>')  # 取得“美元”当前位置
    s = html[a:a + 400]  # 截取美元汇率那部分内容（从a到a+300位置）
    result = re.findall('<td>(.*?)</td>', s)  # 正则获取
    return float(result[1])
    # if float(result[1]) < minimum:
    #     minimum = float(result[1])
    #     print(datetime.datetime.today(), "出现新低点", result[3])
    # dateStr = str(datetime.datetime.today())[:10] + '.csv'

exExchangeRage=10000
exMinute = -1
exDate = '2022-01-01'
while True:
    minimum = 10000
    Date = str(datetime.date.today())
    minute = datetime.datetime.now().minute
    if exMinute != minute:
        exMinute = minute
        exchangeRate = GetExchangeRate()
        if exchangeRate < exExchangeRage:
            exExchangeRage = exchangeRate
            SaveExchangeRateInDB(None, WHICHDB, exchangeRate, Date)
    if exDate != Date:
        exDate = Date
        Date = GetLastUnitPriceInDB(None,WHICHDB)
        Date = Date.split('-')
        Date = datetime.date(int(Date[0]),int(Date[1]),int(Date[2]))
        if Date != datetime.date.today()-datetime.timedelta(1):
            delta = (datetime.date.today()-Date).days-1
            _, priceList = GetAllMeterialUnitPriceInDB(None,WHICHDB,str(Date))
            for i in range(delta):
                SaveMeterialPriceInDB(None,WHICHDB,priceList,str(Date+datetime.timedelta(i+1)))
