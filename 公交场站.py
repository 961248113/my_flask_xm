from pyecharts import Pie
import webbrowser
import pandas as pd

pd.set_option('display.max_columns', None)

data = pd.read_excel(r'E:\桌面文件夹\路网普查数据\公交场站.xls')
area = round(data['土地使用面'].sum() / (10 ** 4),2)
print('土地使用面积为{}公顷'.format(area))
data1=round(data.groupby('用地属性')['土地使用面'].sum()/ (10 ** 4),2).reset_index()
attr = data1['用地属性']
v1 = data1['土地使用面']

pie = Pie("")  # , title_pos='center'
pie.add(
    "",
    attr,
    v1,
    is_label_show=True,
    is_more_utils=True
)
pie.render(path=r"E:\桌面文件夹\路网普查数据\公交场站面积饼状图.html")
webbrowser.open(r"E:\桌面文件夹\路网普查数据\公交场站面积饼状图.html")
