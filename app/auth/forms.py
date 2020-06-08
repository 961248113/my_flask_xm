from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo

class LoginForm(FlaskForm):  # 定义表单
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
class RegistrationForm(FlaskForm):
    phone_num = StringField(label=u'电话号码',validators=[DataRequired()])

    email = StringField(label=u'邮箱地址',validators=[DataRequired(),
                        Length(1,64),Email()])
    username = StringField(label=u'用户名', validators=[DataRequired(),
                                                  Length(1, 64),
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须由字母、数字、下划线或 . 组成')])
    password =PasswordField(label=u'密码',validators=[DataRequired(),EqualTo('password2',message='密码必须一致')])
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
    submit = SubmitField(label=u'马上注册')