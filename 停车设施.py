from pyecharts import Pie
import pandas as pd
import numpy as np
import folium
import webbrowser
from folium.plugins import HeatMap

pd.set_option('display.max_columns', None)

data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\停车设施.xls')
# data.head(1)
data = data[(data["NAME"] == '长清区') | (data["NAME"] == '市中区') | (data["NAME"] == '槐荫区') | (data["NAME"] == '天桥区') | (
    data["NAME"] == '历城区') | (data["NAME"] == '历下区')]
print('停车场数：{}处'.format(len(data)))
data.head()
boweishu = data.groupby('类型')['泊位数'].sum().reset_index()
tingchechangshu = data.groupby('类型')['FID'].count().reset_index()
print('每一类的停车泊位数:', boweishu)
print('停车场数量：',tingchechangshu)
#todo 饼图
attr = boweishu['类型']
v1 = boweishu['泊位数']

# attr = tingchechangshu['类型']
# v1 = tingchechangshu['FID']



pie = Pie("")  # , title_pos='center'
pie.add(
    "",
    attr,
    v1,
    is_label_show=True,
    is_more_utils=True
)
pie.render(path=r"E:\桌面文件夹\路网普查数据\停车设施泊位饼状图.html")
webbrowser.open(r"E:\桌面文件夹\路网普查数据\停车设施泊位饼状图.html")
# pie.render(path=r"E:\桌面文件夹\路网普查数据\停车场数量饼状图.html")
# webbrowser.open(r"E:\桌面文件夹\路网普查数据\停车场数量饼状图.html")

#todo 热力图
df = data
#  获取数据个数
num = df.shape[0]
#  获取纬度
lat = np.array(df["lat"][0:num])
#  获取经度
lon = np.array(df["lng"][0:num])
#  获取PM2.5，转化为numpy浮点型
bws = np.array(df["泊位数"][0:num], dtype=float)
#  将数据制作成[lats, lons, weights]的形式
data1 = [[lat[i], lon[i], bws[i]] for i in range(num)]
#  绘制Map，中心经纬度[32, 120],开始缩放程度是5倍
map_osm = folium.Map(location=[36.6054, 117.178001], zoom_start=5)
#  将热力图添加到前面建立的map里
HeatMap(data1).add_to(map_osm)
file_path = r"E:\桌面文件夹\路网普查数据\停车设施热力图.html"
#  保存为html文件
map_osm.save(file_path)
#  默认浏览器打开
webbrowser.open(file_path)
