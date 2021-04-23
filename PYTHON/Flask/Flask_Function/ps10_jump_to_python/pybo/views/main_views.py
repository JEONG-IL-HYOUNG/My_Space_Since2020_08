from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')
#Blueprint는 이름, 모듈명, URL 프리픽스 값을 입력으로 객체를 생성한다.
# 여기서 사용된 'main' 이라는 이름은 나중에 함수명으로 URL을 찾아내는 url_for 함수에서 사용된다.
# URL 프리픽스(url_prefix)는 main_views.py 파일에 있는 함수들의 URL 앞에 항상 붙게 되는 프리픽스 URL을 의미
# url_prefix='/' 대신 url_prefix='/main' 이라고 선언했다면 hello_pybo 함수를 호출하기 위해서는 http://localhost:5000/ 대신 http://localhost:5000/main/ 이라고 호출


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    return redirect(url_for('question._list'))