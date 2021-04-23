from flask import Blueprint, url_for, render_template, request, flash, session, g
from werkzeug.utils import redirect, secure_filename
import os
from models import gb_account, gb_works, gb_mov, gb_mov_sim, search_history, gb_meta_sim
from forms import post_db_test
from app import db
from .auth_views import login_required, load_logged_in_user
import functools
from datetime import datetime
import requests

# 크롤링할때 import
import os
import shutil
from urllib.request import Request, urlopen
import urllib.request
from urllib.error import URLError, HTTPError
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date
import sys
# if os.path.exists('../python/oaislib_org.py'):
#     shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib

bp = Blueprint('analysis', __name__, url_prefix='/analysis')

#index page에서 검색버튼 눌렀을때
#페이지 넘어가지 않고 index 페이지에서 동영상 출력
#UI-100
@bp.route('/search/', methods=('GET', 'POST'))
def search_main():
    dt = datetime.now()
    if request.method == 'POST':
        input_yurl = request.form['video_url']
        error = None
        https = 'https://'
        find_https = input_yurl.find('https://')
        print(find_https)
        print(input_yurl)

        if input_yurl == '':
            error = '검색어를 입력하세요!!!'
            flash(error)
            return redirect(url_for('main.index'))
        if error is None:
            # url 정규표현식 www.으로 시작하면 ok임
            expr = re.compile(
                r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]'
                r'+(:[0-9]+)?|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-]*)?\??(?:[-\+=&;%@.\w]*)#?(?:[\w]*))?)')

            if expr.match(input_yurl):
                print('it is valid')
                yid = input_yurl[-11:]
                search = search_history.query.filter_by(seq=yid).all()
                if find_https == 0:
                    req = Request(input_yurl)
                    try:
                        html = urlopen(req)
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print('We failed to reach a server.')
                            #print('Reason: ', e.reason)
                            print('flash comple')

                            # error = '잘못된 URL'
                            test_text = False

                            flash(test_text)

                            return redirect(url_for('main.index'))

                        elif hasattr(e, 'code'):
                            print('The server couldn\'t fulfill the request.')
                            print('Error code: ', e.code)
                            error = '잘못된 URL'
                            flash(error)
                            return redirect(url_for('main.index'))
                    else:
                        print('ok url')
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
                                       mov_prov='local_youtube')
                        db.session.add(gbmov)
                        db.session.commit()
                        if not search:
                            user_session = session.get('user_session')
                            if user_session is None:
                                search = search_history(seq=input_yurl,
                                                        date=dt.date())
                            else:
                                search = search_history(seq=input_yurl,
                                                        user_nm=session.get('user_session')['user_nm'],
                                                        date=dt.date())

                            db.session.add(search)
                            db.session.commit()
                            return render_template('index.html',
                                                   aaa=input_yurl,  # 기존 yid에서 변경
                                                   bbb=result_youtube_viewcount,
                                                   ccc=result_youtube_title,
                                                   ddd=result_youtube_tag,
                                                   eee=yid)
                        else:
                            return '뭔가 잘못됐다1.'

                # if find_https==-1일때
                else:
                    past_req = str(https + input_yurl)
                    print(past_req)
                    try:
                        html = urlopen(past_req)
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print('We failed to reach a server.')
                            print('Reason: ', e.reason)
                            error='URL ERROR 다시 확인'
                            flash(error)
                            return redirect(url_for('main.index'))


                        elif hasattr(e, 'code'):
                            print('The server couldn\'t fulfill the request.')
                            print('Error code: ', e.code)
                            error = 'HTTP ERROR 다시 확인'
                            flash(error)

                            return redirect(url_for('main.index'))
                    else:
                        print('ok url')
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
                                       mov_prov='local_youtube')
                        db.session.add(gbmov)
                        db.session.commit()
                        if not search:
                            user_session = session.get('user_session')
                            if user_session is None:
                                search = search_history(seq=input_yurl,
                                                        date=dt.date())
                            else:
                                search = search_history(seq=input_yurl,
                                                        user_nm=session.get('user_session')['user_nm'],
                                                        date=dt.date())

                            db.session.add(search)
                            db.session.commit()
                            return render_template('index.html',
                                                   aaa=input_yurl,  # 기존 yid에서 변경
                                                   bbb=result_youtube_viewcount,
                                                   ccc=result_youtube_title,
                                                   ddd=result_youtube_tag,
                                                   eee=yid)
                        else:
                            return '뭔가 잘못됐다2.'

            else:
                target_url = 'https://www.youtube.com/results?search_query=' + input_yurl

                error = '일반검색어 입력'
                flash(error)
                print('일반검색어가 들어온 경우일때 처리')




                return redirect(url_for('main.index'))



