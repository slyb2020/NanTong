import os
from ID_DEFINE import bluePrintDir

# 获取该目录下所有文件，存入列表中
fileList = os.listdir(bluePrintDir+'构件/')

n = 0
for i in fileList:
    # 设置旧文件名（就是路径+文件名）
    oldname = bluePrintDir+'构件/'+i  # os.sep添加系统分隔符

    newname = bluePrintDir+'构件/'+i[-13:]

    os.rename(oldname, newname)  # 用os模块中的rename方法对文件改名
    print(oldname, '======>', newname)

