from flask import Blueprint, url_for, render_template, request, flash, session,g
from werkzeug.utils import redirect, secure_filename
import os
from models import gb_account, gb_works, gb_mov,gb_mov_sim, search_history
from forms import post_db_test
from app import db
from .auth_views import login_required, load_logged_in_user
import functools
from datetime import datetime

# 크롤링할때 import
import os
import shutil
from urllib.request import urlopen
import urllib.request
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date
import sys

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib


bp = Blueprint('analysis', __name__, url_prefix='/analysis')

#index page에서 검색버튼 눌렀을때
#페이지 넘어가지 않고 index 페이지에서 동영상 출력


#UI-100
@bp.route('/search/', methods=('GET', 'POST'))
def search_main():
    form = post_db_test()
    dt = datetime.now()
    if request.method == 'POST':
        input_yurl = request.form['video_url']
        yid =  input_yurl[-11:]
        search = search_history.query.filter_by(seq = yid).all()
        ##############
        html = urllib.request.urlopen(input_yurl).read()
        soup = BeautifulSoup(html, 'html.parser')
        # 조회수 크롤링
        pattern_viewcount = 'viewCount":"(.*?)"'
        result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_viewcount) >= 1:
            result_youtube_viewcount = result_viewcount[0]
            print(result_youtube_viewcount)
        else:
            result_youtube_viewcount = -1
         #타이틀 크롤링
        pattern_title = '<title>(.*?)</title>'
        result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_title) >= 1:
            result_youtube_title = result_title[0][:-10]
            print(result_youtube_title)
        else:
            result_youtube_title = -1
            print(result_youtube_title)
        # 유튜브 tag(keyword) 크롤링
        pattern_tag = 'keywords\\":\[.*?\]'
        tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
        result_tag = [y[11:-1] for y in tag]
        if len(result_tag) >= 1:
            result_youtube_tag = result_tag[0]
            print(result_youtube_tag)
        else:
            result_youtube_tag = -1
        # 유튜브 id 크롤링
        # pattern = '"videoId":".{11}"'
        pattern = 'videoId":"(.*?)"'
        result_id = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        # youtube_ids = [x[11:-1] for x in result_id]
        if len(result_id) >= 1:
            result_youtube_id = result_id[0]
            print(result_youtube_id)
        else:
            result_youtube_id = -1
        # 업로드날짜 크롤링
        pattern_upload = 'uploadDate":"(.*?)"'
        result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_upload) >= 1:
            result_youtube_upload = result_upload[0]
            print(result_youtube_upload)
        else:
            result_youtube_upload = -1
        # 채널등록자 크롤링
        pattern_owner = 'ownerChannelName":"(.*?)",'
        result_owner = re.findall(pattern_owner, str(soup))
        if len(result_owner) >= 1:
            result_youtube_owner = result_owner[0]
            print(result_youtube_owner)
        else:
            result_youtube_owner = -1

        gbmov = gb_mov(mov_prov_id=result_youtube_id,
                       mov_title= result_youtube_title,
                       mov_owner=result_youtube_owner,
                       mov_date=result_youtube_upload,
                       mov_view_cnt=result_youtube_viewcount,
                       mov_tag=result_youtube_tag,
                       cdate=dt.date(),
                       mov_prov= 'youtube')
        db.session.add(gbmov)
        db.session.commit()

        if not search:
                user_session = session.get('user_session')
                if user_session is None:
                    search = search_history(seq = input_yurl,
                                            date= dt.date())
                else:
                    search = search_history(seq = input_yurl,
                                            user_nm = session.get('user_session')['user_nm'],
                                            date= dt.date())

                db.session.add(search)
                db.session.commit()
                return render_template('index.html',
                                       aaa=input_yurl,#기존 yid에서 변경
                                       bbb=result_youtube_viewcount,
                                       ccc=result_youtube_title,
                                       ddd=result_youtube_tag,
                                       eee=yid)
        else:
            return '뭔가 잘못됐다.'
    else:
        return redirect(url_for('main.index'))
#UI-200
#분석목록
@bp.route('/my_analy_list/', methods=('GET', 'POST'))
@login_required
def my_analy_list():
    my_analy_list1 = gb_works.query.filter(gb_works.userid == session.get('user_session')['user_nm']).all()

    return render_template('analysis/my_analy_list.html', my_analy_list1 = my_analy_list1)


