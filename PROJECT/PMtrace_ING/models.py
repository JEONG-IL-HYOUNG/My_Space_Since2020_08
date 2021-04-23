from app import db
from datetime import datetime

#계정 table
class gb_account(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    user_nm = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255),nullable=True)
    pw = db.Column(db.String(255), nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    user_rnm = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(255))

#프로젝트 작업 
class gb_works(db.Model):

    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(255), nullable=True)
    work_nm = db.Column(db.String(255), nullable=True)
    smov_id = db.Column(db.String(255), nullable=True)  # 기준동영상
    status= db.Column(db.String(255), nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    fdate = db.Column(db.DateTime(), nullable=True)
    smov_id2 = db.Column(db.String(255), nullable=True)

#동영상
class gb_mov(db.Model):
    mov_id = db.Column(db.Integer, nullable=False, primary_key=True)
    mov_prov = db.Column(db.String(255), nullable=True)
    mov_prov_id = db.Column(db.String(255), nullable=True)
    mov_title = db.Column(db.String(255), nullable=True)
    mov_owner = db.Column(db.String(255), nullable=True)
    mov_date = db.Column(db.String(10), nullable=True)
    mov_view_cnt = db.Column(db.BigInteger)
    mov_tag = db.Column(db.Text, nullable=True) #동영상태그
    mov_desc = db.Column(db.Text, nullable=True) #동영상 설명
    cdate = db.Column(db.String(10))
        
#동영상 유사도
class gb_mov_sim(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smov_id = db.Column(db.String(255), nullable=False) #기준동영상
    rmov_id = db.Column(db.String(255), nullable=False) #유사동영상
    smov_start_sec  = db.Column(db.Integer, nullable=True)
    smov_end_sec = db.Column(db.Integer, nullable=True)
    rmov_start_sec = db.Column(db.Integer, nullable=True)
    rmov_end_sec = db.Column(db.Integer, nullable=True)
    cdate = db.Column(db.DateTime(), nullable=True)
    mov_sim = db.Column(db.Integer, nullable=True) #영상유사도
    sim_type = db.Column(db.String(100), nullable=False)

#메타정보 유사도
class gb_meta_sim(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smov_id = db.Column(db.String(255), nullable=False) #기준동영상
    rmov_id = db.Column(db.String(255), nullable=False) #유사동영상
    meta_sim = db.Column(db.Integer, nullable=True) #메타유사도
    sim_type = db.Column(db.String(100), nullable=False)

#검색목록
class gb_search_lists(db.Model):
    work_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    match_id = db.Column(db.String(255), nullable=False) #기준동영상
    use_yn = db.Column(db.String(255), nullable=False) #유사동영상

class search_history(db.Model):
    history_id = db.Column(db.Integer, primary_key=True)
    seq = db.Column(db.String(255), nullable=False)
    user_nm = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime(), nullable=True)
