from app import * #create_app,db
app=create_app()
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
from flask_migrate import Migrate,MigrateCommand,upgrade#数据库修改迁移的插件
from flask_script import Manager # flask_script一般用在开发环境，增加外部扩展包

migrate = Migrate(app,db)#db数据库连接的为mysql 数据库连接方式为orm框架
# 利用脚本语言
# 初始化建立仓库 python migrate.py（manage.py） db init，生成文件夹migrations
# 当添加字段后运行 python migrate.py db migrate，显示修改的字段具体为什么
# 然后运行 python migrate.py db upgrade执行更新数据库操作
manager = Manager(app)
manager.add_command('db',MigrateCommand)

###########################
# @manager.command
# def save():
#     '''
#     #monogoDB orm 样例学习
#     user=User(user='mujin',passw='123')
#     user.save()
#     #monogoDB  直连 样例学习
#     user=User_mongodb('10','mujinjie')
#     user.save()
#     # mysql_orm 样例学习
#     user = User_mysql('1', 'jike1')
#     db.session.add(user)
#     db.session.commit()
#     '''
#     # mysql_orm 实际应用
#     user = User(username='m4', password='m4')
#     db.session.add(user)
#     db.session.commit()
# @manager.command
# def query_all():
#     '''
#     #monogoDB orm
#     users=User.objects.all()
#     for u in users:
#         print(u)
#     #monogoDB 直连
#     users=User_mongodb.query()
#     for user in users:
#         print(user)
#     # mysql_orm
#     users = User_mysql.query.all()
#     for u in users:
#         print('没完了',u)
#     '''
#     # mysql_orm 实际应用
#     users = User.query.all()
#     for u in users:
#         print(u)
######################

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

@manager.command
def dev():
    from livereload import Server# 写代码实时刷新
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')  # 监测整个项目下所有文件
    # 监测static中所有的文件  live_server.watch('static/*.*')
    live_server.serve(open_url_delay=True)
    # live_server.serve(open_url=True)
@manager.command
def test():
    pass
@manager.command
def deploy():#第一次安装程序时需要部署数据库,更新数据库
    from app.model import User
    upgrade()#除了在命令行调用，也可以在方法中调用
    User.seed()#调用静态方法，布置账户
if __name__ == '__main__':
    manager.run()