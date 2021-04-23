# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200616
# goal : 로컬비디오를 대상으로 유사구간을 검색하는 기능 개발 
#
# desc : 
# desc : 
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
start = time.time()
date_str = oaislib.fn_get_date_str()

import pymysql

def compare_img_frame(hmn01, smn01, vmn01, hmd01, smd01, vmd01, hsd01, ssd01, vsd01,
                      rmn01, gmn01, bmn01, rmd01, gmd01, bmd01, rsd01, gsd01, bsd01,
                      hmn02, smn02, vmn02, hmd02, smd02, vmd02, hsd02, ssd02, vsd02,
                      rmn02, gmn02, bmn02, rmd02, gmd02, bmd02, rsd02, gsd02, bsd02):

    hmn_diff = abs(hmn01 - hmn02)/180
    smn_diff = abs(smn01 - smn02)/255
    vmn_diff = abs(vmn01 - vmn02)/255
    hmd_diff = abs(hmd01 - hmd02)/180
    smd_diff = abs(smd01 - smd02)/255
    vmd_diff = abs(vmd01 - vmd02)/255
    hsd_diff = abs(hsd01 - hsd02)/180
    ssd_diff = abs(ssd01 - ssd02)/255
    vsd_diff = abs(vsd01 - vsd02)/255
    rmn_diff = abs(rmn01 - rmn02)/180
    gmn_diff = abs(gmn01 - gmn02)/255
    bmn_diff = abs(bmn01 - bmn02)/255
    rmd_diff = abs(rmd01 - rmd02)/180
    gmd_diff = abs(gmd01 - gmd02)/255
    bmd_diff = abs(bmd01 - bmd02)/255
    rsd_diff = abs(rsd01 - rsd02)/180
    gsd_diff = abs(gsd01 - gsd02)/255
    bsd_diff = abs(bsd01 - bsd02)/255
    
    val_diff = (hmn_diff + smn_diff + vmn_diff + hmd_diff + smd_diff + vmd_diff +
                hsd_diff + ssd_diff + vsd_diff + rmn_diff + gmn_diff + bmn_diff + 
                rmd_diff + gmd_diff + bmd_diff + rsd_diff + gsd_diff + bsd_diff)/18

    return val_diff

def get_colorfeature():
    sql_colorfeature = 'select video_id from anal_local_video_colorfeature where success = "yes"'
    colorfeature_df = oaislib.fn_get_df_from_lab_db(sql_colorfeature)

    sql_hsv_mn = 'select video_id, h_mn, s_mn, v_mn from anal_local_video_hsv_mn'
    hsv_mn_df = oaislib.fn_get_df_from_lab_db(sql_hsv_mn)

    sql_hsv_md = 'select video_id, h_md, s_md, v_md from anal_local_video_hsv_md'
    hsv_md_df = oaislib.fn_get_df_from_lab_db(sql_hsv_md)

    sql_hsv_sd = 'select video_id, h_sd, s_sd, v_sd from anal_local_video_hsv_sd'
    hsv_sd_df = oaislib.fn_get_df_from_lab_db(sql_hsv_sd)

    sql_rgb_mn = 'select video_id, r_mn, g_mn, b_mn from anal_local_video_rgb_mn'
    rgb_mn_df = oaislib.fn_get_df_from_lab_db(sql_rgb_mn)

    sql_rgb_md = 'select video_id, r_md, g_md, b_md from anal_local_video_rgb_md'
    rgb_md_df = oaislib.fn_get_df_from_lab_db(sql_rgb_md)

    sql_rgb_sd = 'select video_id, r_sd, g_sd, b_sd from anal_local_video_rgb_sd'
    rgb_sd_df = oaislib.fn_get_df_from_lab_db(sql_rgb_sd)

    rlt_df = pd.merge(colorfeature_df, hsv_mn_df, how='left', on='video_id')
    rlt_df = pd.merge(rlt_df, hsv_md_df, how='left', on='video_id')
    rlt_df = pd.merge(rlt_df, hsv_sd_df, how='left', on='video_id')
    rlt_df = pd.merge(rlt_df, rgb_mn_df, how='left', on='video_id')
    rlt_df = pd.merge(rlt_df, rgb_md_df, how='left', on='video_id')
    rlt_df = pd.merge(rlt_df, rgb_sd_df, how='left', on='video_id')
            
    return rlt_df

