from . import auth
from .forms import *
from flask import request,render_template,redirect,flash,url_for
from app.model import User

import time
from werkzeug.utils import secure_filename


@auth.route('/', methods=['GET', 'POST'])
def login():
    myForm = LoginForm(request.form)
    if request.method == "POST":
        # print(myForm.username,myForm.password)
        u = User(myForm.username.data, myForm.password.data,'1','2')
        if (u.isExisted()):
            # return redirect(url_for('search'))
            title = 'flask主页'
            return render_template('new_index.html', title_name=title)
        else:
            message = '用户名不存在或者密码错误'
            return render_template('login.html', message=message, form=myForm)
    return render_template('login.html', form=myForm)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    from app import db
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    phone_num=form.phone_num.data)
        u = User(form.username.data, form.password.data,form.email.data, form.phone_num.data)
        if (u.isExisted()):
            message='用户名已存在'
            return render_template('register.html',message=message,
                                   form=form)
        else:

            # from twilio.rest import Client
            # # Your Account Sid and Auth Token from twilio.com/console
            # account_sid = 'AC379c4955bd0f3e0f9f52ec086dcb7c1c'
            # auth_token = '79ff623bc3b52af312c0562cad571c66'
            # # auth_token = '8240d2517918932a997b8bb195911234'
            # client = Client(account_sid, auth_token)
            # message = client.messages.create(
            #     from_='+12482152894',
            #     body=str(form.username.data)+'用户名已由%s注册'%form.phone_num.data,
            #     to='+8615966652606'
            #     # to='+8618866812508'
            # )
            # print(message.sid)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))#重定向登陆页面
    return render_template('register.html',
                           form=form)
    # myForm = LoginForm(request.form)
    # if request.method == 'POST':
    #     mark = request.form["mark"]
    #     if mark == 'mu15966652606':
    #         # addUser(myForm.username.data,myForm.password.data)
    #         u = User(myForm.username.data, myForm.password.data)
    #         u.add()
    #         flash('注册成功，请登录')
    #         time.sleep(2)
    #         return redirect(url_for('auth.login'))
    #     else:
    #         message = '邀请码输入错误'
    #         return render_template('register.html', form=myForm, message=message)
    # return render_template('register.html', form=myForm)


@auth.route('/erweima_wx', methods=['GET', 'POST'])
def erweima_wx():
    return render_template('wechat_2.html')


@auth.route('/erweima_qq', methods=['GET', 'POST'])
def erweima_qq():
    return render_template('qq_2.html')


@auth.route('/upload', methods=['GET', 'POST'])  # 末尾加/
def upload():
    from os import path
    if request.method == 'POST':
        f = request.files['file']
        basepath = path.abspath(path.dirname(__file__))
        upload_path = path.join(basepath, 'static/uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('auth.upload'))
    return render_template('upload.html')
