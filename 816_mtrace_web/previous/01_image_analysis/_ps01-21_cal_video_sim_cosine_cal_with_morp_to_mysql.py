# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200211
# goal : 비디오 별 전처리한 형태소 정보를 바탕으로 코사인 유사도 분석 수행
#
# desc : 각 videdo 별로 유사도가 구해지면, DB에서 해당 video_id에 대한 유사도 정보를 전부 삭제하고
# desc : 새로 구해진 정보를 업데이트함 
# desc : 이 버전에서는 문장 간 유사도를 하나씩 비교하기 때문에 속도가 느림
# desc : 결과를 ananl_video_similarity_with_morp에 저장
# desc : 
# desc : 
#
# prss : 
# prss : 
# prss : 
# prss : 
# prss : 
# prss : 

# note
# 20

import os
import shutil
import time
import re
import pandas as pd
import numpy as np
if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
import pymysql
from datetime import datetime
start = time.time()
now = datetime.now()
date_str = str(now.year)+"-"+str(now.month)+"-"+str(now.day)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

##ps parameter 
num_sim_sentences = 20


##ps_data loading(anal_morp)
db = oaislib.fn_lab_db_connect()
try:
    with db.cursor() as cursor:
        sql_load_anal_morp = ("SELECT VIDEO_ID, YOUTUBE_ID, TITLE_MORP_KO, "  
                             "KEYTAG_MORP_KO, TAG_MORP_KO FROM ANAL_MORP")
        cursor.execute(sql_load_anal_morp)
        cursor_anal_morp_tbl = cursor.fetchall()
        morp_df = pd.DataFrame(list(cursor_anal_morp_tbl),
                               columns=['videoid', 'youtubeid',
                                        'title_morp_ko', 'keytag_morp_ko', 'tag_morp_ko'])
finally:
    db.close()


num_sentence = len(morp_df)    

for i in range(num_sentence):
    morp_df['title_morp_ko'].iloc[i] = oaislib.fn_get_text_ko(morp_df['title_morp_ko'].iloc[i])
    morp_df['keytag_morp_ko'].iloc[i] = oaislib.fn_get_text_ko(morp_df['keytag_morp_ko'].iloc[i])
    morp_df['tag_morp_ko'].iloc[i] = oaislib.fn_get_text_ko(morp_df['tag_morp_ko'].iloc[i])

##ps vectorize
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_title = tfidf_vectorizer.fit_transform(morp_df['title_morp_ko'])
tfidf_matrix_keytag = tfidf_vectorizer.fit_transform(morp_df['keytag_morp_ko'])
tfidf_matrix_tag = tfidf_vectorizer.fit_transform(morp_df['tag_morp_ko'])

##ps calculate cosine similarity

## 결과 벡터 생성
rlt_df = pd.DataFrame(index=range(num_sentence * num_sim_sentences),
                      columns=['videoid1', 'youtubeid1','title1',
                               'videoid2', 'youtubeid2','title2',
                               'rank', 'sim'])

idx_total = -1

## 각 문장 별로 유사도가 높은 N개 이내의 유사문장 벡터를 받음
## 타이틀, 키태그 태그 종류에 대해서 수행하며, 별도가 아니라 동시에 수행해서
## 유사도를 별도로 계산 후에 점수가 높은 문장을 찾아야 함.
## 또한 태그에 공백이 있으면 연산에 에러가 발생할 수 있으니 체크해서 공백에 대해서는 유사도를 0으로 설정하도록 함


for i in range(num_sentence):
    print(str(i) + '/' + str(num_sentence))
    idx1 = morp_df['videoid'].iloc[i]
    sub_rlt_df = pd.DataFrame(index=range(num_sentence),
                              columns=['videoid1', 'youtubeid1',
                                       'videoid2', 'youtubeid2',
                                       'rank', 'sim'])

    idx_sub = -1
    ##하나의 문장에 대해서 다른 모든 문장의 유사도를 구함
    for j in range(num_sentence):
        if i != j:
            idx2 = morp_df['videoid'].iloc[j]

            rlt_title = cosine_similarity(tfidf_matrix_title[i:(i+1)], tfidf_matrix_title[j:(j+1)])
            rlt_keytag = cosine_similarity(tfidf_matrix_keytag[i:(i+1)], tfidf_matrix_keytag[j:(j+1)])
            rlt_tag = cosine_similarity(tfidf_matrix_tag[i:(i+1)], tfidf_matrix_tag[j:(j+1)])

            rlt = 0.2 * rlt_title[0][0] + 0.3 * rlt_keytag[0][0] + 0.5 * rlt_tag[0][0]
            
            if rlt > 0.2:
                youtubeid1 = morp_df[morp_df['videoid'] == idx1]['youtubeid'].iloc[0]
                youtubeid2 = morp_df[morp_df['videoid'] == idx2]['youtubeid'].iloc[0]       

                if youtubeid1 != youtubeid2:
                    print(str(j) + '/' + str(num_sentence) + ' ' + youtubeid1 + ' ' + youtubeid2 + ' '
                          +  str(rlt))
                    
                    idx_sub += 1
                    sub_rlt_df['videoid1'].iloc[idx_sub] = idx1
                    sub_rlt_df['youtubeid1'].iloc[idx_sub] = youtubeid1
                    sub_rlt_df['videoid2'].iloc[idx_sub] = idx2
                    sub_rlt_df['youtubeid2'].iloc[idx_sub] = youtubeid2
                    sub_rlt_df['sim'].iloc[idx_sub] = rlt


    if idx_sub > 0:
        sub_rlt_df = sub_rlt_df[:(idx_sub+1)]
        sub_rlt_df.sort_values(by=['sim'], axis=0, ascending=False, inplace=True)
        num_sub = len(sub_rlt_df)
        for j in range(num_sub):
            sub_rlt_df['rank'].iloc[j] = j+1

        ## 정해진 갯수 이내의 유사도만 DB insert
        num_insert_row = min(num_sub, num_sim_sentences)
        sub_rlt_df = sub_rlt_df[:num_insert_row]


        ## DB insert
        db = oaislib.fn_lab_db_connect()

        try:
            with db.cursor() as cursor:
                ## 테이블에서 video_id1에 대해서 기존 데이터 삭제
                sql_del_sim = 'delete from ANAL_VIDEO_SIMILARITY_WITH_MORP  where VIDEO_ID1 = "' + idx1 + '"'
                cursor.execute(sql_del_sim)
                db.commit()
                # insert data using for
                for k in range(len(sub_rlt_df)):
                    videoid1_str = sub_rlt_df['videoid1'].iloc[k]
                    youtubeid1_str = sub_rlt_df['youtubeid1'].iloc[k]
                    videoid2_str = sub_rlt_df['videoid2'].iloc[k]
                    youtubeid2_str = sub_rlt_df['youtubeid2'].iloc[k]
                    rank_str = sub_rlt_df['rank'].iloc[k]
                    sim_str = sub_rlt_df['sim'].iloc[k]
                    
                    sql_insert = ('insert into ANAL_VIDEO_SIMILARITY_WITH_MORP '
                                  '(VIDEO_ID1, YOUTUBE_ID1, VIDEO_ID2, YOUTUBE_ID2, RANK, SIM, INSERT_DATE) '
                                  'VALUES ("{}" , "{}", "{}", "{}", "{}", "{}", "{}")'
                                  .format(videoid1_str, youtubeid1_str, videoid2_str, youtubeid2_str,
                                  rank_str, sim_str, date_str))
                    #print(sql)
                    cursor.execute(sql_insert)
                db.commit()
        finally:
            db.close()

print("time :", time.time() - start)
