import os
for root, dirs, files in os.walk("D:\\WorkSpace\\Python\\NanTong_YNKS\\工单"):
    print(root,dirs,files)

directoryList = list(os.walk("D:\\WorkSpace\\Python\\NanTong_YNKS\\工单"))
print("directoryList=",directoryList[0][1])