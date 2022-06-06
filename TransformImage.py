# -*- encoding: utf-8 -*-
import base64
import pymysql as MySQLdb
# import MySQLdb
#impo
def TransformBase64(fileName):
    """
    image -> base64
    :param fileName:
    :return:
    """
    # img_path = "./%s.png" % img_name
    # img_path = "%s" % fileName
    try:
        with open(fileName, 'rb') as file:
            fileData = file.read()
            base64_data = base64.b64encode(fileData)  # 'bytes'型数据
            str_base64_data = base64_data.decode()#str型数据
            return str_base64_data
    except:
        return "erro"

def UpdateInfoImage(kinfe_name):
    data=TransformBase64(kinfe_name)
    if data != "erro":
        # DB = MySQLdb.connect(host="%s" % host_name, user='%s' % user_name, passwd='%s' % passwd_name, db='%s' %DATABASE_NAME[6],charset='utf8')
        DB = MySQLdb.connect(host='127.0.0.1',user="root", passwd="12345678", db="dingzhikeji", charset='utf8')
        cursor = DB.cursor()
        cursor.execute(
            "UPDATE `info_tools` set `info_image`='%s' WHERE `kinfe_name`='%s'" % (data,"TJDZ_1"))
        DB.commit()
        print("success")
    else:
        print("erro2")

def ReadInfoImage(kinfe_name):
    DB = MySQLdb.connect(host='127.0.0.1', user='root', passwd='12345678', db="dingzhikeji", charset='utf8')
    cursor = DB.cursor()
    cursor.execute("select `info_image`  from `info_tools` where `kinfe_name`='%s'" %(kinfe_name))
    record=cursor.fetchone()
    return record

def ShowImage(kinfe_name):
    """
    base64 -> image
    :return:
    """
    kinfe_name=ReadInfoImage(kinfe_name)
    with open('TJDZ_1.jpg', 'wb') as file:
        image = base64.b64decode(kinfe_name[0])  # 解码
        file.write(image)

if __name__ == '__main__':
    info=ShowImage("TJDZ_1")
    # info=UpdateInfoImage("TJDZ_1")