from . import gongneng
from flask import request,render_template,redirect,flash,url_for
from .forms import PublishForm
import pandas as pd
from app.model import *

@gongneng.route("/show_liuyanban", methods=['GET', 'POST'])
def search():  # 留言写入
    myEntryForm = PublishForm(request.form)
    l = getAllEntry()  # 取出数据库中全部留言+用户名的数据
    if request.method == 'POST':
        e = Entry(myEntryForm.content.data, myEntryForm.sender.data)  # 初始化
        e.add()  # 插入数据库
        return render_template('search.html', entris=l, form=myEntryForm)  # 传入前端展示
    return render_template('search.html', entris=l, form=myEntryForm)


@gongneng.route("/show_passengernum", methods=['GET', 'POST'])
def data_show1():  # 公交IC卡分析
    data = getICdata()
    minute = 60
    line_no = list(data.line_id.unique())
    # 1
    # data_101 = data[data.line_id.isin(line_no)].sort_values(by='TXNDATE').reset_index(drop=True)
    # 2
    data_101 = data.sort_values(by='TXNDATE').reset_index(drop=True)
    data_101['time_2_seconds'] = data_101.TXNDATE.apply(lambda x: x.time())
    data_101['time_2_seconds'] = data_101['time_2_seconds'].map(str).map(t2s)
    # 站点客流量排序
    station_num = data_101['STATION_NAME'].value_counts().sort_values(ascending=False)  # 大到小
    station_num_head10 = station_num.head(10)

    # 1个小时一划分客流量
    time_2_seconds_bins = [i * minute * 60 for i in range(int(24 / (minute / 60)) + 1)]
    labels = [i for i in range(1, int(24 / (minute / 60)) + 1)]
    Time_groups = pd.cut(data_101['time_2_seconds'], time_2_seconds_bins, labels=labels).rename('time_2_seconds_labels')
    passenger_num = Time_groups.value_counts().sort_index()

    from pyecharts import Bar, Scatter3D, EffectScatter, Overlap, Line, Pie
    from pyecharts import Page, configure
    configure(global_theme='shine')  # 更改主题
    page = Page()
    bar1 = Bar("乘客量top10的站点", "图一")
    bar1.add("乘客量top10的站点", station_num_head10.index, station_num_head10.values, xaxis_rotate=45, is_mor_utils=True)
    line1 = Line()
    line1.add("乘客量top10的站点(折线图)", station_num_head10.index, station_num_head10.values)
    overlap_1 = Overlap()
    overlap_1.add(bar1)
    overlap_1.add(line1)
    bar2 = Bar("全天一小时时段区间乘客登车数量", "图二")
    bar2.add("不同时段区间乘客数量", passenger_num.index, passenger_num.values, xaxis_rotate=90, is_mor_utils=True,
             mark_point=["min", "max"])
    # bar.print_echarts_options() # 该行只为了打印配置项，方便调试时使用
    page.add(overlap_1)
    page.add(bar2)
    page.render('app/templates/render/passenger_top10.html')  # 生成本地 HTML 文件

    return render_template('render/passenger_top10.html')


@gongneng.route("/show_station", methods=['GET', 'POST'])
def data_show2():  # 公交站点展示
    import pandas as pd
    import json
    import traceback
    file = open('app/templates/render/zhandian.json', 'w')  # 建立json数据文件
    data_1 = pd.read_excel("app/templates/render/zhandian.xlsx")  # 读取小区房价信息
    data_1 = data_1[['STATION_NAME', 'LNG', 'LAT', 'NOTE']]
    DATA_STR = []
    for i in data_1.values:
        try:
            c = 100
            lng = i[1]
            lat = i[2]
            str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + ',"count":' + str(c) + '},'
            tum = {"lat": str(lat), "lng": str(lng), "count": str(c)}
            # print(tum)
            file.write(str_temp)
            DATA_STR.append(tum)
        except:
            f = open("异常日志.txt", 'a')
            traceback.print_exc(file=f)
            f.flush()
            f.close()
    # DATA_STR = json.loads(DATA_STR)
    file.close()
    import json
    # json.parse(DATA_STR)
    # DATA_STR.to_json()
    return render_template('公交站点热力图.html', json_data=DATA_STR)


@gongneng.route("/show_point")
def data_showpoint():
    return render_template('point.html')





@gongneng.route("/show_chuxingguiji")
def data_show3():
    return render_template('出行轨迹.html')


@gongneng.route("/show_quyurenqunmidu", methods=['GET', 'POST'])
def data_show4():
    return render_template('区域人群密度监控.html')


@gongneng.route("/show_xuemaitu", methods=['GET', 'POST'])
def data_show5():
    return render_template('血脉图.html')


@gongneng.route("/show_qianxitu", methods=['GET', 'POST'])
def data_show6():
    return render_template('迁徙图.html')

@gongneng.route("/pic_tab")
def data_show7():
    return render_template('pic_tab.html')

@gongneng.route("/show_yuan_point")
def data_yuan_point():
    return render_template('yuan_point.html')

@gongneng.route("/show_line")
def data_showline():
    return render_template('line.html')


@gongneng.route("/show_yuan_area")
def data_yuan_area():
    return render_template('yuan_area.html')




@gongneng.route("/8")
def data_show8():
    return render_template('index_desi.html')

@gongneng.route('/pyvis_guanxi', methods=['GET', 'POST'])
def pyvis_guanxi():
    from pyvis.network import Network
    net = Network()
    # 添加单个节点
    net.add_node(1, label='node_1')
    net.add_node(2, label='node_2')
    # 添加属性,注意这⾥里里是添加多个节点，使⽤用add_nodes
    # 属性值传⼊入的是列列表，要保证列列表⻓长度与节点列列表⻓长度⼀一致
    net.add_nodes([3, 4, 5],
                  value=[10, 20, 30],
                  title=["节点3", "节点4", "节点5"],
                  x=[21.4, 54.2, 11.2],
                  y=[100.2, 23.54, 32.1],
                  label=["node_3", "node_4", "node_5"],
                  color=["#00ff1e", "#162347", "#dd4b39"])
    # ⼀一次添加⼀一条边
    net.add_edge(1, 2)
    net.add_edge(1, 3)
    net.add_edge(1, 4)
    net.add_edge(2, 5)
    # 有权重边
    net.add_edge(2, 1, wright=0.87)
    net.add_edge(2, 3, wright=0.5)
    '''
    #结合networkx使⽤用
    import networkx as nx
    # ⽣生成5个节点，每个点与其他所有点相互联系
    nxg = nx.complete_graph(5)
    G = Network()
    G.from_nx(nxg)
    # 输出并⽣生成demo2.html
    G.show('demo2.html')
    '''
    # 交互式显示，# 可对打开的html进⾏行行调整
    net.show_buttons(filter_=['physics'])
    net.save_graph('app/templates/render/pyvis_guanxi.html')    #输出并⽣生成pyvis_guanxi.html
    return render_template('render/pyvis_guanxi.html')
@gongneng.route('/pyshp', methods=['GET', 'POST'])
def pyshape_luwang():
    import shapely, geopandas, fiona
    import seaborn as sns
    from fiona.crs import from_epsg, from_string

    tpath = r'app/static/data/中心城区腾讯道路.shp'

    # 显示所有列
    pd.set_option('display.max_columns', 100)
    shp_df = geopandas.GeoDataFrame.from_file(tpath)
    shp_df.head()  # 获取表头
    shp_df.plot()
    import matplotlib.pyplot as plt
    plt.show()
    print(shp_df.head())

    #GeoPandas有两种主要的数据结构GeoSeries和GeoDataFrame.