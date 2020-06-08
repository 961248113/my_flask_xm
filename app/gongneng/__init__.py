from flask import Blueprint

gongneng = Blueprint('gongneng',__name__)#蓝图

import app.gongneng.forms
import app.gongneng.views