# -*- coding: utf-8 -*- 
# author : oaiskoo
# date : 200604 
# goal : 유튜브 동영상의 1초 간격의 HSV를 구해서 DB에 저장
#
# desc : input video_sycn
# desc : output 
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
# 200609 - print message update
# 200611 - db에 update하는 부분에 사이즈 에러가 떠서 색공간 값을 전부 0-100의 범위로 맞춤

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


import cv2 as cv
from moviepy.editor import *
import subprocess
import glob
import pymysql

date_str = oaislib.fn_get_date_str()

##ps function
def preprocess_of_workspace():
    if os.path.isdir('01_mov'):
        pass
    else:
        os.mkdir('01_mov')

    if os.path.isdir('02_img'):
        pass
    else:
        os.mkdir('02_img')

def get_video_info():
    sql = 'select video_id, provi_video_id from video_syc where con_provider_id = "YouTube"'
    video_info_df = oaislib.fn_get_df_from_lab_db(sql)
    video_info_df.columns = ['video_id', 'youtube_id']
    return video_info_df

def get_new_video_ids():
    sql_str01 = 'select video_id from video_syc where con_provider_id = "YouTube"'
    video_df = oaislib.fn_get_df_from_lab_db(sql_str01)
    video_cnt = len(video_df)
    
    sql_str02 = 'select video_id from anal_video_colorfeature'
    hsv_df = oaislib.fn_get_df_from_lab_db(sql_str02)
    hsv_count = len(hsv_df)
    
    video_ids = list(video_df['video_id'])
    hsv_ids = list(hsv_df['video_id'])
    
    new_ids = list()

    for i in range(len(video_ids)):
        video_id = video_ids[i]

        if video_id not in hsv_ids :
            new_ids.append(video_id)
    return new_ids

def download_youtube(youtube_id):
    download_url = 'https://www.youtube.com/watch?v=' + youtube_id
    filename = youtube_id + '.mp4'
    print('video is downloading... : '+'url : ' + download_url)
    run_text = ["youtube-dl", download_url, '-f', 'mp4', '-o', '01_mov/' + filename]
    download_rlt = subprocess.call(run_text)

    return download_rlt

def capture_image(youtube_id, youtube_clip, image_interval):
    print('capture imgs')
    duration = int(youtube_clip.duration)
    print('duration is ' + str(duration))
    for j in range(duration):
        if (j % image_interval) == 0:
            img_filepath = '02_img/' + youtube_id + '_' + str(100000 +j) + '.jpg'
            youtube_clip.save_frame(img_filepath, j)
            
    youtube_clip.close()
    return 0