#UI-300
#분석목록 - > 프로젝트명 클릭했을때
@bp.route('/my_detail_list/', methods=('GET', 'POST'))
@login_required
def my_detail_list():
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy import create_engine
    engine = create_engine('mysql://dev:mlab0201@192.168.0.190/test_mtrace')
    Session = sessionmaker(bind=engine)
    session = Session()

    my_project = request.form['test']    #UI200에서 폼으로 보내주는 값 저장  smov_id
    result_project = gb_mov.query.filter(gb_mov.mov_id == my_project).first() # gb_mov에서 gb_work에 있는 동일한 mov_id = smov_id를 가져옴
    print('result_project =' , result_project)
    my_sim = gb_mov_sim.query.filter(gb_mov_sim.smov_id == my_project).all()
    print('my_sim =', my_sim)
    #my_sim1 = gb_mov_sim.query.filter(gb_mov_sim.smov_id == my_project).outerjoin(gb_mov_sim.rmov_id == gb_mov.mov_id)
    #print(my_sim1)
    #
    my_match = session.query(gb_mov, gb_mov_sim).filter(gb_mov.mov_id  == gb_mov_sim.smov_id).filter(gb_mov.mov_id  == my_project).all()
    #my_match = session.query(gb_mov, gb_mov_sim).filter(gb_mov.mov_id  == gb_mov_sim.smov_id).filter(gb_mov.mov_id  == my_project).filter(gb_mov.mov_id  == gb_mov_sim.rmov_id).all()


    # my_smov_id = gb_mov.query.filter(gb_mov.mov_id == my_project).first() # gb_mov에서 gb_work에 있는 동일한 mov_id = smov_id를 가져옴
    #my_smov_id = session.query(gb_mov).filter(gb_mov.mov_id  == my_project).all()
    #my_smov_id11 = session.query(gb_mov_sim, my_project).filter(gb_mov_sim.smov_id == my_project).all()
    #my_smov_id11 = session.query(gb_mov_sim).filter(gb_mov_sim.smov_id == my_project).all()
    #aa = session.query(my_smov_id).join(my_smov_id11)
    print('my_match =', str(my_match))
    #print(str(my_smov_id11))
    #print(aa)
    for item in my_match:
        print(item.gb_mov.mov_id, ':' , item.gb_mov_sim.rmov_start_sec)
        #print(item.gb_mov.mov_id, ':' )
    # my_smov_id = gb_mov.query.filter(gb_mov.mov_id == my_project).join(gb_mov_sim, gb_mov.mov_id == gb_mov_sim.smov_id);
    # gb_mov에서 gb_work에 있는 동일한 mov_id = smov_id를 가져옴
    # my_sim = gb_mov_sim.query.filter(gb_mov_sim.smov_id == my_project).all() # gb_sim_mov에서 smov_id가 있는 모든 row를 불러옴
    # print(my_sim)
    # print(my_sim[0].smov_start_sec)
    #    print(my_sim[1].rmov_id)
    #    print()
    #matchList = []
    #for i in my_sim:
    #    matchList.append(gb_mov.query.filter(gb_mov.mov_id == i.rmov_id).all())
        # matchtest = gb_mov.query.filter(gb_mov.mov_id == i.rmov_id).all()
    #    print(matchList)
        #print(my_smov_id, i.rmov_id)
        #print(matchtest)
        #print(matchtest[0].mov_title)
        #print(matchtest[1].mov_title)

    return  render_template('analysis/my_detail_list.html',
                            qqq=my_project,
                            result_project=result_project,
                            result_match_list=my_match)

#my_sim = my_sim


        #print(my_smov_id, i.rmov_id)
        #print(matchtest)

        #print(matchtest.mov_title) 오류


    #print(my_smov_id)
    #print(my_sim[0].rmov_id)
    #print(my_sim[1].rmov_id)



    #return render_template('analysis/my_detail_list.html',
    #                       qqq = my_project,
    #                      my_list = my_smov_id)#,
                           #my_sim = my_sim)

#UI-400
@bp.route('/new_work/', methods=('GET', 'POST'))
@login_required
def new_work():
    return render_template('analysis/new_work.html')


