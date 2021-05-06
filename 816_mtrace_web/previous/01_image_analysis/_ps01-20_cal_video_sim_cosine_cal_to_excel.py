# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200211
# goal : 비디오 별 전처리한 형태소 정보를 바탕으로 코사인 유사도 분석 수행
#
# desc : 각 videdo 별로 유사도가 구해지면, DB에서 해당 video_id에 대한 유사도 정보를 전부 삭제하고
# desc : 새로 구해진 정보를 업데이트함 
# desc : 
# desc : 
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
start = time.time()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

##ps parameter 
num_sim_sentences = 20


##ps_data loading(anal_morp)
db = oaislib.fn_lab_db_connect()
try:
    with db.cursor() as cursor:
        sql_load_anal_morp = ("SELECT VIDEO_ID, YOUTUBE_ID, TITLE_MORP_KO, "  
                             "KEYTAG_MORP_KO, TAG_MORP_KO FROM anal_morp")
        cursor.execute(sql_load_anal_morp)
        cursor_anal_morp_tbl = cursor.fetchall()
        morp_df = pd.DataFrame(list(cursor_anal_morp_tbl),
                               columns=['videoid', 'youtubeid',
                                        'title_morp_ko', 'keytag_morp_ko', 'tag_morp_ko'])
finally:
    db.close()


num_sentence = len(morp_df)    

##ps vectorize
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix_title = tfidf_vectorizer.fit_transform(morp_df['title_morp_ko'])
tfidf_matrix_keytag = tfidf_vectorizer.fit_transform(morp_df['keytag_morp_ko'])
tfidf_matrix_tag = tfidf_vectorizer.fit_transform(morp_df['tag_morp_ko'])

##ps calculate cosine similarity

## 결과 벡터 생성
rlt_df = pd.DataFrame(index=range(num_sentence * num_sim_sentences),
                      columns = ['videoid1', 'youtubeid1','title1',
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
                              columns = ['videoid1', 'youtubeid1',
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
                    print(youtubeid1 + ' ' + youtubeid2 + ' ' +  str(rlt))
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


        for j in range(num_sub):
            idx_total += 1
            rlt_df['videoid1'].iloc[idx_total] = sub_rlt_df['videoid1'].iloc[j]
            rlt_df['youtubeid1'].iloc[idx_total] = sub_rlt_df['youtubeid1'].iloc[j]
            rlt_df['videoid2'].iloc[idx_total] = sub_rlt_df['videoid2'].iloc[j]
            rlt_df['youtubeid2'].iloc[idx_total] = sub_rlt_df['youtubeid2'].iloc[j]
            rlt_df['rank'].iloc[idx_total] = sub_rlt_df['rank'].iloc[j]
            rlt_df['sim'].iloc[idx_total] = sub_rlt_df['sim'].iloc[j]

rlt_df = rlt_df[:idx_total+1]
rlt_df.to_excel('output/sentence_cosine_similarity02.xlsx')



breakpoint()
print("time :", time.time() - start)
