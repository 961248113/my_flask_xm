from flask import Flask, render_template, request, redirect, url_for, flash, abort
# from db import *#与db.py文件相对应
from model import *#包含app
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, PasswordField, validators, StringField, SubmitField

from wtforms.validators import DataRequired
import time
from os import path
from werkzeug.utils import secure_filename

# app = Flask(__name__)
class LoginForm(Form):#定义表单
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])


class PublishForm(Form):
    content = StringField('content', [DataRequired()])
    sender = StringField('sender', [DataRequired()])


from user import *
app.register_blueprint(user,url_prefix='/user')#固定url格式


@app.route('/', methods=['GET', 'POST'])
def login():
    myForm = LoginForm(request.form)
    if request.method == "POST":
        # print(myForm.username,myForm.password)
        u = User(myForm.username.data, myForm.password.data)
        if (u.isExisted()):
            return redirect(url_for('search'))
        else:
            message = '用户名不存在或者密码错误'
            return render_template('login.html', message=message, form=myForm)
    return render_template('login.html', form=myForm)


@app.route('/register', methods=['GET', 'POST'])
def register():
    myForm = LoginForm(request.form)
    if request.method == 'POST':
        mark = request.form["mark"]
        if mark == 'mumu123':
            # addUser(myForm.username.data,myForm.password.data)
            u = User(myForm.username.data, myForm.password.data)
            u.add()
            # time.sleep(1)
            return redirect(url_for('login'))
        else:
            # flash('邀请码为必填项')
            message = '邀请码为必填项'
            return render_template('register.html', form=myForm, message=message)
    return render_template('register.html', form=myForm)


@app.route('/erweima', methods=['GET', 'POST'])
def erweima():
    return render_template('wechat_2.html')

@app.route('/upload', methods=['GET', 'POST'])  # 末尾加/
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


@app.route("/show_data", methods=['GET', 'POST'])
def search():  # 留言写入
    myEntryForm = PublishForm(request.form)
    l = getAllEntry()  # 取出数据库中全部留言+用户名的数据
    if request.method == 'POST':
        e = Entry(myEntryForm.content.data, myEntryForm.sender.data)  # 初始化
        e.add()  # 插入数据库
        return render_template('search.html', entris=l, form=myEntryForm)  # 传入前端展示
    return render_template('search.html', entris=l, form=myEntryForm)


@app.route("/show_passengernum", methods=['GET', 'POST'])
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
    page.render('templates/render/passenger_top10.html')  # 生成本地 HTML 文件

    return render_template('render/passenger_top10.html')


@app.route("/show_station", methods=['GET', 'POST'])
def data_show2():  # 公交站点展示
    import pandas as pd
    import json
    import traceback
    file = open('templates/render/zhandian.json', 'w')  # 建立json数据文件
    data_1 = pd.read_excel("templates/render/zhandian.xlsx")  # 读取小区房价信息
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


@app.route("/show_point")
def data_showpoint():
    return render_template('point.html')


@app.route("/show_line")
def data_showline():
    return render_template('line.html')


@app.route("/show_yuan_area")
def data_yuan_area():
    return render_template('yuan_area.html')


@app.route("/show_yuan_point")
def data_yuan_point():
    return render_template('yuan_point.html')


@app.route("/show_chuxingguiji")
def data_show3():
    return render_template('出行轨迹2.html')

@app.route("/pic_tab")
def data_show7():
    return render_template('pic_tab.html')

@app.route("/8")
def data_show8():
    return render_template('index_desi.html')


@app.route("/show_quyurenqunmidu", methods=['GET', 'POST'])
def data_show4():
    return render_template('区域人群密度监控.html')


@app.route("/show_xuemaitu", methods=['GET', 'POST'])
def data_show5():
    return render_template('血脉图.html')


@app.route("/show_qianxitu", methods=['GET', 'POST'])
def data_show6():
    return render_template('迁徙图.html')

from flask_restful import Api
api=Api(app)
from userAPI import *#Authentication
api.add_resource(Authentication,'/auth')#需要用浏览器插件 Advanced-REST-client_v3.1.9 来获得返回值

if __name__ == '__main__':
    app.run(debug=True)#host='0.0.0.0',
    # manager.run()#利用脚本语言python main.py runserver执行项目
