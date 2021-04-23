from flask import Blueprint, url_for, render_template, request, flash, session,g
from werkzeug.utils import redirect, secure_filename
import os
from models import gb_account, gb_projects, gb_mov_sim_anal
from forms import post_db_test

from app import db
from .auth_views import login_required, load_logged_in_user
import functools

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

#메인페이지- input
#분석 버튼을 누르면 db에 저장이되고 페이지 넘어간다
@bp.route('/analysis/', methods=('GET', 'POST'))
@login_required
def analysis():
    form = post_db_test()
    if request.method == 'POST':
        input_yurl = request.form['video_url']
        input_keyword = request.form['keyword']
        #여기부분 수정중
        prj_nm = gb_projects.query.filter_by(prj_nm=form.prj_nm.data).first()
        if not prj_nm:
            prj_nm = gb_projects(prj_nm = input_yurl,
                                  user_nm = session.get('user_session')['user_nm'],
                                 status = 0,
                                 smov_id= input_yurl)
            '''
            prj_nm = gb_mov_sim_anal(smov_id=input_yurl,
                                     rmov_id = 'efg')
            '''
            db.session.add(prj_nm)
            db.session.commit()
            return render_template('analysis/analysis.html',
                                   vvvvv = input_yurl,
                                   aaaaa = input_keyword)
        else:
            return '뭔가 잘못됐다.'
    else:
        return '포스트로 안넘어왔음'

#네비바에서 분석목록
@bp.route('/my_analy_list/', methods=('GET', 'POST'))
def my_analy_list():
    #페이지 위쪽 기본적으로 분석중, 분석완료
    my_analy_list = gb_projects.query.order_by(gb_projects.user_nm) # 정렬하는 부분인데 별로 필요없을듯..
    my_analy_list1 = gb_projects.query.filter(gb_projects.user_nm == session.get('user_session')['user_nm'])
    status_ing = gb_projects.query.filter(gb_projects.status == 0)
    status_end = gb_projects.query.filter(gb_projects.status == 1)

    #페이지 아래쪽 상세정보 보기

    smov = gb_mov_sim_anal.query.filter(gb_mov_sim_anal.match_id).all()
    rmov = gb_mov_sim_anal.query.filter(gb_mov_sim_anal.rmov_id).all()

    return render_template('analysis/my_analy_list.html',
                           my_analy_list = my_analy_list,
                           my_analy_list1 = my_analy_list1,
                           status_ing = status_ing,
                           status_end = status_end,
                           smov= smov,
                           rmov= rmov)
                           #status = status)


#파일 업로드
@bp.route('/fileupload/', methods=('GET', 'POST'))
def upload_files():
    if request.method == 'POST':
        UPLOAD_DIR = "D:/test"
        f = request.files['file']
        fname = secure_filename(f.filename)
        path = os.path.join(UPLOAD_DIR, fname)
        f.save(path)
        return 'File upload complete (%s)' % path