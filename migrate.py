#数据库迁移、修改
from model import db
from model import app
from flask_migrate import Migrate,MigrateCommand#数据库修改迁移的插件
from flask_script import Manager # flask_script一般用在开发环境，增加外部扩展包

migrate = Migrate(app,db)#db数据库连接的为mysql 数据库连接方式为orm框架
manager = Manager(app)
manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()
    #利用脚本语言
    # 初始化建立仓库 python migrate.py db init，生成文件夹migrations
    #当添加字段后运行 python migrate.py db migrate，显示修改的字段具体为什么
    #然后运行 python migrate.py db upgrade执行更新数据库操作