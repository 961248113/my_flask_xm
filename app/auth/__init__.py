from flask import Blueprint

auth = Blueprint('auth',__name__)#蓝图

import app.auth.forms
import app.auth.views
# from . import forms
