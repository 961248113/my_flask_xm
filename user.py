'''
#蓝图 blueprint
使用Flask中的蓝图，将用户模块和文章模块分离。不同的url加以区分，比如
www.*.cn/user/1访问1号用户信息
www.*.cn/article/1访问1号文章的信息
防止以后路由多了后，难以分辨属于的模块
'''
#此处定义有关用户的路由，然后再main.py注册该路由，并将url访问路径的前缀进行定义
from flask import Blueprint
from app.model import User
# 此处定义有关用户的路由，然后再main.py注册该路由，并将url访问路径的前缀进行定义
from flask import Blueprint

from app.model import User

user=Blueprint('user',__name__)
@user.route('/<int:user_id>')
def showUser(user_id):
    u=User.query.filter_by(id=user_id).first()
    return u.get_username()