def make_hsv_from_images(youtube_id):    
    img_filelist = sorted(glob.glob('02_img/'+ youtube_id + '_*.jpg')) # sort by name

    h_mn_list = list()
    s_mn_list = list()
    v_mn_list = list()
    h_md_list = list()
    s_md_list = list()
    v_sd_list = list()
    h_sd_list = list()
    s_sd_list = list()
    v_md_list = list()
    r_mn_list = list()
    g_mn_list = list()
    b_mn_list = list()
    r_md_list = list()
    g_md_list = list()
    b_md_list = list()
    r_sd_list = list()
    g_sd_list = list()
    b_sd_list = list()
    
    for i in range(len(img_filelist)):
        img_filepath = img_filelist[i]
        img_rgb = cv.imread(img_filepath, cv.IMREAD_COLOR)
        img_hsv = cv.cvtColor(img_rgb, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(img_hsv)
        r, g, b = cv.split(img_rgb)
        
        h_mn = np.mean(h)
        s_mn = np.mean(s)
        v_mn = np.mean(v)
        h_md = np.mean(h)
        s_md = np.mean(s)
        v_md = np.mean(v) 
        h_sd = np.std(h) 
        s_sd = np.std(s) 
        v_sd = np.std(v) 
        r_mn = np.mean(r) 
        g_mn = np.mean(g) 
        b_mn = np.mean(b) 
        r_md = np.mean(r) 
        g_md = np.mean(g) 
        b_md = np.mean(b) 
        r_sd = np.std(r) 
        g_sd = np.std(g) 
        b_sd = np.std(b) 
        
        h_mn_list.append(h_mn)
        s_mn_list.append(s_mn)
        v_mn_list.append(v_mn)
        h_md_list.append(h_md)
        s_md_list.append(s_md)
        v_md_list.append(v_md)
        h_sd_list.append(h_sd)
        s_sd_list.append(s_sd)
        v_sd_list.append(v_sd)
        r_mn_list.append(r_mn)
        g_mn_list.append(g_mn)
        b_mn_list.append(b_mn)
        r_md_list.append(r_md)
        g_md_list.append(g_md)
        b_md_list.append(b_md)
        r_sd_list.append(r_sd)
        g_sd_list.append(g_sd)
        b_sd_list.append(b_sd)
        
    return h_mn_list,s_mn_list, v_mn_list, h_md_list, s_md_list, v_md_list, h_sd_list, s_sd_list, v_sd_list, r_mn_list, g_mn_list, b_mn_list, r_md_list, g_md_list, b_md_list, r_sd_list, g_sd_list, b_sd_list

##ps main
if __name__ == '__main__':

    ## parameter
    image_interval = 1

    ## preprocess
    preprocess_of_workspace()
    ## for non-normal exit of this code
    oaislib.fn_remove_all_files_in_folder('01_mov')
    oaislib.fn_remove_all_files_in_folder('02_img')
    
    ## data load
    video_info = get_video_info()
    new_ids = get_new_video_ids()
    video_cnt = len(new_ids)

    rlt_df = pd.DataFrame(index = range(video_cnt),
                          columns = ['video_id', 'youtube_id', 'success','h_m', 's_m', 'v_m'])

    ## capture image and make hsv
    for i in range(video_cnt): #video_cnt
        video_id = new_ids[i]
        print(str(i) + '/' + str(video_cnt) )

        ##register the video id for multi download
        ## exec following code if the video_id is not register in the table
        db = oaislib.fn_lab_db_connect()
        try:
            with db.cursor() as cursor:
                sql = f'select count(*) from anal_video_colorfeature where video_id = "{video_id}"'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == 0:
                    sql_update = ('insert into anal_video_colorfeature (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_hsv_mn (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_hsv_md (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_hsv_sd (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_rgb_mn (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_rgb_md (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    sql_update = ('insert into anal_video_rgb_sd (video_id) '
                                  'values("{}")'
                                  .format(video_id))
                    cursor.execute(sql_update)
                    db.commit()
                else:
                    print( video_id + 'is already registered')
                    continue
        finally:
            db.close()

        youtube_id = video_info[video_info['video_id'] == video_id]['youtube_id'].iloc[0]
        youtube_filepath = '01_mov/' + youtube_id + '.mp4'
        idx_download = download_youtube(youtube_id)

        ## case of video downloading
        if idx_download == 0:
            youtube_clip = VideoFileClip(youtube_filepath)
            flag_capture = capture_image(youtube_id, youtube_clip, image_interval)

            ## make hsv from images
            h_mn_list,s_mn_list, v_mn_list, h_md_list, s_md_list, v_md_list, h_sd_list, s_sd_list, v_sd_list, r_mn_list, g_mn_list, b_mn_list, r_md_list, g_md_list, b_md_list, r_sd_list, g_sd_list, b_sd_list = make_hsv_from_images(youtube_id)

            ## chage int form float of hsv
            h_mn_list = [int(x) for x in h_mn_list]
            s_mn_list = [int(x) for x in s_mn_list]
            v_mn_list = [int(x) for x in v_mn_list]
            h_md_list = [int(x) for x in h_md_list]
            s_md_list = [int(x) for x in s_md_list]
            v_md_list = [int(x) for x in v_md_list]            
            h_sd_list = [int(x) for x in h_sd_list]
            s_sd_list = [int(x) for x in s_sd_list]
            v_sd_list = [int(x) for x in v_sd_list]
            r_mn_list = [int(x) for x in r_mn_list]
            g_mn_list = [int(x) for x in g_mn_list]
            v_mn_list = [int(x) for x in v_mn_list]
            r_md_list = [int(x) for x in r_md_list]
            g_md_list = [int(x) for x in g_md_list]
            b_md_list = [int(x) for x in b_md_list]
            r_sd_list = [int(x) for x in r_sd_list]
            g_sd_list = [int(x) for x in g_sd_list]
            b_sd_list = [int(x) for x in b_sd_list]
            
            ##ps upload hsv to mstuv.anal_video_colorfeature
            db = oaislib.fn_lab_db_connect()

            try:
                with db.cursor() as cursor:
                    sql_update = ('update anal_video_hsv_mn '
                                  'set h_mn = "{}" , '
                                  's_mn = "{}" , '
                                  'v_mn = "{}"  '
                                  'where video_id = "{}" '
                                  .format(h_mn_list,
                                          s_mn_list,
                                          v_mn_list,
                                          video_id))
                    #print(sql_update)
                    cursor.execute(sql_update)
                    db.commit()                    
                    sql_update = ('update anal_video_hsv_md '
                                  'set h_md = "{}" , '
                                  's_md = "{}" , '
                                  'v_md = "{}"  '
                                  'where video_id = "{}" '
                                  .format(h_md_list,
                                          s_md_list,
                                          v_md_list,
                                          video_id))
                    #print(sql_update)
                    cursor.execute(sql_update)
                    db.commit()
                    sql_update = ('update anal_video_hsv_sd '
                                  'set h_sd = "{}" , '
                                  's_sd = "{}" , '
                                  'v_sd = "{}"  '
                                  'where video_id = "{}" '
                                  .format(h_sd_list,
                                          s_sd_list,
                                          v_sd_list,
                                          video_id))
                    #print(sql_update)                    
                    cursor.execute(sql_update)
                    db.commit()
                    sql_update = ('update anal_video_rgb_mn '
                                  'set r_mn = "{}" , '
                                  'g_mn = "{}" , '
                                  'b_mn = "{}"  '
                                  'where video_id = "{}" '
                                  .format(r_mn_list,
                                          g_mn_list,
                                          b_mn_list,
                                          video_id))
                    #print(sql_update)
                    cursor.execute(sql_update)
                    db.commit()
                    sql_update = ('update anal_video_rgb_md '
                                  'set r_md = "{}" , '
                                  'g_md = "{}" , '
                                  'b_md = "{}"  '
                                  'where video_id = "{}" '
                                  .format(r_md_list,
                                          g_md_list,
                                          b_md_list,
                                          video_id))
                    #print(sql_update)                    
                    cursor.execute(sql_update)
                    db.commit()
                    sql_update = ('update anal_video_rgb_sd '
                                  'set r_sd = "{}" , '
                                  'g_sd = "{}" , '
                                  'b_sd = "{}"  '
                                  'where video_id = "{}" '
                                  .format(r_sd_list,
                                          g_sd_list,
                                          b_sd_list,
                                          video_id))
                    #print(sql_update)                    
                    cursor.execute(sql_update)
                    sql_update = ('update anal_video_colorfeature '
                                  'set youtube_id = "{}", '
                                  'success = "yes", '                                  
                                  'insert_date = "{}" '
                                  'where video_id = "{}" '
                                  .format(youtube_id,
                                          date_str,
                                          video_id))
                    print(sql_update)                    
                    cursor.execute(sql_update)
                
                    db.commit()
            finally:
                db.close()

        else:
            ## record for failure of download
            db = oaislib.fn_lab_db_connect()
            try:
                with db.cursor() as cursor:
                    sql_update = ('update anal_video_colorfeature '
                                  'set youtube_id = "{}", '
                                  'success = "no", '
                                  'insert_date = "{}" '
                                  'where video_id = "{}"'
                                  .format(youtube_id, date_str, video_id))
                    cursor.execute(sql_update)
                    db.commit()
            finally:
                print('download video is failed')
                db.close()
            
        oaislib.fn_remove_all_files_in_folder('01_mov')
        oaislib.fn_remove_all_files_in_folder('02_img')

#breakpoint()
print("time :", time.time() - start)