def trans_str_to_num(sentences):
    for i in range(len(sentences)):
        num_str =  oaislib.fn_get_number(sentences[i])
        num_str = num_str.split(' ')
        num_list = [float(i) for i in num_str]
        sentences[i] = num_list
    return sentences

def trans_str_to_num_for_df(input_df):
    input_df['h_mn'] = trans_str_to_num(input_df['h_mn'])
    input_df['s_mn'] = trans_str_to_num(input_df['s_mn'])
    input_df['v_mn'] = trans_str_to_num(input_df['v_mn'])
    input_df['h_md'] = trans_str_to_num(input_df['h_md'])
    input_df['s_md'] = trans_str_to_num(input_df['s_md'])
    input_df['v_md'] = trans_str_to_num(input_df['v_md'])
    input_df['h_sd'] = trans_str_to_num(input_df['h_sd'])
    input_df['s_sd'] = trans_str_to_num(input_df['s_sd'])
    input_df['v_sd'] = trans_str_to_num(input_df['v_sd'])
    input_df['r_mn'] = trans_str_to_num(input_df['r_mn'])
    input_df['g_mn'] = trans_str_to_num(input_df['g_mn'])
    input_df['b_mn'] = trans_str_to_num(input_df['b_mn'])
    input_df['r_md'] = trans_str_to_num(input_df['r_md'])
    input_df['g_md'] = trans_str_to_num(input_df['g_md'])
    input_df['b_md'] = trans_str_to_num(input_df['b_md'])
    input_df['r_sd'] = trans_str_to_num(input_df['r_sd'])
    input_df['g_sd'] = trans_str_to_num(input_df['g_sd'])
    input_df['b_sd'] = trans_str_to_num(input_df['b_sd'])

    return input_df


