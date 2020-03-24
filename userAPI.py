# restful API开发
from flask_restful import  Resource, reqparse #Resource资源代表浏览器链接
from model import User
from Jsonobject import *
auth=reqparse.RequestParser()# 为解析器
class Authentication(Resource):
    def get(self):
        pass
    def post(self):
        #提交用户名密码
        auth.add_argument("username",required=True,help="username is required")
        auth.add_argument("password",required=True,help="password is required")
        args=auth.parse_args()
        username=args['username']
        password=args['password']
        u=User(username,password)
        jsobj = JsonObject()
        if u.isExisted():
            jsobj.put("code",1)
            jsobj.put("desc","user Existed")
        else:
            jsobj.put("code",2)
            jsobj.put("desc","user not Existed")
        return jsobj.getJson(),200