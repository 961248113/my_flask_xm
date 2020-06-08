from flask_wtf import FlaskForm
from wtforms import  StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,Regexp,EqualTo

class PublishForm(FlaskForm):
    content = StringField('content', [DataRequired()])
    sender = StringField('sender', [DataRequired()])