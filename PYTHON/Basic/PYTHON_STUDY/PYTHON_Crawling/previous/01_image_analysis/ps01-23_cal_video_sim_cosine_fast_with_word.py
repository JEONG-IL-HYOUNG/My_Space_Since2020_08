# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200602
# goal : 형태소 분석을 행렬 계산을 통해서 고속화함
#
# desc : 각 videdo 별로 유사도가 구해지면, DB에서 해당 video_id에 대한 유사도 정보를 전부 삭제하고
# desc : 새로 구해진 정보를 업데이트함 
# desc : 이전 버전의 문장 유사도를 1:1로 진행해서 느린 속도 문제를 1:N의 행렬계산으로 고속화 함
# desc : 
# desc : 
# desc : 
#
# prss : 01. parameter 
# prss : 02. data loading(anal_word)
# prss : 03. vectorize
# prss : 04. calculate cosine similarity
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
import sys
start = time.time()
now = datetime.now()
date_str = str(now.year)+"-"+str(now.month)+"-"+str(now.day)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

##ps parameter 
num_sim_sentences = 20

print('ps01-23_cal_video_sim_cosine_fast_with_word.py start')
##ps_data loading(anal_word)

#db = pymysql.connect(host='192.168.0.58',
#                     port=3306, user='oaiskoo', passwd='u4i3o2p1',
#                     db='labmstuv', charset='utf8')
db = oaislib.fn_lab_db_connect()

try:
    with db.cursor() as cursor:
        sql_select_anal_word = ("SELECT VIDEO_ID, YOUTUBE_ID, TITLE_ORG, TITLE_WORD_KO, "  
                             "KEYTAG_WORD_KO, TAG_WORD_KO FROM anal_word")
        cursor.execute(sql_select_anal_word)
        cursor_anal_word_tbl = cursor.fetchall()
        word_df = pd.DataFrame(list(cursor_anal_word_tbl),
                               columns=['video_id', 'youtubeid','title',
                                        'title_word_ko', 'keytag_word_ko', 'tag_word_ko'])
finally:
    db.close()


num_sentence = len(word_df)    

for i in range(num_sentence):
    word_df['title_word_ko'].iloc[i] = oaislib.fn_get_text_ko(word_df['title_word_ko'].iloc[i])
    word_df['keytag_word_ko'].iloc[i] = oaislib.fn_get_text_ko(word_df['keytag_word_ko'].iloc[i])
    word_df['tag_word_ko'].iloc[i] = oaislib.fn_get_text_ko(word_df['tag_word_ko'].iloc[i])

##ps vectorize
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_title = tfidf_vectorizer.fit_transform(word_df['title_word_ko'])
tfidf_matrix_keytag = tfidf_vectorizer.fit_transform(word_df['keytag_word_ko'])
tfidf_matrix_tag = tfidf_vectorizer.fit_transform(word_df['tag_word_ko'])

##ps calculate cosine similarity

## 결과 벡터 생성

## 각 문장 별로 유사도가 높은 N개 이내의 유사문장 벡터를 받음
## 타이틀, 키태그 태그 종류에 대해서 수행하며, 별도가 아니라 동시에 수행해서
## 유사도를 별도로 계산 후에 점수가 높은 문장을 찾아야 함.
## 또한 태그에 공백이 있으면 연산에 에러가 발생할 수 있으니 체크해서 공백에 대해서는 유사도를 0으로 설정하도록 함