def search_same_clip(colorfeatuere_df,insert_df, i, j,para_duration, para_diff):

    videoid1 = colorfeature_df['video_id'].iloc[i]
    h_mn_01_lst = colorfeature_df['h_mn'].iloc[i]
    s_mn_01_lst = colorfeature_df['s_mn'].iloc[i]
    v_mn_01_lst = colorfeature_df['v_mn'].iloc[i]
    h_md_01_lst = colorfeature_df['h_md'].iloc[i]
    s_md_01_lst = colorfeature_df['s_md'].iloc[i]
    v_md_01_lst = colorfeature_df['v_mn'].iloc[i]
    h_sd_01_lst = colorfeature_df['h_sd'].iloc[i]
    s_sd_01_lst = colorfeature_df['s_sd'].iloc[i]
    v_sd_01_lst = colorfeature_df['v_sd'].iloc[i]
    r_mn_01_lst = colorfeature_df['r_mn'].iloc[i]
    g_mn_01_lst = colorfeature_df['g_mn'].iloc[i]
    b_mn_01_lst = colorfeature_df['b_mn'].iloc[i]
    r_md_01_lst = colorfeature_df['r_md'].iloc[i]
    g_md_01_lst = colorfeature_df['g_md'].iloc[i]
    b_md_01_lst = colorfeature_df['b_mn'].iloc[i]
    r_sd_01_lst = colorfeature_df['r_sd'].iloc[i]
    g_sd_01_lst = colorfeature_df['g_sd'].iloc[i]
    b_sd_01_lst = colorfeature_df['b_sd'].iloc[i]

    len_video01 = len(h_mn_01_lst)

    videoid2 = colorfeature_df['video_id'].iloc[j]
    h_mn_02_lst = colorfeature_df['h_mn'].iloc[j]
    s_mn_02_lst = colorfeature_df['s_mn'].iloc[j]
    v_mn_02_lst = colorfeature_df['v_mn'].iloc[j]
    h_md_02_lst = colorfeature_df['h_md'].iloc[j]
    s_md_02_lst = colorfeature_df['s_md'].iloc[j]
    v_md_02_lst = colorfeature_df['v_mn'].iloc[j]
    h_sd_02_lst = colorfeature_df['h_sd'].iloc[j]
    s_sd_02_lst = colorfeature_df['s_sd'].iloc[j]
    v_sd_02_lst = colorfeature_df['v_sd'].iloc[j]
    r_mn_02_lst = colorfeature_df['r_mn'].iloc[j]
    g_mn_02_lst = colorfeature_df['g_mn'].iloc[j]
    b_mn_02_lst = colorfeature_df['b_mn'].iloc[j]
    r_md_02_lst = colorfeature_df['r_md'].iloc[j]
    g_md_02_lst = colorfeature_df['g_md'].iloc[j]
    b_md_02_lst = colorfeature_df['b_mn'].iloc[j]
    r_sd_02_lst = colorfeature_df['r_sd'].iloc[j]
    g_sd_02_lst = colorfeature_df['g_sd'].iloc[j]
    b_sd_02_lst = colorfeature_df['b_sd'].iloc[j]
            
    len_video02 = len(h_mn_02_lst)

    ##ps 두 영상 비교
    idx_i = 0
    idx_j = 0

    #비교 시작시 초기화 
    idx_status = 0 # not same
    idx_match_len = 0 #영상 매칭 길이 초기화

    while True:
        if idx_i < len_video01: # 첫번째 영상의 비교요소가 끝까지 가지 않은 경우
            if idx_j < len_video02: # 두번째 영상의 비교요소가 끝까지 가지 않은 경우

                hmn01 = h_mn_01_lst[idx_i]
                smn01 = s_mn_01_lst[idx_i]
                vmn01 = v_mn_01_lst[idx_i]
                hmd01 = h_md_01_lst[idx_i]
                smd01 = s_md_01_lst[idx_i]
                vmd01 = v_md_01_lst[idx_i]
                hsd01 = h_sd_01_lst[idx_i]
                ssd01 = s_sd_01_lst[idx_i]
                vsd01 = v_sd_01_lst[idx_i]
                rmn01 = r_mn_01_lst[idx_i]
                gmn01 = g_mn_01_lst[idx_i]
                bmn01 = b_mn_01_lst[idx_i]
                rmd01 = r_md_01_lst[idx_i]
                gmd01 = g_md_01_lst[idx_i]
                bmd01 = b_md_01_lst[idx_i]
                rsd01 = r_sd_01_lst[idx_i]
                gsd01 = g_sd_01_lst[idx_i]
                bsd01 = b_sd_01_lst[idx_i]

                hmn02 = h_mn_02_lst[idx_j]
                smn02 = s_mn_02_lst[idx_j]
                vmn02 = v_mn_02_lst[idx_j]
                hmd02 = h_md_02_lst[idx_j]
                smd02 = s_md_02_lst[idx_j]
                vmd02 = v_md_02_lst[idx_j]
                hsd02 = h_sd_02_lst[idx_j]
                ssd02 = s_sd_02_lst[idx_j]
                vsd02 = v_sd_02_lst[idx_j]
                rmn02 = r_mn_02_lst[idx_j]
                gmn02 = g_mn_02_lst[idx_j]
                bmn02 = b_mn_02_lst[idx_j]
                rmd02 = r_md_02_lst[idx_j]
                gmd02 = g_md_02_lst[idx_j]
                bmd02 = b_md_02_lst[idx_j]
                rsd02 = r_sd_02_lst[idx_j]
                gsd02 = g_sd_02_lst[idx_j]
                bsd02 = b_sd_02_lst[idx_j]


                # 첫번째 영상데이터와 두번째 영상 데이터 비교
                rlt_diff = compare_img_frame(hmn01, smn01, vmn01, hmd01, smd01, vmd01, hsd01, ssd01, vsd01,
                                             rmn01, gmn01, bmn01, rmd01, gmd01, bmd01, rsd01, gsd01, bsd01,
                                             hmn02, smn02, vmn02, hmd02, smd02, vmd02, hsd02, ssd02, vsd02,
                                             rmn02, gmn02, bmn02, rmd02, gmd02, bmd02, rsd02, gsd02, bsd02)

                # initialize sim value if matching of image is not preceeding
                if idx_status == 0:
                    sim  = rlt_diff
                else:
                    sim = (sim * idx_len + rlt_diff)/(idx_len + 1)

                # 비교값의 임계치 이상 이하 검토
                if sim < para_diff:
                    #print('idx_i::' + str(idx_i) + ' - idx_j::' + str(idx_j) + ' - sim ::' +  str(rlt_diff))
                    if idx_status == 0:  # 첫 매칭인 경우
                        idx_status = 1   # 매칭상태 표시
                        idx_len = 1      # 매칭 길이 표시
                        v1_start_time = idx_i # 매칭 시작점
                        v2_start_time = idx_j # 매칭 시작점

                        # 인덱스 올림
                        idx_i += 1
                        idx_j += 1

                    else: # 매칭중인 경우(idx_status == 1)
                        idx_len += 1
                        v1_end_time = idx_i # 매칭될수록 갱신됨
                        v2_end_time = idx_j # 매칭될수록 갱신됨

                        # 인덱스 올림
                        idx_i += 1
                        idx_j += 1

                else: #임계치를 넘어가는 경우(매칭이 끝난경우)
                    if idx_status == 1: # 매칭중인 경우
                        # 매칭길이가 para_duration 이상인 경우만 결과에 기록
                        if idx_len >= para_duration:
                            ##ps upload hsv to mstuv.anal_video_hsv
                            ##### add result to insert_db
                            new_row = {'videoid1': videoid1,
                                       'videoid2': videoid2,
                                       'v1_start_time': v1_start_time,
                                       'v2_start_time': v2_start_time,
                                       'v1_end_time': v1_end_time,
                                       'v2_end_time': v2_end_time,
                                       'sim': sim,
                                       'insert_date':date_str
                                       }
                            insert_df = insert_df.append(new_row, ignore_index=True)

                            ## 매칭정보 초기화
                        idx_status = 0
                        idx_i += 1
                        idx_j = 0
                        idx_len = 0

                    else:  # 매칭중이 아닌 경우에는 두번째 영상요소 시퀀스만 올린다
                        idx_j += 1

            else:  # 첫번째는 괜찮은데 두번째 영상요소가 끝까지 간 경우
                idx_i += 1  # 비교없이 첫번째 영상의 인덱스를 올려서 종료조건이 되도록 함

        else:  # (idx_i >= len_video01)
            break
        # 첫번째 요소가 끝까지 갔으니 while를 빠져나가서 다음 두 영상 비교

    return insert_df

