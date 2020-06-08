# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '道路中心线.py'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import pandas as pd

######todo 中心城区路网密度

data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\table最终.xls')
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中心线二环标识.xls')
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中心线0605out.xls')#todo 0605中心线更改部分
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中心线加OD.xls')#todo 中心线赵元辰加OD
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中心线标识行政区.xls')#todo 沙沙姐要数据

fenqutongji=True
if fenqutongji==True:
    data=data[data['区域']=='东部城区']#todo 东部城区
    data=data[data['区域']=='西部城区']#todo 西部城区
    data=data[data['区域']=='主城区']#todo 主部城区    2.整个绕城封闭范围内
    data=data[data['标识']!='交通局外']#todo 交通局管辖区域
    data=data[data['FID_二环']==0]#todo    3.整个二环封闭范围内

    data=data[data['NAME_1']=='历城区']#todo
    data=data[data['NAME_1']=='历下区']#todo
    data=data[data['NAME_1']=='槐荫区']#todo
    data=data[data['NAME_1']=='天桥区']#todo
    data=data[data['NAME_1']=='市中区']#todo

#todo 现状快主次支汇总表

data2=data[data.Finished!=1]# 现状

data_k=data2[data2.GHDLDJ=='快速路']# 现状 快
# data_k=data_k.groupby(['RoadName','GHDLDJ','GH_width', 'XZ_width','JDCDS','Finished','区域','Layer'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_k=data_k.groupby(['RoadName','O','D','GHDLDJ','GH_width', 'XZ_width','Finished','JDCDS'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_k.to_csv(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_快.csv',encoding='utf-8-sig')

data_zhu=data2[data2.GHDLDJ=='主干路']# 现状 主
# data_zhu=data_zhu.groupby(['RoadName','GHDLDJ','GH_width', 'XZ_width','JDCDS','Finished','区域','Layer'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_zhu=data_zhu.groupby(['RoadName','O','D','GHDLDJ','GH_width', 'XZ_width','Finished','JDCDS'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_zhu.to_csv(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_主.csv',encoding='utf-8-sig')

data_ci=data2[data2.GHDLDJ=='次干路']# 现状 次
# data_ci=data_ci.groupby(['RoadName','GHDLDJ','GH_width', 'XZ_width','JDCDS','Finished','区域','Layer'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_ci=data_ci.groupby(['RoadName','O','D','GHDLDJ','GH_width', 'XZ_width','Finished','JDCDS'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_ci.to_csv(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_次.csv',encoding='utf-8-sig')

