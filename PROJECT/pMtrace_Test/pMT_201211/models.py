from app import db
from datetime import datetime

#계정생성, 로그인
class gb_account(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    user_nm = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255),nullable=True)
    pw = db.Column(db.String(255), nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    last_login_date = db.Column(db.DateTime(), nullable=True)

#프로젝트 작업 
class gb_works(db.Model):
    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(255), nullable=True)
    work_nm = db.Column(db.String(255), nullable=True)
    smov_id = db.Column(db.String(255), nullable=True)  # 기준동영상
    status= db.Column(db.String(255), nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    fdate = db.Column(db.DateTime(), nullable=True)

#동영상
class gb_mov(db.Model):
    mov_id = db.Column(db.String(255), nullable=False, primary_key=True) #동영상id
    mov_prov = db.Column(db.String(255), nullable=False) #동영상 프로바이더{youtube, local}
    mov_prov_id = db.Column(db.String(255), nullable=False) #프로바이더의 id
    mov_title = db.Column(db.String(255), nullable=False)
    mov_owner = db.Column(db.String(255), nullable=True)
    mov_date = db.Column(db.DateTime(), nullable=True)
    mov_view_cnt = db.Column(db.Integer, nullable=True)
    mov_tag = db.Column(db.String(255), nullable=True) #동영상태그
    mov_desc = db.Column(db.String(255), nullable=True) #동영상 설명
    cdate = db.Column(db.DateTime(), nullable=False)
        
#동영상 유사도
class gb_mov_sim(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smov_id = db.Column(db.String(255), nullable=True) #기준동영상
    rmov_id = db.Column(db.String(255), nullable=True) #유사동영상
    smov_start_sec  = db.Column(db.Integer, nullable=True)
    smov_end_sec = db.Column(db.Integer, nullable=True, primary_key=True)
    rmov_start_sec = db.Column(db.Integer, nullable=True)
    rmov_end_sec = db.Column(db.Integer, nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    mov_sim = db.Column(db.Integer, nullable=True) #영상유사도


#메타정보 유사도
class gb_meta_sim(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smov_id = db.Column(db.String(255), nullable=False) #기준동영상
    rmov_id = db.Column(db.String(255), nullable=False) #유사동영상
    meta_sim = db.Column(db.Integer, nullable=True) #메타유사도

#매칭리스트
class gb_match_lists(db.Model):
    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.Integer, nullable=False)
    use_yn =  db.Column(db.String(20), nullable=False) #유사동영상

#검색목록
class gb_search_lists(db.Model):
    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.String(255), nullable=False) #기준동영상
    use_yn = db.Column(db.String(255), nullable=False) #유사동영상

class search_histroy(db.Model):
    seq = db.Column(db.String(255), primary_key=True, nullable=False)
    user_nm = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime(), nullable=True)
