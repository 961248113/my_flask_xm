from pyecharts import Pie
import pandas as pd
import numpy as np
import folium
import webbrowser
from folium.plugins import HeatMap

pd.set_option('display.max_columns', None)

# data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\公交专用道.xls')
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\gj专用道.xls')
# b=data.groupby(['RoadName','起点','终点','专用道','专用_1'],as_index=False)['长度'].sum()
#todo 导出后部分路段存在问题，需要手动调整
b=data.groupby(['道路名','RoadName','起点','终点','专用道','专用_1'],as_index=False)['长度'].sum().sort_values('专用道',ascending=False).reset_index(drop=True)
b.to_csv(r'E:\桌面文件夹\路网普查数据\公交专用道汇总表.csv',encoding='utf-8-sig')


print('专用道总长度为：', round(data['长度'].sum(), 2))
zhuanyongdao = round(data.groupby('专用道')['长度'].sum(), 2)
luce=zhuanyongdao['单向路侧']+zhuanyongdao['节假日专用道（限时专用道）']+zhuanyongdao['限时公交专用道']

print('单向路侧长度',zhuanyongdao['单向路侧'])
print('双向路侧长度',zhuanyongdao['节假日专用道（限时专用道）']+zhuanyongdao['限时公交专用道'])

data1=zhuanyongdao.reset_index()

attr = data1['专用道']
v1 = data1['长度']

pie = Pie("")  # , title_pos='center'
pie.add(
    "",
    attr,
    v1,
    is_label_show=True,
    is_more_utils=True
)
pie.render(path=r"E:\桌面文件夹\路网普查数据\公交专用道长度饼状图.html")
webbrowser.open(r"E:\桌面文件夹\路网普查数据\公交专用道长度饼状图.html")