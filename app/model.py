# -*- coding: UTF-8 -*-
'''
该文件完成所有类的创建和插入数据库,数据库修改
'''
# from flask_mongoengine import MongoEngine  # mongodb orm
# import pymysql  # 直接连接mysql数据库
# import sqlite3 # sqlite3数据库
# import pymongo # mongodb数据库

import seaborn as sns
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei', font_scale=1.5)  # 解决Seaborn中文显示问题并调整字体大小
from app import db

# mysql数据库——实际应用
# 执行db.create_all()可以创建以下user和entry表格，seed
# 具体使用方法为python程序运行该model文件,然后执行db.create_all()语句即可，
# 数据库中可以见到相应的表和字段创建完成

class User(db.Model):  # db.Model可以提供增删改查的操作
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String, nullable=True)
    phone_num = db.Column(db.String, nullable=True)
    def __init__(self, username, password,email,phone_num):
        self.username = username
        self.password = password
        self.email = email
        self.phone_num = phone_num
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            # print(self.id)
            return self.id
        except Exception as e:
            db.session.rollback()
            return e
        finally:
            return 0

    def isExisted(self):  # 查询,判断用户名是否存在于数据库中
        temUser = User.query.filter_by(username=self.username, password=self.password).first()
        if temUser is None:
            return 0
        else:
            return 1

    def get_username(self):
        return self.username
    @staticmethod
    def seed():#预设角色数据
        db.session.add_all(map(lambda r: User(username=r), ['Guests', 'Administrators']))
        db.session.commit()


class Entry(db.Model):  # 留言的模型
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    sender = db.Column(db.String(32))

    def __init__(self, content, sender):
        self.content = content
        self.sender = sender

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            # print(self.id)
            return self.id
        except Exception as e:
            db.session.rollback()
            return e
        finally:
            return 0


def getAllEntry():  # 得到数据库所有的内容（留言板）
    Enlist = []
    Enlist = Entry.query.filter_by().all()
    return Enlist


def getICdata():
    import pymysql
    import pandas as pd
    conn = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='flasktest', port=3306, charset='utf8')
    data = pd.read_sql('select * from gps_ic_merge_bas_ic ', con=conn)
    conn.close()
    return data




def t2s(t):
    if t == None or t is '' or t is 0:
        return t
    else:
        h, m, s = t.strip().split(":")
        return int(h) * 3600 + 60 * int(m) + int(s)


def m2t(m):
    s = 0
    h, m = divmod(m, 60)
    return ("%02d:%02d:%02d" % (h, m, s))


# sqlite3数据库直接连接—基本操作
'''

def get_conn():
    return sqlite3.connect("test.db")
class User1(object):
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def save(self):
        sql="insert into user2 VALUES (?,?)"
        conn=get_conn()
        cursor=conn.cursor()
        cursor.execute(sql,(self.id,self.name))
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def query():
        sql="select * from user2"
        conn=get_conn()
        cursor=conn.cursor()
        rows=cursor.execute(sql)
        users=[]
        for row in rows:
            print(row)
            user=User1(row[0],row[1])
            users.append(user)
        conn.commit()
        cursor.close()
        conn.close()
        return users
    def __str__(self):#格式化输出
        return 'id:{}--name:{}'.format(self.id,self.name)
'''

# mysql数据库直接连接—基本操作
'''
import pymysql
def get_conn():
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='flasktest', charset='utf8')
    # 创建游标
    return conn
class User_mysql(object):
    def __init__(self,id,name):
        self.id=id
        self.name=name
    def save(self):
        sql="insert into user_mysql (id,name) VALUES (%s,%s)"
        conn=get_conn()
        cursor=conn.cursor()
        cursor.execute(sql,(self.id,self.name))
        conn.commit()
        cursor.close()
        conn.close()
    @staticmethod
    def query():
        sql="select * from user_mysql"
        conn=get_conn()
        cursor=conn.cursor()
        rows=cursor.execute(sql)
        print(rows)
        users=[]
        for row in rows:
            print(row)
            user=User_mysql(row[0],row[1])
            users.append(user)
        conn.commit()
        cursor.close()
        conn.close()
        return users
    def __str__(self):#格式化输出
        return 'id:{}--name:{}'.format(self.id,self.name)
'''

# mongoDB数据库直接连接—基本操作
'''
import pymongo
def get_conn():
    # 创建连接
    client=pymongo.MongoClient('127.0.0.1',27017)
    db =client.test
    user=db.user_colletion
    return user
class User_mongodb(object):
    def __init__(self,id2,name):
        self.id2=id2
        self.name=name
    def save(self):
        conn=get_conn()
        user={"id2":self.id2,"name":self.name}
        id=conn.insert(user)
        #id=conn.remove(user) 
        print(id)

    @staticmethod
    def query():
        users=get_conn().find()
        return users
'''

# mongodb的orm框架 MongoEngine—基本操作
'''
#mongodb orm 配置 MongoEngine
app.config['MONGODB_SETTINGS'] = {'db': 'test','host': 'mongodb://localhost/test'}
db=MongoEngine(app)  #数据库实例化#mongodb orm 数据库应用
class User(db.Document):  # db.Model可以提供增删改查的操作
    user = db.StringField()
    passw = db.StringField()
    def __str__(self):#格式化输出
        return 'username:{}--password:{}'.format(self.user,self.passw)
'''
