# -*- coding: utf-8 -*-
# date : 200604
# goal : 원소스에서 동영상 텍스트 정보를 받아서 한글만 추출후 어절로 태그를 구성해서 DB에 업로드
#
# desc : 1. source
# desc :    video_syc, video_key_tag, tag_syc
# desc : 2. target
# desc :    anal_word : 비디오 별 메타정보 텍스트의 어절 정보를 구축
# desc :      `video_id` varchar(200) 
# desc :      `youtube_id` varchar(100) 
# desc :      `word_org` text - 리스트를 컬럼에 집어넣음

# desc :      `INSERT_DATE` date 
# desc : 
#
# prss : 1. 
# prss : 
# prss : 
# prss : 
# prss : 
# prss : 

# note
# 200604 - ps01-10의 파일에서 Oki(형태소)를 어절로 분절하고 insert하는 테이블 명 변경

import os
import shutil
import time
import re
import pandas as pd
import numpy as np
if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py','oaislib.py')
import oaislib
from datetime import datetime
start = time.time()

##import
import sys
import pymysql
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

print('ps01-11_cal_video_sim_preprocess_with_word.py start')
# db의 date에 insert 할 내용
now = datetime.now()
date_str = str(now.year)+"-"+str(now.month)+"-"+str(now.day)



## get video table
sql = "select video_id, provi_video_id, title FROM video_syc"
video_df = oaislib.fn_get_df_from_lab_db(sql)
video_df.columns = ['video_id', 'provi_video_id', 'title']

## get key_tag table
sql = 'SELECT video_id, video_key_tag FROM video_key_tag_syc where USE_YN = "Y"'
keytag_df = oaislib.fn_get_df_from_lab_db(sql)

## get tag table
sql = "SELECT video_id, tag_contents FROM tag_syc"
tag_df = oaislib.fn_get_df_from_lab_db(sql)
tag_df.columns = ['video_id', 'tag_contents']

##ps 전처리
## 키태그 테이블 전처리
keytag_df = keytag_df[keytag_df["video_key_tag"] != ' ']
keytag_df['video_key_tag'] = keytag_df.video_key_tag.astype('str')
keytag_df.fillna('', inplace=True)
keytag_fin = pd.DataFrame(keytag_df.groupby('video_id')['video_key_tag'].apply(','.join).reset_index())


## 태그 테이블 전처리
#태그에서 null과 빈칸으로된 행 제거
if tag_df['tag_contents'].isnull().sum() > 0:  
    tag_df = tag_df.dropna(subset=["tag_contents"])  
if tag_df['tag_contents'].isnull().sum() > 0:
    tag_df = tag_df[tag_df["tag_contents"] != ' ']
# 비디오 ID별 그룹바이 (댓글)
tag_df['tag_contents'] = tag_df.tag_contents.astype('str')
tag_df.fillna('', inplace=True)
tag_group = pd.DataFrame(tag_df.groupby('video_id')['tag_contents'].apply(','.join).reset_index())
tag_group['tag_contents'] = tag_group["tag_contents"].replace(r'[\n]', '', regex=True)
tag_fin = tag_group[['video_id', 'tag_contents']]


##비디오 테이블 전처리
#타이틀 테이블 전처리(null이면 제외) 
if video_df['title'].isnull().sum() > 0:
    video_df = video_df[video_df["title"] != ' ']

# 비디오 ID 기준 머지
video_fin = video_df[['video_id', 'provi_video_id', 'title']]

contents_df = pd.merge(video_fin, keytag_fin, on='video_id', how='left')
contents_df = pd.merge(contents_df, tag_fin, on='video_id', how='left')
contents_df = contents_df.fillna('')

