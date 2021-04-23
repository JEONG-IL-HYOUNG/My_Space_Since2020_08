from flask import Blueprint, url_for, render_template
from werkzeug.utils import redirect
from .auth_views import login_required

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_flask():
    return 'Hello, Flask!'

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/required/')
@login_required
def aaa():
    return '로그인했으니까 이 페이지가 보임 안했으면 로그인 페이지로 넘어감'