#UI-100_1
@bp.route('/go_work/', methods=('GET', 'POST'))
def go_work():
    if g.user is None:
        return redirect(url_for('auth.login'))
    else:
        return render_template('analysis/new_work.html')


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
    #################################
    my_project = request.form['test']    #UI200에서 폼으로 보내주는 값 저장  smov_id
    #1. gb_mov에서 gb_work에 있는 동일한 mov_id = smov_id를 가져옴
    result_project = gb_mov.query.filter(gb_mov.mov_id == my_project).first()
    #print('result_project =' , result_project)
    #2. Gb_mov_sim 테이블에서 my_project와 같은 값(GB_mov_sim.smov_id == My_project)을 가진 모든 row를 가져온다. Smov_id 하나당 rmov_id가 여러 개 있을 수있기 때문
    my_sim = gb_mov_sim.query.filter(gb_mov_sim.smov_id == my_project).all()
    #print('my_sim =', my_sim)
    #3.Gb_mov table에서 GB_mov_sim의 rmov_id를 기준으로  정보값을 가지고 온다.
    #유사동영상 출력 부분에서 타이틀, URL, 채널오너 가지고 오는 변수
    #gb_mov_sim 테이블에 기준동영상 하나당 유사동영상이 여러개 있을 수 있다.
    #3-1. 유사동영상rmov_id를 기준으로 gb_mov테이블에서 정보를 가져와야 한다.
    #값이 여러개 들어올 수 있으니 빈 리스트를 만들어준 뒤 append 방식으로 붙여 넣는다.
    match_list = []
    for i in my_sim:
        match_list.append(gb_mov.query.filter(gb_mov.mov_id == i.rmov_id).all())
    print('match_list =', match_list)
    print(result_project.mov_id)

    ######21/02/02######
    # #4. meta 유사도 부분도 위와 같이 불러온다.
    my_meta = gb_meta_sim.query.filter(gb_meta_sim.smov_id == my_project).all()
    match_metalist =[]
    for x in my_meta:
        match_metalist.append(gb_mov.query.filter(gb_mov.mov_id == x.rmov_id).all())
    print('match_metalist =', match_metalist)
    print()


    return render_template('analysis/my_detail_list.html',
                           qqq=my_project,
                           result_project=result_project,
                           result_match_list=match_list,
                           my_sim = my_sim,
                           result_match_meta=match_metalist,
                           my_meta = my_meta,
                           zip = zip)


#UI-400
@bp.route('/new_work/', methods=('GET', 'POST'))
@login_required
def new_work():
    return render_template('analysis/new_work.html')

