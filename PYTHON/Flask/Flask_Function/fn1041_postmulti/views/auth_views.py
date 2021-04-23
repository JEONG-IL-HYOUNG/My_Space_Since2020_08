from flask import Blueprint, url_for, render_template, flash, request, session, g #로그인폼할때 session, g 추가
from werkzeug.security import generate_password_hash, check_password_hash # 로그인폼할때 check_password_hash 추가
from werkzeug.utils import redirect

from app import db
from forms import UserCreateForm, UserLoginForm
from models import User
import functools



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


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_id

#로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


'''#login_required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

'''
'''
login_required라는 데코레이터 함수를 생성하였다.
이제 다른 함수에서 @login_required 라는 어노테이션을 지정하면 login_required라는 데코레이터 함수가 먼저 실행될 것.
login_required함수는 g.user가 있는지를 조사하여 없으면 로그인 URL로 리다이렉트 시키고 g.user가 있을 경우에는 원래 함수를 그대로 실행.
'''
#여기까지 처리하고 main_views.py로 가서
##test.html(기본템플릿)에 로그인 리콰이어 함수 적용