#토크나이징
#타이틀, 키태그, 태그 데이터 한글,영어 분리
contents_df['title_kor'] = contents_df["title"].replace(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', regex=True)
contents_df['title_eng'] = contents_df["title"].replace(r'[^A-Za-z]', ' ', regex=True)
contents_df['key_tag_kor'] = contents_df["video_key_tag"].replace(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', regex=True)
contents_df['key_tag_eng'] = contents_df["video_key_tag"].replace(r'[^A-Za-z]', ' ', regex=True)
contents_df['tag_kor'] = contents_df["tag_contents"].replace(r'[^가-힣ㄱ-ㅎㅏ-ㅣ]', ' ', regex=True)
contents_df['tag_eng'] = contents_df["tag_contents"].replace(r'[^A-Za-z]', ' ', regex=True)
contents_df['title_kor'] = contents_df["title_kor"].replace(r'\s+', ' ', regex=True)
contents_df['title_eng'] = contents_df["title_eng"].replace(r'\s+', ' ', regex=True)
contents_df['key_tag_kor'] = contents_df["key_tag_kor"].replace(r'\s+', ' ', regex=True)
contents_df['key_tag_eng'] = contents_df["key_tag_eng"].replace(r'\s+', ' ', regex=True)
contents_df['tag_kor'] = contents_df["tag_kor"].replace(r'\s+', ' ', regex=True)
contents_df['tag_eng'] = contents_df["tag_eng"].replace(r'\s+', ' ', regex=True)

##ps tokenizing

# 키태그 토크나이징
key_tag_kor_token = []
for i in range(len(contents_df)):
#    key_tag_kor_token_okt = okt.nouns(contents_df.key_tag_kor.loc[i])
    key_tag_kor_token_word = contents_df['key_tag_kor'].iloc[i].split()
    key_tag_kor_token.append(key_tag_kor_token_word)
contents_df['key_tag_kor_noun'] = key_tag_kor_token

# ### 댓글 토크나이징
tag_kor_token =[]
for i in range(len(contents_df)):
#    tag_kor_token_okt = okt.nouns(contents_df.tag_kor.loc[i])
    tag_kor_token_word = contents_df['tag_kor'].iloc[i].split()
    tag_kor_token.append(tag_kor_token_word)
contents_df['tag_kor_noun'] = tag_kor_token

## 타이틀 토크나이징
title_kor_token =[]
for i in range(len(contents_df)):
#    title_kor_token_okt = okt.nouns(contents_df.title_kor.loc[i])
    title_kor_token_word = contents_df['title_kor'].iloc[i].split()
    title_kor_token.append(title_kor_token_word)
contents_df['title_kor_noun'] = title_kor_token

# 최종 데이터 테이블
contents_fin = contents_df[['video_id', 'provi_video_id', 'title', 'video_key_tag', 'tag_contents',
                                 'title_kor_noun', 'key_tag_kor_noun', 'tag_kor_noun']]
contents_fin["title_kor_noun"] = contents_fin["title_kor_noun"].astype(str)
contents_fin["key_tag_kor_noun"] = contents_fin["key_tag_kor_noun"].astype(str)
contents_fin["tag_kor_noun"] = contents_fin["tag_kor_noun"].astype(str)

# 타이틀, 키태그, 태그 모두 비어 있는 비디오 테이블 제거
contents_fin = contents_fin[(contents_fin['title_kor_noun'] != '[]') |
                                    (contents_fin['key_tag_kor_noun'] != '[]') |
                                    (contents_fin['tag_kor_noun'] != '[]')]
contents_fin = contents_fin.reset_index(drop=True)

#timetail = oaislib.fn_get_timetail()
#outputfilename = 'output/contents_fin_' + timetail + '.xlsx'
#contents_fin.to_excel(outputfilename)
#contents_fin.to_pickle('output/contents_fin.pickle')

##ps insert tag
print("insert word to anal_word table ")

db = oaislib.fn_lab_db_connect()

try:
    with db.cursor() as cursor:
        # insert data using for
        for i in range(len(contents_df)):
            print(str(i) + "/" + str(len(contents_df)))

            video_id_str = contents_df['video_id'].iloc[i]
            youtube_id_str = contents_df['provi_video_id'].iloc[i]
            title_org_str = oaislib.fn_get_text_ko(contents_df['title'].iloc[i])
            keytag_org_str = oaislib.fn_get_text_ko(contents_df['video_key_tag'].iloc[i])
            tag_org_str = oaislib.fn_get_text_ko(contents_df['tag_contents'].iloc[i])
            title_word_ko_str = contents_df['title_kor_noun'].iloc[i]
            keytag_word_ko_str = contents_df['key_tag_kor_noun'].iloc[i]
            tag_word_ko_str = contents_df['tag_kor_noun'].iloc[i]

            sql = f'delete from anal_word where video_id ="{video_id_str}"'            
            cursor.execute(sql)
            db.commit()
            
            sql = 'insert into anal_word (video_id, youtube_id, title_org, keytag_org, TAG_ORG, title_word_ko, KEYTAG_WORD_KO, TAG_WORD_KO,INSERT_DATE) VALUES ( "{}" , "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(video_id_str, youtube_id_str, title_org_str, keytag_org_str, tag_org_str, title_word_ko_str, keytag_word_ko_str, tag_word_ko_str, date_str)
            #print(sql)
            cursor.execute(sql)
        db.commit()

        #check update error
        sql_check = "select count(0) from anal_word"
        cursor.execute(sql_check)
        result = cursor.fetchall()
        if len(contents_df) == result:
            print('upload OK')
finally:
    db.close()

print('ps01-11_cal_video_sim_preprocess_with_word.py finish')
print("time :", time.time() - start)