# UI-400_1
@bp.route('/my_analy_list1/', methods=('GET', 'POST'))
@login_required
def make_work():
    dt = datetime.now()
    if request.method == 'POST':
        error = None
        input_work_nm = request.form['work_nm']
        if input_work_nm == '':
            error = '프로젝트명을 입력하세요!'
        if error is None:
            # 유튜브 URL 등록할때
            if request.form['foo'] == 'smov_id':
                error1 = None
                input_url = request.form['smov_id']
                if input_url =='':
                    error1 = 'URL을 입력하세요!'
                if error1 is None:
                    input_url1 = input_url[-11:]
                    search_gv_mov = gb_mov.query.filter_by(mov_prov_id=input_url1).first()
                    print(search_gv_mov)

                    if search_gv_mov:
                        make = gb_works(work_nm=input_work_nm,
                                        smov_id=search_gv_mov.mov_id,
                                        userid=session.get('user_session')['user_nm'],
                                        cdate=dt.date(),
                                        smov_id2=input_url1,
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
                                       mov_prov='local_youtube')
                        db.session.add(gbmov)
                        db.session.commit()
                        search1 = gb_mov.query.filter_by(mov_prov_id=input_url1).first()

                        make1 = gb_works(work_nm=input_work_nm,
                                         smov_id=search1.mov_id,
                                         userid=session.get('user_session')['user_nm'],
                                         cdate=dt.date(),
                                         smov_id2=input_url1,
                                         status=0)
                        db.session.add(make1)
                        db.session.commit()
                        return redirect(url_for('analysis.my_analy_list'))
                else:
                    flash(error1)
                    return redirect(url_for('analysis.make_work'))


            # radio button file 받기
            else:
                if request.method == 'POST':
                    UPLOAD_DIR = "D:\mlab Dropbox\\mlab\\04_lab\\01_labbing\\816_mtrace_web\\static\\815_mtrace_anal\\ps8010"
                    f = request.files['local_file']
                    mov_keyword = request.form['keyword']
                    mov_desc = request.form['descript']

                    print(f.filename)
                    add_gb_mov = gb_mov(mov_title=f.filename,
                                        cdate=dt.date(),
                                        mov_owner=session.get('user_session')['user_nm'],
                                        mov_prov='local_file',
                                        mov_tag=mov_keyword,
                                        mov_desc=mov_desc)
                    db.session.add(add_gb_mov)
                    db.session.commit()

                    search2 = gb_mov.query.filter_by(mov_title=f.filename).filter_by(
                        mov_owner=session.get('user_session')['user_nm']).first()
                    print(search2)

                    add_gb_work_file = gb_works(work_nm=input_work_nm,
                                                smov_id=search2.mov_id,
                                                userid=session.get('user_session')['user_nm'],
                                                cdate=dt.date(),
                                                status=0)

                    db.session.add(add_gb_work_file)
                    db.session.commit()

                    change_fname = gb_mov.query.filter_by(mov_title=f.filename).first()
                    print(change_fname)
                    print(change_fname.mov_id)

                    # fname = secure_filename(f.filename) 업로드 된 파일의 이름이 안전한가를 확인해주는 함수
                    fname = secure_filename(str(change_fname.mov_id) + ".mp4")  # int +str이 되어서 type error 발생 파일명에 str추가

                    path = os.path.join(UPLOAD_DIR, fname)
                    f.save(path)
                    return redirect(url_for('analysis.my_analy_list'))

        else:
            flash(error)
            return redirect(url_for('analysis.make_work'))
    else:
        return render_template('analysis/new_work.html')

#UI-400_1 ajax로 완료.
@bp.route('/my_analy_list2/', methods=('GET', 'POST'))
def url_test():
    print("request ok!")
    if request.method == 'POST':
        URL = request.form['smov_id']
        print('URL ', URL)
        response = requests.get(URL)
        print(response.status_code)

        html = urllib.request.urlopen(URL).read()
        soup = BeautifulSoup(html, 'html.parser')
        pattern_viewcount = 'viewCount":"(.*?)"'
        result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_viewcount) >= 1:
            result_youtube_viewcount = 1
            print(result_youtube_viewcount)
            flash('ok url')
            # return redirect(url_for('analysis.new_work'))
            return {'status' : "ok"}
        else:
            result_youtube_viewcount = -1
            print(result_youtube_viewcount)
            flash('nononono')
            # return redirect(url_for('analysis.new_work'))
            return {'status' : "no"}







#파일 업로드 test
@bp.route('/fileupload/', methods=('GET', 'POST'))
def upload_files():
    if request.method == 'POST':
        UPLOAD_DIR = "D:/test"
        f = request.files['file']
        fname = secure_filename(f.filename)
        path = os.path.join(UPLOAD_DIR, fname)
        f.save(path)
        return 'File upload complete (%s)' % path

#test
@bp.route('/test/', methods=('GET', 'POST'))
def test():
    return render_template('analysis/test.html')


#test
@bp.route('/test1/', methods=('GET', 'POST'))
def test1():
    dt = datetime.now()
    if request.method == 'POST':
        UPLOAD_DIR = "D:\mlab Dropbox\\mlab\\04_lab\\01_labbing\\816_mtrace_web\\static\\815_mtrace_anal"
        f = request.files['local_file']
        print(f.filename)

        add_gb_mov = gb_mov(mov_title=f.filename,
                        cdate=dt.date(),
                        mov_owner=session.get('user_session')['user_nm'],
                        mov_prov= 'local_file')
        db.session.add(add_gb_mov)
        db.session.commit()

        change_fname = gb_mov.query.filter_by(mov_title = f.filename).first()
        print(change_fname)
        print(change_fname.mov_id)

        # fname = secure_filename(f.filename) 업로드 된 파일의 이름이 안전한가를 확인해주는 함수
        fname = secure_filename(str(change_fname.mov_id) + ".mp4") # int +str이 되어서 type error 발생 파일명에 str추가

        path = os.path.join(UPLOAD_DIR, fname)
        f.save(path)
        return 'File upload complete (%s)' % path


