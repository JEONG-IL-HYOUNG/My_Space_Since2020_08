# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200825
# goal : 유사도 테이블에 tag 유사도 삽입
#
# desc : 기존에 생성한 영상기반 유사도에 태그기반 유사도를 삽입
# desc : 현재 실시간으로 태그기반 유사도를 계산하는 부분을 사전 계산함
# desc :
# desc : input
# desc : anal_search_same_video :: videoid1, videoid2, tag_sim
# desc : anal_video_similarity_with_morp :: video_id1, video_id2, sim
# desc : 
#
# prss : 1. anal_video_similarity_with_morp download
# prss : 2. anal_search_same_video download
# prss : 3. anal_search_same_video의 video_id1, video_id2을 조건으로
# prss : 4  anal_video_similarity_with_morp에서 sim을 찾음
# prss : 5. sim값을 anal_search_same_video의 tag_sim에 업데이트
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

## data loading
sql_str = 'select videoid1, videoid2, tag_sim from anal_search_same_video'
same_df = oaislib.fn_get_df_from_lab_db(sql_str)
same_df.columns = map(str.lower, same_df.columns)
same_cnt = len(same_df)

sql_str = 'select video_id1, video_id2, sim from anal_video_similarity_with_morp'
morp_df = oaislib.fn_get_df_from_lab_db(sql_str)
morp_df.columns = map(str.lower, morp_df.columns)


## search tag_sim
conn = oaislib.fn_connect_lab_db()
try:
    # INSERT
    with conn.cursor() as curs:
        for i in range(same_cnt):
            print(str(i) + '/' + str(same_cnt))
            vid01 = same_df['videoid1'].iloc[i]
            vid02 = same_df['videoid2'].iloc[i]
            tag_sim_df = morp_df['sim'][(morp_df['video_id1']== vid01) & (morp_df['video_id2']== vid02)] 
            if len(tag_sim_df) == 0:
                tag_sim = 0
            else:
                tag_sim = tag_sim_df.values[0]
            sql_str = f"update anal_search_same_video set tag_sim = '{tag_sim}' where videoid1 = '{vid01}' and videoid2 = '{vid02}'"
            curs.execute(sql_str)
        conn.commit()
finally:
    conn.close()

print("time :", time.time() - start)
breakpoint()
