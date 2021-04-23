from flask import Blueprint, url_for, render_template, request, flash, session,g
from werkzeug.utils import redirect, secure_filename
import os
from models import gb_account, gb_works, gb_mov_sim ,search_histroy
from forms import post_db_test
from app import db
from .auth_views import login_required, load_logged_in_user
import functools
from datetime import datetime

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

#index page에서 검색버튼 눌렀을때
#페이지 넘어가지 않고 index 페이지에서 동영상 출력

#UI-100
@bp.route('/search/', methods=('GET', 'POST'))
def search_main():
    if request.method == 'POST':
        input_yurl = request.form['video_url']
        yid =  input_yurl[-11:]
        search = search_histroy.query.filter_by(seq = input_yurl).first()
        if not search:
                user_session = session.get('user_session')
                if user_session is None:
                    search = search_histroy(seq = input_yurl,
                                            date= datetime.now())
                else:
                    search = search_histroy(seq = input_yurl,
                                            user_nm = session.get('user_session')['user_nm'],
                                            date= datetime.now())
                db.session.add(search)
                db.session.commit()
                return render_template('index.html',aaa=yid)
        else:
            return 'DB에 저장되어 있는 URL입력하면..이페이지가 뜸'
    else:
        return redirect(url_for('main.index'))

#UI-200
#분석목록
@bp.route('/my_analy_list/', methods=('GET', 'POST'))
@login_required
def my_analy_list():
    return render_template('analysis/my_analy_list.html')


#UI-300
#분석목록 - > 프로젝트명 클릭했을때
@bp.route('/my_detail_list/', methods=('GET', 'POST'))
@login_required
def my_detail_list():
    return render_template('analysis/my_detail_list.html')

#UI-400
@bp.route('/new_work/', methods=('GET', 'POST'))
@login_required
def new_work():
    return render_template('analysis/new_work.html')





# 메인페이지- input 로그인 했을경우에....
# #분석 버튼을 누르면 db에 저장이되고 페이지 넘어간다
# @bp.route('/analysis/', methods=('GET', 'POST'))
# @login_required
# def analysis():
#     form = post_db_test()
#     if request.method == 'POST':
#         input_yurl = request.form['video_url']
#         #input_keyword = request.form['keyword']
#         #여기부분 수정중
#         prj_nm = gb_works.query.filter_by(prj_nm=form.prj_nm.data).first()
#         if not prj_nm:
#             prj_nm = gb_works(prj_nm = input_yurl,
#                                   user_nm = session.get('user_session')['user_nm'],
#                                  status = 1,
#                                  smov_id= input_yurl)
#             '''
#             prj_nm = gb_mov_sim_anal(smov_id=input_yurl,
#                                      rmov_id = 'efg')
#             '''
#             db.session.add(prj_nm)
#             db.session.commit()
#             return render_template('analysis/analysis.html',
#                                    vvvvv = input_yurl)
#                                    #aaaaa = input_keyword)
#         else:
#             return '뭔가 잘못됐다.'
#     else:
#         return render_template('analysis/analysis.html')
#
# #비 로그인 상태에서 input
# @bp.route('/analysis_nlogin/', methods=('GET', 'POST'))
# def analysis_nn():
#     if request.method == 'POST':
#         input_yurl = request.form['video_url']
#         input_keyword = request.form['keyword']
#         return render_template('analysis/nlogin.html',
#                                vvvvv=input_yurl,
#                                aaaaa=input_keyword)
#
# #gb_test용 url 수집해서 넣기
# @bp.route('/gb_test/', methods=('GET', 'POST'))
# def gb_tt():
#     form = post_db_test()
#     if request.method == 'POST':
#         input_yurl = request.form['test_test']
#         test_url = gb_test.query.filter_by(test_url=form.test_url.data).first()
#         if not test_url:
#             test_url = gb_test(test_url=input_yurl)
#             db.session.add(test_url)
#             db.session.commit()
#             return render_template('analysis/test.html',
#                                    vvvvv=input_yurl)
#         else:
#             return '뭔가 잘못됐다.'
#     else:
#         return render_template('analysis/test.html')
#
##네비바에서 분석목록
#UI-200
# @bp.route('/my_analy_list/', methods=('GET', 'POST'))
# def my_analy_list():
#     #페이지 위쪽 기본적으로 분석중, 분석완료
#     #my_analy_list = gb_projects.query.order_by(gb_projects.user_nm) # 정렬하는 부분인데 별로 필요없을듯..
#     my_analy_list1 = gb_works.query.filter(gb_works.user_nm == session.get('user_session')['user_nm'])
#     status_ing = gb_works.query.filter(gb_works.status == 0)
#     status_end = gb_works.query.filter(gb_works.status == 1)
#
#     #페이지 아래쪽 상세정보 보기
#
#     smov = gb_mov_sim.query.order_by(gb_mov_sim.smov_id).all()
#
#     return render_template('analysis/my_analy_list.html',
#                            my_analy_list = my_analy_list,
#                            my_analy_list1 = my_analy_list1,
#                            status_ing = status_ing,
#                            status_end = status_end,
#                            smov= smov)
#                            #status = status)

#
# #파일 업로드
# @bp.route('/fileupload/', methods=('GET', 'POST'))
# def upload_files():
#     if request.method == 'POST':
#         UPLOAD_DIR = "D:/test"
#         f = request.files['file']
#         fname = secure_filename(f.filename)
#         path = os.path.join(UPLOAD_DIR, fname)
#         f.save(path)
#         return 'File upload complete (%s)' % path