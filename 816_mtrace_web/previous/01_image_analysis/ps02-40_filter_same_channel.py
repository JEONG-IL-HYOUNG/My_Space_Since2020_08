# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200813
# goal : 동일 유튜브 채널의 유사 비디오를 제외함 
#
# desc : 
# desc : 
# desc : 
# desc : 
# desc : 
# desc : 
#
# prss : 1.video 테이블 로딩
# prss : 2.anal_search_same_video 로딩
# prss : 3.videoid1의 채널 확인
# prss : 4.videoid2의 채널 확인
# prss : - 값이 같으면 컬럼값 n이고 값이 다르면 y
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
start = time.time()

### main
## tbl loading
sql_str = 'select VIDEO_ID, PROVI_VIDEO_ID,CHANNEL_ID,channel_title from video_syc where CON_PROVIDER_ID = "Youtube"'
video_df = oaislib.fn_get_df_from_lab_db(sql_str)
video_df.columns = ['video_id', 'youtube_id', 'channel_id','channel_title']

sql_str = 'select videoid1, videoid2 from anal_search_same_video'
vid_df = oaislib.fn_get_df_from_lab_db(sql_str)
vid_df.columns = ['vid01', 'vid02']
vid_df['cid01'] = ""
vid_df['cid02'] = ""
vid_df['cnm01'] = ""
vid_df['cnm02'] = ""
vid_df['same'] = ""

## compare youtube id
for i in range(len(vid_df)):
    vid01 = vid_df['vid01'].iloc[i]
    vid02 = vid_df['vid02'].iloc[i]
    cid01 = video_df[video_df['video_id'] == vid01]['channel_id']
    cid02 = video_df[video_df['video_id'] == vid02]['channel_id']
    cnm01 = video_df[video_df['video_id'] == vid01]['channel_title']
    cnm02 = video_df[video_df['video_id'] == vid02]['channel_title']
    
    if len(cid01) == 1:
        if len(cid02) == 1:
            cid01 = cid01.values[0]
            cid02 = cid02.values[0]
            cnm01 = cnm01.values[0]
            cnm02 = cnm02.values[0]
            vid_df['cid01'].iloc[i] = cid01
            vid_df['cid02'].iloc[i] = cid02
            vid_df['cnm01'].iloc[i] = cnm01
            vid_df['cnm02'].iloc[i] = cnm02
            
            if cid01 == cid02:
                vid_df['same'].iloc[i] = 'y'
            else:
                vid_df['same'].iloc[i] = 'n'
        else:
            vid_df['same'].iloc[i] = 'n' #채널이름이 없으면 다른걸 침
    else:
        vid_df['same'].iloc[i] = 'n' #채널이름이 없으면 다른걸로 침

## update DB
db = oaislib.fn_connect_lab_db()
try:
    with db.cursor() as cursor:
        for i in range(len(vid_df)):
            vid01 = vid_df['vid01'].iloc[i]
            vid02 = vid_df['vid02'].iloc[i]
            cnm01 = vid_df['cnm01'].iloc[i]
            cnm02 = vid_df['cnm02'].iloc[i]
            same_str = vid_df['same'].iloc[i]
            sql_str = f'update anal_search_same_video set channel_same = "{same_str}", ch_nm1 = "{cnm01}", ch_nm2 = "{cnm02}" where videoid1 = "{vid01}" and videoid2 = "{vid02}"'
            cursor.execute(sql_str)
        db.commit()
finally:
    db.close()

print("time :", time.time() - start)
#breakpoint()
    
