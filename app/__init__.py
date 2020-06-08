
# from model import app
# from app.main import main as main_blueprint
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_sqlalchemy import SQLAlchemy  # mysql orm     # mysql的orm框架 SQLAlchemy  # SQLAlchemy对象关系映射 mysql orm配置

from flask_nav.elements import *
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for, flash, abort
# from os import path
# basedir = path.abspath(path.dirname(__file__))
db = SQLAlchemy()  # 数据库实例化#mysql orm 数据库应用
bootstrap = Bootstrap()  # 实例化Bootstrap
nav=Nav()#项目栏、侧边栏

def create_app():
    app = Flask(__name__)
    app.debug = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'sqlite:///' + path.join(basedir, 'data.sqlite')
    # mysql+pymysql会报警告，为了防止报警告，最好用mysql+mysqlconnector
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flasktest?charset=utf8"  # 设定数据库目录
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:root@localhost:3306/flasktest?charset=utf8"  # 设定数据库目录
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
    # app.secret_key = 'qi_fei_de_mumu_123'  # 防止跨站攻击
    app.config.from_pyfile('config')  # 防止跨站攻击
    # db = SQLAlchemy(app)  # 数据库实例化#mysql orm 数据库应用
    # bootstrap = Bootstrap(app)  # 实例化Bootstrap
    # nav=Nav()
    nav.register_element('top', Navbar(u'Flask项目',
                                       View(u'主页', 'auth.login'),
                                       View(u'关于', 'gongneng.search'),
                                       View(u'上传', 'auth.upload'),
                                       Subgroup(u'项目',
                                                View(u'公交站点乘客分析', 'gongneng.data_show1'),
                                                Separator(),
                                                View(u'站点热力图', 'gongneng.data_show2'),
                                                Separator(),
                                                View(u'出行轨迹', 'gongneng.data_show3'),
                                                Separator(),
                                                View(u'区域人群密度', 'gongneng.data_show4'),
                                                Separator(),
                                                View(u'血脉图', 'gongneng.data_show5'),
                                                Separator(),
                                                View(u'迁徙图', 'gongneng.data_show6'),
                                                Separator(),
                                                View(u'Echarts示例', 'gongneng.data_show7'),
                                                Separator(),
                                                Separator(),
                                                View(u'点', 'gongneng.data_yuan_point'),
                                                Separator(),
                                                Separator(),
                                                View(u'线', 'gongneng.data_showline'),
                                                Separator(),
                                                Separator(),
                                                View(u'圆域', 'gongneng.data_yuan_area'),
                                                Separator(),
                                                View(u'设计首页（设计中）', 'gongneng.data_show8'),
                                                Separator(),
                                                View(u'pyvis关系图', 'gongneng.pyvis_guanxi'),
                                                Separator(),
                                                ),
                                       ))
    db.init_app(app)  # 数据库实例化#mysql orm 数据库应用
    bootstrap.init_app(app)  # 实例化Bootstrap
    nav.init_app(app)

    #注册蓝图
    from app.auth import auth
    from app.gongneng import gongneng
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(auth)  # , url_prefix='/auth'
    # app.register_blueprint(main_blueprint, static_folder='static')
    app.register_blueprint(gongneng)  # , url_prefix='/auth'
    return app