for i in range(num_sentence):
    print(str(i) + '/' + str(num_sentence))
    video_id01 = word_df['video_id'].iloc[i]
    youtube_id01 = word_df['youtubeid'].iloc[i]
    title01 = word_df['title'].iloc[i]

    rlt_title = cosine_similarity(tfidf_matrix_title[i:(i+1)], tfidf_matrix_title)
    rlt_keytag = cosine_similarity(tfidf_matrix_keytag[i:(i+1)], tfidf_matrix_keytag)
    rlt_tag = cosine_similarity(tfidf_matrix_tag[i:(i+1)], tfidf_matrix_tag)

    ## 위의 실행 결과에서 한 문장에 대해서 다른 전체 문장과의 유사도가 계산되었으며,
    ## 자기 자신을 포함한 결과가 나옴
    ## 결과가 ndarray(인덱스가 없음)로 나와서 이를 인덱스를 붙인 df로 변환 후 소팅을 하고
    ## 조건 내의 결과를 가지고 옴

    ## 위의 것을 하기 위해서 위의 코사인 유사도가 전체 입력문장 개수만큼 나왔다는 보장이 필요함
    ## 검증용으로 아래를 수행
    if rlt_title.shape[1] != num_sentence:
        sys.exit('length of title is not same as that of sentence')
    if rlt_keytag.shape[1] != num_sentence:
        sys.exit('length of keytag is not same as that of sentence')
    if rlt_tag.shape[1] != num_sentence:
        sys.exit('length of tag is not same as that of sentence')

    ## title에 대한 코사인 유사도 
    rlt_title_df = pd.DataFrame(data = rlt_title[0].tolist(), index= range(num_sentence),
                                columns = ['v1'])

    ## keytag에 대한 코사인 유사도 
    rlt_keytag_df = pd.DataFrame(data = rlt_keytag[0].tolist(), index= range(num_sentence),
                                columns = ['v1'])
    
    ## tag에 대한 코사인 유사도 
    rlt_tag_df = pd.DataFrame(data = rlt_tag[0].tolist(), index= range(num_sentence),
                                columns = ['v1'])

    ## 유사도 합
    rlt_cosine_df = 0.5 * rlt_title_df + 0.3 * rlt_keytag_df + 0.2 * rlt_tag_df

    ##유사도 높은 순 정렬 
    rlt_cosine_df.sort_values(by=['v1'], inplace=True, ascending=False)
    rlt_cosine_df = rlt_cosine_df[rlt_cosine_df['v1'] > 0]

    ## 동영상 별 유사 동영상 계산
    rlt_cosine_count = len(rlt_cosine_df)
    
    if rlt_cosine_count > 0:
        num_sim = min(rlt_cosine_count, num_sim_sentences)

        rlt_df = pd.DataFrame(index=range(num_sim),
                      columns = ['video_id01', 'youtube_id01','title01',
                                 'video_id02', 'youtube_id02','title02',
                                 'rank', 'sim'])
        idx_total = -1
        idx_rank = 0
        for k in range(num_sim):
            rlt_index = rlt_cosine_df.index[k]
            sim_value = rlt_cosine_df['v1'].iloc[k]
            video_id02 = word_df['video_id'].iloc[rlt_index]
            youtube_id02 = word_df['youtubeid'].iloc[rlt_index]
            title02 = word_df['title'].iloc[rlt_index]

            if video_id01 != video_id02:
                idx_total += 1
                idx_rank += 1
                rlt_df['video_id01'].iloc[idx_total] = video_id01
                rlt_df['youtube_id01'].iloc[idx_total] = youtube_id01
                rlt_df['video_id02'].iloc[idx_total] = video_id02
                rlt_df['youtube_id02'].iloc[idx_total] = youtube_id02
                rlt_df['title01'].iloc[idx_total] = title01
                rlt_df['title02'].iloc[idx_total] = title02
                rlt_df['rank'].iloc[idx_total] = idx_rank
                rlt_df['sim'].iloc[idx_total] = sim_value
                #print(video_id01 + ' and ' + video_id02 + ' sim : ' + str(sim_value))
                
        rlt_df= rlt_df[:idx_total]
                
        ## DB insert
        db = oaislib.fn_lab_db_connect()
        try:
            with db.cursor() as cursor:
                ## 테이블에서 video_id1에 대해서 기존 데이터 삭제
                sql_del_sim = 'delete from ANAL_VIDEO_SIMILARITY_WITH_WORD where VIDEO_ID1 = "' + video_id01 + '"'
                cursor.execute(sql_del_sim)
                #db.commit()
                
                # insert data using for
                for k in range(len(rlt_df)):
                    video_id01_str = rlt_df['video_id01'].iloc[k]
                    youtube_id01_str = rlt_df['youtube_id01'].iloc[k]
                    video_id02_str = rlt_df['video_id02'].iloc[k]
                    youtube_id02_str = rlt_df['youtube_id02'].iloc[k]
                    rank_str = rlt_df['rank'].iloc[k]
                    sim_str = rlt_df['sim'].iloc[k]

                    if video_id01 != video_id02:
                        sql_insert = ('insert into ANAL_VIDEO_SIMILARITY_WITH_WORD '
                                      '(VIDEO_ID1, YOUTUBE_ID1, VIDEO_ID2, YOUTUBE_ID2, RANK, SIM, INSERT_DATE) '
                                      'VALUES ("{}" , "{}", "{}", "{}", "{}", "{}", "{}")'
                                      .format(video_id01_str, youtube_id01_str, video_id02_str, youtube_id02_str,
                                              rank_str, sim_str, date_str))
                    #print(sql)
                    cursor.execute(sql_insert)
                db.commit()
        finally:
            db.close()

print('ps01-23_cal_video_sim_cosine_fast_with_word.py finish')            
print("time :", time.time() - start)
