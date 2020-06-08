import pandas as pd
import folium
import webbrowser
from folium.plugins import HeatMap
import numpy as np
######todo 中心城区路网密度
# data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\公交中途站2.xls')#todo 原始
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\中途站附加道路 - 副本.xls')#todo 匹配道路
# data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\公交站点最终2.xls')#todo 匹配道路
data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\公交站点标识区域最终.xls')#todo 匹配道路
# 查看 齐鲁软件园东 站点，确定经纬度有效字段：'lng_avg'(计算方法为：在'lng_avg1'上再取均值)
# todo 公交站点数量统计（不含莱芜章丘）
# data=data[(data["NAME"] != '章丘区')]
data = data[(data["NAME"] == '长清区') | (data["NAME"] == '市中区') | (data["NAME"] == '槐荫区') | (data["NAME"] == '天桥区') | (
    data["NAME"] == '历城区') | (data["NAME"] == '历下区')]

#todo 导出数据

# data_zt=data[data['区域']=='中心城区']#todo 中心城区
data_zt=data #todo 不含莱芜
# data_zt_luzhong=data_zt[data_zt['luzhong_ce']=='路中']
# data_zt_luce=data_zt[data_zt['luzhong_ce']=='路侧']
# data_zt_luzhong_dt=data_zt_luzhong.groupby(['stopname'],as_index=False)['routename'].count().reset_index(drop=True)
# data_zt_luce_dt=data_zt_luzhong.groupby(['stopname','方位'],as_index=False)['routename'].count().reset_index(drop=True)
za=data_zt.groupby(['stopname','方位','luzhong_ce','roadname'],as_index=True)#[['lng_avg','lat_avg','routename']]#所有字段

station_pass_route = pd.DataFrame(za['routename'].unique().reset_index())
station_pass_route['pass_route_num'] = station_pass_route['routename'].apply(lambda x: len(x))

station_pass_route1 = station_pass_route[station_pass_route.luzhong_ce=='路侧']
station_pass_route2 = station_pass_route[station_pass_route.luzhong_ce=='路中'].drop_duplicates(['stopname','roadname'],keep='first')
station_pass_route2['方位']='路中'
station_pass_route_ = station_pass_route1.append(station_pass_route2,sorted(['stopname','方位']))
station_pass_route_.to_csv(r'E:\桌面文件夹\路网普查数据\公交站点导出表.csv',encoding='utf-8-sig')
import webbrowser
webbrowser.open(r'E:\桌面文件夹\路网普查数据\公交站点导出表.csv')
# data_zt_=data_zt.groupby(['stopname','方位'],as_index=False)['routename'].count().reset_index(drop=True)





# todo 2.1 BRT （1）
pd.set_option('display.max_rows', 500)
center_brt_nums = len(data[(data.FID_area == 0) & (data['BRT站台'] == 1)].groupby(['stopname', '方位']))#.routename.count().sum()
center_brt_nums = len(data[(data.FID_area == 0) & (data['BRT站台'] == 1)].groupby(['stopname']))#.routename.count().sum()
print('中心城区 BRT（1）站点总数{}处'.format(center_brt_nums))
center_brt_nums1 = len(data[(data['BRT站台'] == 1)].groupby(['stopname', '方位']))#.routename.count().sum()
center_brt_nums1 = len(data[(data['BRT站台'] == 1)].groupby(['stopname']))#.routename.count().sum()
print('市区 BRT（1）站点总数{}处'.format(center_brt_nums1))
# todo 2.2 常规 （0，2）,3

center_cg_nums = len(data[(data.FID_area == 0)&((data['BRT站台']== 0)|(data['BRT站台']== 3))].groupby(['stopname', '方位']))#.routename.count().sum()
print('中心城区 常规（0，3）站点总数{}处'.format(center_cg_nums))
center_cg_nums1 = len(data[(data['BRT站台']== 0)|(data['BRT站台']== 3)].groupby(['stopname', '方位']))#.routename.count().sum()
print('市区 常规（0，3） 站点总数{}处'.format(center_cg_nums1))


# todo 1.站点总数（变）
all_nums1 = center_brt_nums1+center_cg_nums1

print('站点总数{}处'.format(all_nums1))
# todo 2.中心城区站点数  #  FID_area#.routename.count().sum()
center_nums = center_brt_nums+center_cg_nums
print('中心城区站点总数{}处'.format(center_nums))


# todo 2.3 途径线路最多的站点排名（前20名）,输出表格
data_center = data#todo 全部城区
data_center = data[data.FID_area == 0]#todo 中心城区
# station_pass_route = data_center.groupby('stopname').routename.unique()
za=data_center.groupby(['stopname','方位'],as_index=True)#[['lng_avg','lat_avg','routename']]#所有字段
station_pass_route = pd.DataFrame(za['routename'].unique().reset_index())
station_pass_route['pass_route_num'] = station_pass_route['routename'].apply(lambda x: len(x))
station_pass_route['lng_avg']=za['lng_avg'].head(1).reset_index()['lng_avg']
station_pass_route['lat_avg']=za['lat_avg'].head(1).reset_index()['lat_avg']
station_pass_route.to_csv(r'E:\桌面文件夹\路网普查数据\站点经纬度热力图用表(中心城区).csv', encoding='utf_8_sig', index=True)
station_pass_route.to_csv(r'E:\桌面文件夹\路网普查数据\站点经纬度热力图用表(市区).csv', encoding='utf_8_sig', index=True)

use_20_station = station_pass_route.sort_values(by='pass_route_num', ascending=False).head(20)
pd.DataFrame(use_20_station).to_csv(r'E:\桌面文件夹\路网普查数据\公交站点线路通过数量排名前20站点表（市区）.csv', encoding='utf_8_sig', index=True)
pd.DataFrame(use_20_station).to_csv(r'E:\桌面文件夹\路网普查数据\公交站点线路通过数量排名前20站点表（中心城）.csv', encoding='utf_8_sig', index=True)
# station_pass_route2 = data_center.groupby(['stopname','方位']).routename.unique()
# todo 2.4 根据途径线路数的多少形成热力图
df=station_pass_route
#  获取数据个数
num=df.shape[0]
#  获取纬度
lat=np.array(df["lat_avg"][0:num])
#  获取经度
lon=np.array(df["lng_avg"][0:num])
#  获取PM2.5，转化为numpy浮点型
pass_route_num=np.array(df["pass_route_num"][0:num],dtype = float)
#  将数据制作成[lats, lons, weights]的形式
data1=[[lat[i],lon[i],pass_route_num[i]] for i in range(num)]
#  绘制Map，中心经纬度[32, 120],开始缩放程度是5倍
map_osm=folium.Map(location=[36.500538,116.798706],zoom_start = 5)
#  将热力图添加到前面建立的map里
HeatMap(data1).add_to(map_osm)
file_path=r"E:\桌面文件夹\路网普查数据\公交站点热力图.html"
#  保存为html文件
map_osm.save(file_path)
#  默认浏览器打开
webbrowser.open(file_path)








#
data[data.lat_avg1 != data.lat_avg][['stopname', '方位', 'lat_avg1', 'lat_avg']]
