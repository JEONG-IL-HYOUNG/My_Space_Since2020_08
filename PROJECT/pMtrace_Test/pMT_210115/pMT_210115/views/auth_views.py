from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db
from forms import UserCreateForm, UserLoginForm
from models import gb_account, gb_works
import functools
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

#계정 등록
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = gb_account.query.filter_by(user_nm=form.user_nm.data).first()
        if not user:
            user = gb_account(user_nm=form.user_nm.data,
                              pw=generate_password_hash(form.pw1.data),
                              cdate= datetime.now())
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


#로그인 UI-100 원래 하던것
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = gb_account.query.filter_by(user_nm=form.user_nm.data).first()
        #prj = gb_works.query.order_by().first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.pw, form.pw.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            # session['user_id'] = user.userid
            user_session = {
                'user_id': user.userid,
                'user_nm': user.user_nm
                #'prj_nm' : prj.smov_id
            }
            session['user_session'] = user_session
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

# @bp.route('/login/', methods=('GET', 'POST'))
# def login():
#     if request.method == 'POST':
#         error = None
#         user_nm = request.form['user_nm']
#         user = gb_account.query.filter_by(user_nm= user_nm).first()
#                  #prj = gb_works.query.order_by().first()
#         if not user:
#             error = "존재하지 않는 사용자입니다."
#         elif not check_password_hash(user.pw):
#             error = "비밀번호가 올바르지 않습니다."
#         if error is None:
#             session.clear()
#         #             # session['user_id'] = user.userid
#             user_session = {
#                     'user_id': user.userid,
#                     'user_nm': user.user_nm
#                          #'prj_nm' : prj.smov_id
#                      }
#             session['user_session'] = user_session
#             return redirect(url_for('main.index'))
#         flash(error)
#     render_template('auth/login.html')



@bp.before_app_request
def load_logged_in_user():
    user_session = session.get('user_session')
    if user_session is None:
        g.user = None
    else:
        g.user = gb_account.query.get(user_session['user_id'])

#로그아웃
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

