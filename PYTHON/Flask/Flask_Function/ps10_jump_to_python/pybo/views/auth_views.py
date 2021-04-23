from flask import Blueprint, url_for, render_template, flash, request, session, g #로그인폼할때 session, g 추가
from werkzeug.security import generate_password_hash, check_password_hash # 로그인폼할때 check_password_hash 추가
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

#계정 등록
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)
#로그인
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)
'''
 /login/ 이라는 라우트 URL에 매핑되는 login 함수를 생성.
 login함수도 signup함수와 마찬가지로 POST 요청인 경우에는 로그인을 수행하고 GET 요청인 경우에는 로그인을 할 수 있는 템플릿을 렌더링하도록 하였다.
 로그인 수행시 폼 입력으로 받은 username에 해당되는 사용자가 있는지를 조사하여 없을 경우 "존재하지 않는 사용자입니다." 라는 오류를 발생.
 데이터베이스에 저장된 비밀번호는 암호화된 비밀번호이므로 비밀번호 검증시에는 반드시 check_password_hash 함수를 사용해야 함. import 해야함.

 폼 검증과 사용자 및 비밀번호 체크가 이상없다면 플라스크 세션(session)에 user_id라는 키에 조회된 사용자의 id값을 저장.
 세션은 request와 마찬가지로 플라스크가 자동으로 생성하여 제공하는 변수.
 단, request는 요청과 응답이라는 한 사이클에만 의미있는 값이라면 세션은 플라스크 메모리에 저장되기 때문에 플라스크 서버가 구동중인 동안에는 영구적으로 사용할 수 있는 값.
 **세션은 영구적이지만 타임아웃이 설정되어 있어서 타임아웃 시간동안 접속이 없으면 세션정보가 삭제된다.
 이렇게 로그인 되었을때 session 변수에 User의 id값을 저장하면 브라우저 요청이 발생할 경우 이 세션값으로 사용자가 로그인한 사용자인지 아닌지를 판별할 수 있게 된다.
'''
#로그인을 하고 난 후에 "로그아웃" 링크가 보이고 로그아웃 상태에서 "로그인" 링크가 보이도록 수정.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
'''
@bp.before_app_request 어노테이션은 플라스크에서 제공하는 기능으로 이 어노테이션이 적용된 함수는 라우트 함수 실행전에 항상 먼저 실행.
따라서 load_logged_in_user 함수는 모든 라우트 함수 실행전에 반드시 먼저 실행될 것.
load_logged_in_user함수에서 사용된 g변수는 플라스크가 제공하는 컨텍스트 변수로 request변수와 마찬가지로 요청과 응답이라는 한 사이클에서만 유효한 컨텍스트 변수. 
load_logged_in_user함수는 session 변수에 user_id 값이 있는 경우 User데이터를 조회하여
g.user 변수에 조회된 User객체를 저장되어 있기 때문에 사용자이름이나 이메일등의 정보도 추가로 얻을수 있는 이점이 있다.
'''
#로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
'''
/logout/ 라우트 URL에 매핑되는 logout함수를 생성.
session.clear() 코드는 세션의 모든 값을 삭제. 따라서 session에 저장된 user_id도 삭제될 것.
그러면 앞서 작성한 load_logged_in_user함수에서 session의 user_id 값을 읽을 수 없으므로 g.user도 None이라는 값이 설정될 것이다.
'''