if __name__ == '__main__':
    print('ps03-20_find_same_video_clip_in_local.py')
    ## parameter
    para_duration = 20
    para_diff = 0.01

    ## preprocess
    colorfeature_df = get_colorfeature()
    colorfeature_df = trans_str_to_num_for_df(colorfeature_df)
    mov_cnt = len(colorfeature_df)

    insert_df = pd.DataFrame(columns = ['videoid1', 'videoid2',
                                        'v1_start_time', 'v1_end_time',
                                        'v2_start_time', 'v2_end_time',
                                        'sim', 'insert_date'])        
    for i in range(mov_cnt-1):
        for j in range(mov_cnt):
            print(str(i) + ' / ' + str(mov_cnt))

            insert_df = search_same_clip(colorfeature_df,insert_df, i, j,para_duration, para_diff)

    db = oaislib.fn_lab_db_connect()
    try:
        with db.cursor() as cursor:
            ## remove similar info of video1
            videoid1 = colorfeature_df['video_id'].iloc[i]
            sql_rm_previous = 'truncate table anal_local_search_same_video'
            oaislib.fn_run_sql_to_lab_db(sql_rm_previous)

            insert_cnt = len(insert_df)
            if insert_cnt > 0:
                for idx_insert in range(insert_cnt):
                    videoid1 = insert_df['videoid1'].iloc[idx_insert]
                    videoid2 = insert_df['videoid2'].iloc[idx_insert]
                    v1_start_time = insert_df['v1_start_time'].iloc[idx_insert]
                    v2_start_time = insert_df['v2_start_time'].iloc[idx_insert]
                    v1_end_time = insert_df['v1_end_time'].iloc[idx_insert]
                    v2_end_time = insert_df['v2_end_time'].iloc[idx_insert]
                    sim = insert_df['sim'].iloc[idx_insert]

                    sql = f'insert into anal_local_search_same_video (videoid1, videoid2, v1_start_time, v1_end_time, v2_start_time, v2_end_time, sim, insert_date) values("{videoid1}", "{videoid2}", "{v1_start_time}", "{v1_end_time}", "{v2_start_time}", "{v2_end_time}","{sim}",  "{date_str}")'
                    cursor.execute(sql)
                db.commit()
    finally:
        db.close()

    #breakpoint()
    print("time :", time.time() - start)