#UI-400_1
@bp.route('/my_analy_list1/', methods=('GET', 'POST'))
@login_required
def make_work():
    dt = datetime.now()
    if request.method == 'POST':
        input_work_nm = request.form['work_nm']
        input_url = request.form['smov_id']
        input_url1 = input_url[-11:]
        search_gv_mov = gb_mov.query.filter_by(mov_prov_id = input_url1).first()
        print(search_gv_mov)

        if search_gv_mov:
            make = gb_works(work_nm= input_work_nm,
                        smov_id= search_gv_mov.mov_id,
                        userid= session.get('user_session')['user_nm'],
                        cdate=dt.date(),
                        smov_id2= input_url1,
                        status=0)
            db.session.add(make)
            db.session.commit()
            return redirect(url_for('analysis.my_analy_list'))


        else:
            html = urllib.request.urlopen(input_url).read()
            soup = BeautifulSoup(html, 'html.parser')
            # 조회수 크롤링
            pattern_viewcount = 'viewCount":"(.*?)"'
            result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
            if len(result_viewcount) >= 1:
                result_youtube_viewcount = result_viewcount[0]
                print(result_youtube_viewcount)
            else:
                result_youtube_viewcount = -1
            # 타이틀 크롤링
            pattern_title = '<title>(.*?)</title>'
            result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
            if len(result_title) >= 1:
                result_youtube_title = result_title[0][:-10]
                print(result_youtube_title)
            else:
                result_youtube_title = -1
                print(result_youtube_title)
            # 유튜브 tag(keyword) 크롤링
            pattern_tag = 'keywords\\":\[.*?\]'
            tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
            result_tag = [y[11:-1] for y in tag]
            if len(result_tag) >= 1:
                result_youtube_tag = result_tag[0]
                print(result_youtube_tag)
            else:
                result_youtube_tag = -1

            # 유튜브 id 크롤링
            # pattern = '"videoId":".{11}"'
            pattern = 'videoId":"(.*?)"'
            result_id = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
            # youtube_ids = [x[11:-1] for x in result_id]
            if len(result_id) >= 1:
                result_youtube_id = result_id[0]
                print(result_youtube_id)
            else:
                result_youtube_id = -1

            # 업로드날짜 크롤링
            pattern_upload = 'uploadDate":"(.*?)"'
            result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
            if len(result_upload) >= 1:
                result_youtube_upload = result_upload[0]
                print(result_youtube_upload)
            else:
                result_youtube_upload = -1

            # 채널등록자 크롤링
            pattern_owner = 'ownerChannelName":"(.*?)",'
            result_owner = re.findall(pattern_owner, str(soup))
            if len(result_owner) >= 1:
                result_youtube_owner = result_owner[0]
                print(result_youtube_owner)
            else:
                result_youtube_owner = -1

            gbmov = gb_mov(mov_prov_id=result_youtube_id,
                       mov_title=result_youtube_title,
                       mov_owner=result_youtube_owner,
                       mov_date=result_youtube_upload,
                       mov_view_cnt=result_youtube_viewcount,
                       mov_tag=result_youtube_tag,
                       cdate=dt.date(),
                       mov_prov= 'youtube')
            db.session.add(gbmov)
            db.session.commit()
            search1 = gb_mov.query.filter_by(mov_prov_id = input_url1).first()

            make1 = gb_works(work_nm=input_work_nm,
                            smov_id = search1.mov_id,
                            userid=session.get('user_session')['user_nm'],
                            cdate=dt.date(),
                            smov_id2=input_url1,
                            status=0)
            db.session.add(make1)
            db.session.commit()
            return redirect(url_for('analysis.my_analy_list'))



#UI-400_1
#@bp.route('/my_analy_list1/', methods=('GET', 'POST'))
#@login_required
#def make_work():
#    dt = datetime.now()
#    if request.method == 'POST':
#        input_work_nm = request.form['work_nm']
#        input_url = request.form['smov_id']
#        input_url1 = input_url[-11:]
#        make = gb_works(work_nm= input_work_nm,
#                        smov_id= input_url,
#                        userid= session.get('user_session')['user_nm'],
 #                       cdate=dt.date(),
  #                      smov_id2= input_url1,
   #                     status=0)
#
#
 #       html = urllib.request.urlopen(input_url).read()
  #      soup = BeautifulSoup(html, 'html.parser')
   #     # 조회수 크롤링
    #    pattern_viewcount = 'viewCount":"(.*?)"'
     #   result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
      #  if len(result_viewcount) >= 1:
       #     result_youtube_viewcount = result_viewcount[0]
        #    print(result_youtube_viewcount)
        #else:
        #    result_youtube_viewcount = -1

        # 타이틀 크롤링
        #pattern_title = '<title>(.*?)</title>'
        #result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
        #if len(result_title) >= 1:
       #    result_youtube_title = result_title[0][:-10]
        #    print(result_youtube_title)
        #else:
       #     result_youtube_title = -1
       #     print(result_youtube_title)

        # 유튜브 tag(keyword) 크롤링
       # pattern_tag = 'keywords\\":\[.*?\]'
       # tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
       # result_tag = [y[11:-1] for y in tag]
       # if len(result_tag) >= 1:
       #     result_youtube_tag = result_tag[0]
      #      print(result_youtube_tag)
       # else:
       #     result_youtube_tag = -1

        # 유튜브 id 크롤링
        # pattern = '"videoId":".{11}"'
       # pattern = 'videoId":"(.*?)"'
       # result_id = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        # youtube_ids = [x[11:-1] for x in result_id]
       # if len(result_id) >= 1:
        #    result_youtube_id = result_id[0]
       #     print(result_youtube_id)
       # else:
       #     result_youtube_id = -1

        # 업로드날짜 크롤링
       # pattern_upload = 'uploadDate":"(.*?)"'
       # result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
      #  if len(result_upload) >= 1:
       #     result_youtube_upload = result_upload[0]
       #     print(result_youtube_upload)
       # else:
      #      result_youtube_upload = -1

       # # 채널등록자 크롤링
       # pattern_owner = 'ownerChannelName":"(.*?)",'
        #result_owner = re.findall(pattern_owner, str(soup))
       # if len(result_owner) >= 1:
        #    result_youtube_owner = result_owner[0]
     #       print(result_youtube_owner)
       # else:
       #     result_youtube_owner = -1

       # gbmov = gb_mov(mov_prov_id=result_youtube_id,
        #               mov_title=result_youtube_title,
        ##               mov_owner=result_youtube_owner,
        #               mov_date=result_youtube_upload,
        #               mov_view_cnt=result_youtube_viewcount,
        #               mov_tag=result_youtube_tag,
        #               cdate=dt.date(),
        #               mov_prov= 'youtube')

       # db.session.add(make)
       # db.session.add(gbmov)
       # db.session.commit()
       # return redirect(url_for('analysis.my_analy_list'))








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