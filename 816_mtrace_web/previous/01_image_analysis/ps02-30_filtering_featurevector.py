# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200811
# goal : 기존의 특징벡터에서 의미없는 구간을 필터링함
#
# desc : 기존 분석 결과를 하나씩 검사해서 사용할거면 y 아니면 n를 use_yn 컬럼에 표기
# desc : 
# desc : 
# desc : 
# desc : 
# desc : 
#
# prss : 1. anal_search_same_video에서 video_id를 가지고 옴
# prss : 2. feature vector 데이터를 가지고 옴
# prss : 3. rgb의 메디안 - hmd, smd  vmd의 meidan이 0,0,100와의 abs가 10이하면 
# prss : 4. rgb의 표준편차 - hsd, ssd, vsd의 메디안이 0,0,0과의 abs가 10이하이면 
# prss : 5. use_yn <- n
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
import numpy as np
start = time.time()

## function

def check_color_val(md_df, sd_df,ssec,esec):
    md_df.columns = ['h','s','v']
    sd_df.columns = ['h','s','v']

    r_md = md_df['h'].values[0]
    r_md = oaislib.fn_get_number(r_md).split(' ')
    r_md = oaislib.fn_change_element_in_list_to_int(r_md)
    r_md = r_md[ssec:esec]
    
    g_md = md_df['s'].values[0]
    g_md = oaislib.fn_get_number(g_md).split(' ')
    g_md = oaislib.fn_change_element_in_list_to_int(g_md)
    g_md = g_md[ssec:esec]
    
    b_md = md_df['v'].values[0]
    b_md = oaislib.fn_get_number(b_md).split(' ')
    b_md = oaislib.fn_change_element_in_list_to_int(b_md)
    b_md = b_md[ssec:esec]
    
    r_sd = sd_df['h'].values[0]
    r_sd = oaislib.fn_get_number(r_sd).split(' ')    
    r_sd = oaislib.fn_change_element_in_list_to_int(r_sd)
    r_sd = r_sd[ssec:esec]
    
    g_sd = sd_df['s'].values[0]
    g_sd = oaislib.fn_get_number(g_sd).split(' ')    
    g_sd = oaislib.fn_change_element_in_list_to_int(g_sd)
    g_sd = g_sd[ssec:esec]
    
    b_sd = sd_df['v'].values[0]
    b_sd = oaislib.fn_get_number(b_sd).split(' ')
    b_sd = oaislib.fn_change_element_in_list_to_int(b_sd)
    b_sd = b_sd[ssec:esec]
    
    rlt = 0
    r_md_mn = np.mean(r_md)
    g_md_mn = np.mean(g_md)
    b_md_mn = np.mean(b_md)

    r_sd_mn = np.mean(r_sd)
    g_sd_mn = np.mean(g_sd)
    b_sd_mn = np.mean(b_sd)
    


    
    if abs(r_md_mn) < 50:
        if abs(g_md_mn) < 50:
            if abs(r_md_mn) < 50:
                if abs(r_sd_mn) < 20:
                    if abs(g_sd_mn) < 20:
                        if abs(r_sd_mn) < 20:
                            rlt = 1

    if abs(r_md_mn) > 220:
        if abs(g_md_mn) > 220 :
            if abs(r_md_mn) > 220:
                if abs(r_sd_mn) < 20:
                    if abs(g_sd_mn) < 20:
                        if abs(r_sd_mn) < 20:
                            rlt = 1
    if rlt == 1:
        print('filtered')
    return rlt

## prss : 1. anal_search_same_video에서 video_id를 가지고 옴
sql_str = "select videoid1, v1_start_time, v1_end_time from anal_search_same_video " #where use_yn = ''  
vids_df = oaislib.fn_get_df_from_lab_db(sql_str)
vid_cnt = len(vids_df)

for i in range(vid_cnt):
    print( str(i) + '/' + str(vid_cnt))

    vid = vids_df['videoid1'].iloc[i]
    ssec = vids_df['v1_start_time'].iloc[i]
    esec = vids_df['v1_end_time'].iloc[i]
    vid == '0DC9F1AB-C1A2-4FA7-A87F-18122A4342AF'
    ssec = 23
    esec = 36
    
    sql_str = f'select r_md, g_md, b_md from anal_video_rgb_md where video_id = "{vid}"'
    md_df = oaislib.fn_get_df_from_lab_db(sql_str)
    
    sql_str = f'select r_sd, g_sd, b_sd from anal_video_rgb_sd where video_id = "{vid}"'
    sd_df = oaislib.fn_get_df_from_lab_db(sql_str)

    rlt = check_color_val(md_df, sd_df, ssec, esec)

    if rlt == 0:
        sql_str = f"update anal_search_same_video set use_yn = 'y' where videoid1 = '{vid}'"
        oaislib.fn_run_sql_to_lab_db(sql_str)
    else:
        sql_str = f"update anal_search_same_video set use_yn = 'n' where videoid1 = '{vid}'"
        oaislib.fn_run_sql_to_lab_db(sql_str)

print("time :", time.time() - start)
#breakpoint()
