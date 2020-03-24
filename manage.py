from model import app
from flask_script import Manager # flask_script一般用在开发环境，增加外部扩展包
from model import User # 实际应用mysql数据库的操作
#from model import User1 # sqlite 数据库
#import sqlite3 # sqlite 数据库
from model import db # mysql orm 应用

#from model import User_mysql,get_conn # mysql 数据库
#from model import User_mongodb # mongodb 数据库
#from model import User_mysql # mysql orm 数据库
#from model import User # mongodb orm 数据库
manager=Manager(app)

@manager.command
def save():
    '''
    #monogoDB orm 样例学习
    user=User(user='mujin',passw='123')
    user.save()
    #monogoDB  直连 样例学习
    user=User_mongodb('10','mujinjie')
    user.save()
    # mysql_orm 样例学习
    user = User_mysql('1', 'jike1')
    db.session.add(user)
    db.session.commit()
    '''
    # mysql_orm 实际应用
    user = User(username='m4', password='m4')
    db.session.add(user)
    db.session.commit()
@manager.command
def query_all():
    '''
    #monogoDB orm
    users=User.objects.all()
    for u in users:
        print(u)
    #monogoDB 直连
    users=User_mongodb.query()
    for user in users:
        print(user)
    # mysql_orm
    users = User_mysql.query.all()
    for u in users:
        print('没完了',u)
    '''
    # mysql_orm 实际应用
    users = User.query.all()
    for u in users:
        print(u)


# @manager.command
# def init_sqlite():#sqlite 样例学习
#     sql='create table user2 (id INT,name TEXT)'
#     conn=sqlite3.connect("test.db")
#     cursor=conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     cursor.close()
#     conn.close()
# @manager.command
# def init_mysql():#sqlite
#     sql='create table user_mysql2 (id int(32),name varchar(32))'
#     conn=get_conn()
#     cursor=conn.cursor()
#     cursor.execute(sql)
#     conn.commit()
#     cursor.close()
#     conn.close()
# @manager.command
# def save():
#     '''
#     #sqlite3 直连
#     user=User1(2,'jike2')
#     user.save()
#     '''
#     #mysql 直连
#     user=User_mysql('1','jike1')
#     user.save()
#     # print('mumumumumu~~~~~')
# @manager.command
# def query_all():
#     '''
#     # sqlite3 直连
#     users=User1.query()
#     '''
#     # mysql 直连
#     users = User_mysql.query()
#     for user in users:
#         print(user)
#     # print('mumumu2')

if __name__ == '__main__':
    manager.run()