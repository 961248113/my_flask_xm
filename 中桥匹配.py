import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中桥匹配.xls')#gis数据
# data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\桥梁录入系统.xlsx')#excel原表格数据
# data = data[data.id != 0]
# num = data.shape[0]

LENGTH_qiao = round(data.groupby('桥梁类')['桥梁全'].sum()/ 1000,1)
# LENGTH_qiao = round(data.groupby('桥梁类型')["桥梁全长（m）"].sum()/ 1000,2)


# LENGTH_qiao = round(data['桥梁全'].sum() / 1000, 2)
qiao_num=data.groupby('桥梁类')['桥梁名'].count()
# print('中桥数量为{}，桥梁总长度为{}'.format(num, LENGTH_qiao))