data_zz=data2[data2.GHDLDJ=='支路']# 现状 支
# data_zz=data_zz.groupby(['RoadName','GHDLDJ','GH_width', 'XZ_width','JDCDS','Finished','区域','Layer'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_zz=data_zz.groupby(['RoadName','O','D','GHDLDJ','GH_width', 'XZ_width','Finished','JDCDS'],as_index=False)['Length'].sum().sort_values(['GHDLDJ','Finished','RoadName'],ascending=False).reset_index(drop=True)
data_zz.to_csv(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_支.csv',encoding='utf-8-sig')



import webbrowser
webbrowser.open(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_快.csv')
webbrowser.open(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_主.csv')
webbrowser.open(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_次.csv')
webbrowser.open(r'E:\桌面文件夹\路网普查数据\道路中心线汇总表_支.csv')


# data=pd.read_excel(r'E:\桌面文件夹\绕城以外道路.xls')
# data0=data[data.Finished==0]
data0 = data[data.Finished != 1]  ##todo 快速路含匝道
# data0 = data0[data0['匝道'] != 1]##todo 快速路不含匝道
# data2=data[data.Finished==0]
list0 = data0.groupby('GHDLDJ').Length.sum()


list0_km = round(list0 / 1000, 1)
# print('不同等级道路长度（km）：',list0_km.sort_values())
print('高速', list0_km['高速'])
try:
    print('快速路', '主线长度：115.8km,总长度(含引导线)：', list0_km['快速路'])
except:
    print('快速路', '主线长度：115.8km,总长度(含引导线)：',0)
print('主干路', list0_km['主干路'])
print('次干路', list0_km['次干路'])
print('支路', list0_km['支路'])
print('路网总长度：', round(sum(list0_km),1))

zhucizhi = list0_km['主干路'] + list0_km['次干路'] + list0_km['支路']
print(
    '主次支比例：{}:{}:{}'.format(1, round(list0_km['次干路'] / list0_km['主干路'], 1), round(list0_km['支路'] / list0_km['主干路'], 2)))


print('####################')
list_midu = round(list0_km / 462, 3)
# print('不同等级道路密度：',list0_km.sort_values())
print('高速', list_midu['高速'])
try:
    print('快速路', list_midu['快速路'])
except:
    print('快速路', 0)
print('主干路', list_midu['主干路'])
print('次干路', list_midu['次干路'])
print('支路', list_midu['支路'])
print('####################')
zongmidu = ((list0['主干路'] + list0['次干路'] + list0['支路'] + list0['快速路']++ list0['高速']) / 1000) / 462
print('总密度：', round(zongmidu, 1))
## todo 道路面积率
roadarea = round(sum(data0.Length * data0.XZ_width) / (10 ** 6), 1)
print('道路面积{}'.format(roadarea))
print('道路面积率（km2）:{}%'.format(round((roadarea / 462) * 100, 1)))
## todo Finished字段道路长度统计
# data.groupby(['GHDLDJ','Finished']).Length.sum()/1000
def text1():
    # todo 规划
    gaoguihua = round(data[(data.Finished != 5) & (data.GHDLDJ == '高速')].Length.sum() / 1000,1)
    kuaiguihua = round(data[(data.Finished != 5) & (data.GHDLDJ == '快速路')].Length.sum() / 1000,1)
    zhuguihua = round(data[(data.Finished != 5) & (data.GHDLDJ == '主干路')].Length.sum() / 1000,1)
    ciguihua = round(data[(data.Finished != 5) & (data.GHDLDJ == '次干路')].Length.sum() / 1000,1)
    zhiguihua = round(data[(data.Finished != 5) & (data.GHDLDJ == '支路')].Length.sum() / 1000,1)

    print('规划高速长度：{}km'.format(gaoguihua))
    print('规划快速路长度：{}km'.format(kuaiguihua))
    print('规划主干路长度：{}km'.format(zhuguihua))
    print('规划次干路长度：{}km'.format(ciguihua))
    print('规划支路长度：{}km'.format(zhiguihua))

    columns=['规划路网长度','已完成规划','尚未按照规划形成','现状存在但未规划','未建设']
    list_out=pd.DataFrame(columns=columns)

    list_out['规划路网长度']=[gaoguihua,kuaiguihua,zhuguihua,ciguihua,zhiguihua]

    # todo 现状建成
    gaoguihuafinish0 = round(data[(data.Finished == 0) & (data.GHDLDJ == '高速')].Length.sum() / 1000,1)
    kuaiguihuafinish0 = round(data[(data.Finished == 0) & (data.GHDLDJ == '快速路')].Length.sum() / 1000,1)
    zhuguihuafinish0 = round(data[(data.Finished == 0) & (data.GHDLDJ == '主干路')].Length.sum() / 1000,1)
    ciguihuafinish0 = round(data[(data.Finished == 0) & (data.GHDLDJ == '次干路')].Length.sum() / 1000,1)
    zhiguihuafinish0 = round(data[(data.Finished == 0) & (data.GHDLDJ == '支路')].Length.sum() / 1000,1)
    print('现状建成高速长度：{}km'.format(gaoguihuafinish0))
    print('现状建成快速路长度：{}km'.format(kuaiguihuafinish0))
    print('现状建成主干路长度：{}km'.format(zhuguihuafinish0))
    print('现状建成次干路长度：{}km'.format(ciguihuafinish0))
    print('现状建成支路长度：{}km'.format(zhiguihuafinish0))
    list_out['已完成规划']=[gaoguihuafinish0,kuaiguihuafinish0,zhuguihuafinish0,ciguihuafinish0,zhiguihuafinish0]
    # todo 未按规划形成
    gaoguihuafinish2 = round(data[(data.Finished == 2) & (data.GHDLDJ == '高速')].Length.sum() / 1000,1)
    kuaiguihuafinish2 = round(data[(data.Finished == 2) & (data.GHDLDJ == '快速路')].Length.sum() / 1000,1)
    zhuguihuafinish2 = round(data[(data.Finished == 2) & (data.GHDLDJ == '主干路')].Length.sum() / 1000,1)
    ciguihuafinish2 = round(data[(data.Finished == 2) & (data.GHDLDJ == '次干路')].Length.sum() / 1000,1)
    zhiguihuafinish2 = round(data[(data.Finished == 2) & (data.GHDLDJ == '支路')].Length.sum() / 1000,1)
    print('未按规划形成高速长度：{}km'.format(gaoguihuafinish2))
    print('未按规划形成快速路长度：{}km'.format(kuaiguihuafinish2))
    print('未按规划形成主干路长度：{}km'.format(zhuguihuafinish2))
    print('未按规划形成次干路长度：{}km'.format(ciguihuafinish2))
    print('未按规划形成支路长度：{}km'.format(zhiguihuafinish2))
    list_out['尚未按照规划形成']=[gaoguihuafinish2,kuaiguihuafinish2,zhuguihuafinish2,ciguihuafinish2,zhiguihuafinish2]

    # todo 现状存在但未规划
    gaoguihuafinish5 = round(data[(data.Finished == 5) & (data.GHDLDJ == '高速')].Length.sum() / 1000,1)
    kuaiguihuafinish5 = round(data[(data.Finished == 5) & (data.GHDLDJ == '快速路')].Length.sum() / 1000,1)
    zhuguihuafinish5 = round(data[(data.Finished == 5) & (data.GHDLDJ == '主干路')].Length.sum() / 1000,1)
    ciguihuafinish5 = round(data[(data.Finished == 5) & (data.GHDLDJ == '次干路')].Length.sum() / 1000,1)
    zhiguihuafinish5 = round(data[(data.Finished == 5) & (data.GHDLDJ == '支路')].Length.sum() / 1000,1)
    print('未建设高速长度：{}km'.format(gaoguihuafinish5))
    print('未建设快速路长度：{}km'.format(kuaiguihuafinish5))
    print('未建设主干路长度：{}km'.format(zhuguihuafinish5))
    print('未建设次干路长度：{}km'.format(ciguihuafinish5))
    print('未建设支路长度：{}km'.format(zhiguihuafinish5))
    list_out['现状存在但未规划']=[gaoguihuafinish5,kuaiguihuafinish5,zhuguihuafinish5,ciguihuafinish5,zhiguihuafinish5]

    # todo 未建设
    gaoguihuafinish1 = round(data[(data.Finished == 1) & (data.GHDLDJ == '高速')].Length.sum() / 1000,1)
    kuaiguihuafinish1 = round(data[(data.Finished == 1) & (data.GHDLDJ == '快速路')].Length.sum() / 1000,1)
    zhuguihuafinish1 = round(data[(data.Finished == 1) & (data.GHDLDJ == '主干路')].Length.sum() / 1000,1)
    ciguihuafinish1 = round(data[(data.Finished == 1) & (data.GHDLDJ == '次干路')].Length.sum() / 1000,1)
    zhiguihuafinish1 = round(data[(data.Finished == 1) & (data.GHDLDJ == '支路')].Length.sum() / 1000,1)
    print('未建设高速长度：{}km'.format(gaoguihuafinish1))
    print('未建设快速路长度：{}km'.format(kuaiguihuafinish1))
    print('未建设主干路长度：{}km'.format(zhuguihuafinish1))
    print('未建设次干路长度：{}km'.format(ciguihuafinish1))
    print('未建设支路长度：{}km'.format(zhiguihuafinish1))
    list_out['未建设']=[gaoguihuafinish1,kuaiguihuafinish1,zhuguihuafinish1,ciguihuafinish1,zhiguihuafinish1]
    list_out.index=['高速','快速路','主干路','次干路','支路']
    list_out.to_csv(r'E:\桌面文件夹\路网普查PPT\out_data.csv',encoding='utf-8-sig')

    print('导出完成')
text1()
import webbrowser
webbrowser.open(r'E:\桌面文件夹\路网普查PPT\out_data.csv')



# import matplotlib.pyplot as plt
#
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
# plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
# plt.bar(list0.index,round(list0/1000,1).values)
# for i in range(len(list0.index)):
#     print(i)
#     plt.text(list0.index[i], list(round(list0/1000,1)+1)[i], '%.02f' % list(round(list0/1000,1))[i],ha='center', va= 'bottom',fontsize=11)
#
# plt.show()


