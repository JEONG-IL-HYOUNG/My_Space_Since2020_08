# -*- coding: utf-8 -*- 
# author : oaiskoo
# date : 200604 
# goal : 유튜브 동영상의 1초 간격의 HSV를 구해서 DB에 저
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
    
    sql_str02 = 'select video_id from anal_video_hsv_median'
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
    for j in range(duration):
        if (j % image_interval) == 0:
            img_filepath = '02_img/' + youtube_id + '_' + str(100000 +j) + '.jpg'
            youtube_clip.save_frame(img_filepath, j)
            
    youtube_clip.close()
    return 0

def make_hsv_from_images(youtube_id):    
    img_filelist = sorted(glob.glob('02_img/'+ youtube_id + '_*.jpg')) # sort by name

    h_list = list()
    s_list = list()
    v_list = list()
        
    for i in range(len(img_filelist)):
        img_filepath = img_filelist[i]
        img_rgb = cv.imread(img_filepath, cv.IMREAD_COLOR)
        img_hsv = cv.cvtColor(img_rgb, cv.COLOR_BGR2HSV)
        h, s, v = cv.split(img_hsv)

        h_m = np.median(h)
        s_m = np.median(s)
        v_m = np.median(v)
        
        h_list.append(h_m)
        s_list.append(s_m)
        v_list.append(v_m)
            
    return h_list, s_list, v_list



##ps main
if __name__ == '__main__':

    ## parameter
    image_interval = 1

    ## preprocess
    preprocess_of_workspace()
    
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

        ##멀티 다운로드를 위한 video id 선제 등록
        ## 등록하려고 하는 아이디가 DB에 등록이 안되어 있으면
        db = oaislib.fn_lab_db_connect()
        try:
            with db.cursor() as cursor:
                sql = f'select count(*) from anal_video_hsv_median where video_id = "{video_id}"'
                cursor.execute(sql)
                result = cursor.fetchall()
                if result[0][0] == 0:
                    sql_update = ('insert into anal_video_hsv_median (video_id) '
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
            h_list, s_list, v_list = make_hsv_from_images(youtube_id)

            ## chage int form float of hsv
            h_list = [int(x) for x in h_list]
            s_list = [int(x) for x in s_list]
            v_list = [int(x) for x in v_list]
            
            ##ps upload hsv to mstuv.anal_video_hsv_median
            db = oaislib.fn_lab_db_connect()

            try:
                with db.cursor() as cursor:
                    sql_update = ('update anal_video_hsv_median '
                                  'set youtube_id = "{}", '
                                  'success = "yes", '
                                  'h_m = "{}" , '
                                  's_m = "{}" , '
                                  'v_m = "{}" , '
                                  'insert_date = "{}" '
                                  'where video_id = "{}" '
                                  .format(youtube_id, h_list, s_list, v_list, date_str, video_id))
                    cursor.execute(sql_update)
                    db.commit()
            finally:
                db.close()

        else:
            ## 다운로드를 실패했다는 정보를 기록함
            db = oaislib.fn_lab_db_connect()
            
            try:
                with db.cursor() as cursor:
                    sql_update = ('update anal_video_hsv_median '
                                  'set youtube_id = "{}", '
                                  'success = "no", '
                                  'insert_date = "{}" '
                                  'where video_id = "{}"'
                                  .format(youtube_id, date_str, video_id))
                    cursor.execute(sql_update)
                    db.commit()
            finally:
                db.close()
            
        oaislib.fn_remove_all_files_in_folder('01_mov')
        oaislib.fn_remove_all_files_in_folder('02_img')

#breakpoint()
print("time :", time.time() - start)
