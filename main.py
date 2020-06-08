from flask import Flask, render_template, request, redirect, url_for, flash, abort
# from db import *#与db.py文件相对应
from app.model import *  # 包含app,nav
from app import *
import time
from os import path
from werkzeug.utils import secure_filename

# app = Flask(__name__)


app=create_app()

from user import *

# app.register_blueprint(user, url_prefix='/user')  # 固定url格式,与user.py userAPI结合使用

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# from flask_restful import Api
#
# api = Api(app)
# from userAPI import *  # Authentication
# api.add_resource(Authentication, '/auth')  # 需要用浏览器插件 Advanced-REST-client_v3.1.9 来获得返回值

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)  # debug=True,host='0.0.0.0',
    # manager.run()#利用脚本语言python main.py runserver执行项目
