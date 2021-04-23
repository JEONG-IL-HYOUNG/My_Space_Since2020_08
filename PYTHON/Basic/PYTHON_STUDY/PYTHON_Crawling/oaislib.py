# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200211
# goal : 개인용 모듈 
#
# desc : oaislib.fn_remove_all_files_in_folder(folder_name) # 폴더 내 파일 삭제 
# desc : oaislib.fn_read_utftxt_to_list(filename)  #utf8의 텍스트를 읽어 들여서 리스트로 리턴 
# desc : oaislib.fn_get_clean_text(text) #문장에서 기호제거
# desc : oaislib.fn_get_text_ko(text)  #문장에서 한글 추출
# desc : oaislib.fn_get_text_en(text) #문장에서 영문추출
# desc : oaislib.fn_get_number(text) #문장에서 숫자 추출
# desc :
# desc : oaislib.fn_get_timetail() #파일명 생성을 위한 테일링 YYMMDD_HHMMSS 생성

# desc : ## DB
# desc : oaislib.fn_connect_dev_db() #개발부DB 연결
# desc : oaislib.fn_connect_lab_db() #연구소DB 연결
# desc : oaislib.fn_get_df_from_mstuv_dev_db(sql_str) #개발서버에서 sql결과를 df로 리턴
# desc : oaislib.fn_get_df_from_lab_db(sql_str) #연구소 서버에서 sql결과를 df로 리턴
# desc : oaislib.fn_run_sql_to_mstuv_dev_db(sql_str) #mlab 개발DB에 sql문 실행
# desc : oaislib.fn_run_sql_to_lab_db(sql_str) # mlab lab DB에 sql문 실행
# desc :
# desc : oaislib.fn_get_date_str(): #YYYY-MM-DD의 날짜 문자열 리턴
# desc : oaislib.fn_change_element_in_list_to_int(lst) # 요소를 숫자로 변환
# desc :
# desc :
# desc :


# module for oaiskoo

'''
사용법
import shutil
if os.path.exists("../python/oaislib.py"):
    shutil.copy("../python/oaislib_org.py','oaislib.py")
import oaislib
'''
import os
import re
import pymysql
import pandas as pd
from datetime import datetime

# 폴더 내 파일 삭제 
def fn_remove_all_files_in_folder(folder_name):
    if os.path.exists(folder_name):
        for file in os.scandir(folder_name):
            os.remove(file.path)
        return 0
    else:
        return 1
    
# utf8의 텍스트를 읽어 들여서 리스트로 리턴 
def fn_read_utftxt_to_list(filename):
    output = list()
    with open(filename, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip() #공백제거
            output.append(line)
    f.close()
    return output
# filename ='input/kor_sentences_utf8.txt'
#rlt = oais.read_utf_txt_to_list(filename)

# 문장에서 기호 제거
def fn_get_clean_text(text):
    text = str(text)
    text = text.replace("\\","") #위의 표현으로 역슬래시가 제거가 안되어서 추가함
    text = re.sub('[-=+#/\?:^$.,@*\"※~&%ㆍ!ㅡ』\\;_‘|\(\)\[\]\<\>`\'…》]', '', text)
    return text

# 문장에서 한글만 추출
def fn_get_text_ko(text):
    text = str(text)
    text = re.compile('[가-힣]+').findall(text)
    text = ' '.join(text)
    return text

# 문장에서 영어만 추출
def fn_get_text_en(text):
    text = str(text)
    text = re.compile('[a-zA-Z]+').findall(text)
    text = ' '.join(text)
    return text

# 문장에서 숫자만 추출
def fn_get_number(text):
    text = str(text)
    text = re.compile('[0-9.]+').findall(text)
    text = ' '.join(text)
    return text
    
## 지금 시각을 YYMMDD_HHMMSS 형태로 리턴하기
def fn_get_timetail():
    now = datetime.now()
    yy =  str(now.year)[2:]
    mm = str(now.month)
    dd = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)
    ss = str(now.second)
    timetail = yy + mm + dd + '_'+ hh + mm + ss
    return timetail

## connect_db
def fn_connect_dev_db():
    db = pymysql.connect(host='bizdb.smartmlab.com',
                         port=33306, user='stuv', passwd='stuv!@#$',
                         db='stuv', charset='utf8')
    return db

def fn_connect_lab_db():
    db = pymysql.connect(host='192.168.0.190',
                         port=3306, user='oaiskoo', passwd='u4i3o2p1',
                         db='labmstuv', charset='utf8')
    return db

## 위의 것을 사용(호환성때문에 둠)
def fn_lab_db_connect():
    db = pymysql.connect(host='192.168.0.190',
                         port=3306, user='oaiskoo', passwd='u4i3o2p1',
                         db='labmstuv', charset='utf8')
    return db

## mlab 개발 서버에서 쿼리 결과를 데이터 프레임으로 받음
def fn_get_df_from_mstuv_dev_db(sql_str):

    db = fn_connect_dev_db()
    
    try:
        cursor = db.cursor()
        cursor.execute(sql_str)
        table_col = cursor.description
        table_col = [items[0] for items in table_col]
        rlt = cursor.fetchall()
        rlt_df = pd.DataFrame(list(rlt), columns=table_col)
        rlt_df.columns = map(str.lower, rlt_df.columns)
        
    finally:
        db.close()

    return rlt_df

## 연구소 서버에서 쿼리 결과를 데이터 프레임으로 받음
def fn_get_df_from_lab_db(sql_str):
    db = fn_connect_lab_db()
    try:
        cursor = db.cursor()
        cursor.execute(sql_str)
        table_col = cursor.description
        table_col = [items[0] for items in table_col]
        rlt = cursor.fetchall()
        rlt_df = pd.DataFrame(list(rlt), columns=table_col)
        rlt_df.columns = map(str.lower, rlt_df.columns)

    finally:
        db.close()

    return rlt_df

## mlab 개발DB에 sql문 실행
def fn_run_sql_to_mstuv_dev_db(sql_str):
    db = fn_connect_dev_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_str)
            db.commit()
    finally:
        db.close()

## mlab lab DB에 sql문 실행
def fn_run_sql_to_lab_db(sql_str):
    db = fn_connect_lab_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(sql_str)
            db.commit()
    finally:
        db.close()

        
## YYYY-MM-DD의 날짜 문자열 리턴
def fn_get_date_str():
    now_time = datetime.now()
    date_str = str(now_time.year) + "-" + str(now_time.month) + "-" + str(now_time.day)
    return date_str

## 요소를 숫자로 변환
def fn_change_element_in_list_to_int(lst):
    cnt = len(lst)
    for i in range(cnt):
        x = lst[i]
        lst[i] = int(x)
    return lst
