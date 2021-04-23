from app import db

#계정 table
class gb_account(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    user_nm = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(255),nullable=True)
    pw = db.Column(db.String(255), nullable=False)
    cdate = db.Column(db.DateTime(), nullable=True)


#프로젝트 table
class gb_projects(db.Model):
    prj_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prj_nm = db.Column(db.String(255), nullable=True)
    user_nm = db.Column(db.String(255), nullable=True)
    #cdate = db.Column(db.DateTime(), nullable=True)
    #fdate = db.Column(db.DateTime(), nullable=True)
    status= db.Column(db.String(255), nullable=True)
    smov_id = db.Column(db.String(255), nullable=True) #기준동영상
    match_id = db.Column(db.String(255), nullable=True) #매치동영상


#동영상 유사분석
class gb_mov_sim_anal(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    smov_id = db.Column(db.String(255), nullable=False) #기준동영상
    rmov_id = db.Column(db.String(255), nullable=False) #유사동영상
    #smov_start_sec  = db.Column(db.Integer, nullable=True)
    #smov_end_sec = db.Column(db.Integer, nullable=True, primary_key=True)
    #rmov_start_sec = db.Column(db.Integer, nullable=True)
    #rmov_end_sec = db.Column(db.Integer, nullable=True)
    #cdate = db.Column(db.DateTime(), nullable=True)



#동영상
class gb_mov(db.Model):
    mov_id = db.Column(db.String(255), nullable=False, primary_key=True)
    mov_prov = db.Column(db.String(255), nullable=False)
    mov_prov_id = db.Column(db.String(255), nullable=False)
    mov_title = db.Column(db.String(255), nullable=False)
    mov_owner = db.Column(db.String(255), nullable=False)
    mov_date = db.Column(db.DateTime(), nullable=False)
    mov_view_cnt = db.Column(db.Integer)
    mov_tag = db.Column(db.String(255), nullable=False) #동영상태그
    mov_desc = db.Column(db.String(255), nullable=False) #동영상 설명
    cdate = db.Column(db.DateTime())



