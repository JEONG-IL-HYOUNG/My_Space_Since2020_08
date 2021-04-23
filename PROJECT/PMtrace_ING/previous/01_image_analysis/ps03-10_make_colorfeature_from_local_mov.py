# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200615
# goal : 로컬 동영상에 대해서 colorfeature를 뽑아서 DB에 저장함 
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

import glob
from moviepy.editor import *
import cv2 as cv
import pymysql

def capture_image(mov_id, mov_clip, image_interval):
    print('capture imgs')
    duration = int(mov_clip.duration)
    print('duration is ' + str(duration))
    for j in range(duration):
        if (j % image_interval) == 0:
            img_filepath = '04_local_img/' + mov_id + '_' + str(100000 +j) + '.jpg'
            mov_clip.save_frame(img_filepath, j)
            
    mov_clip.close()
    return 0

def make_hsv_from_images(mov_id):    
    img_filelist = sorted(glob.glob('04_local_img/'+ mov_id + '_*.jpg')) # sort by name

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

    print('ps03-10_make_colorfeature_from_local_mov.py')
    mov_list = sorted(glob.glob('03_local_mov/*.mp4'))
    mov_cnt = len(mov_list)

    ## parameter
    image_interval = 1

    ##preprocess
    oaislib.fn_remove_all_files_in_folder('04_local_img')
    date_str = oaislib.fn_get_date_str()

    db = oaislib.fn_lab_db_connect()
    try:
        with db.cursor() as cursor:

            ## capture img
            for i in range(mov_cnt):
                movfile_name = mov_list[i]
                mov = VideoFileClip(movfile_name)
                mov_id = movfile_name[13:15]
                capture_image(mov_id, mov, image_interval)
        
                ## make hsv from images
                h_mn_list,s_mn_list, v_mn_list, h_md_list, s_md_list, v_md_list, h_sd_list, s_sd_list, v_sd_list, r_mn_list, g_mn_list, b_mn_list, r_md_list, g_md_list, b_md_list, r_sd_list, g_sd_list, b_sd_list = make_hsv_from_images(mov_id)

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


                sql_update = ('insert into anal_local_video_colorfeature (video_id, success, insert_date) '
                              'values("{}","yes","{}")'
                              .format(str(mov_id), date_str))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_hsv_md (video_id, h_md, s_md, v_md) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), h_md_list, s_md_list, v_md_list))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_hsv_mn (video_id, h_mn, s_mn, v_mn) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), h_mn_list, s_mn_list, v_mn_list))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_hsv_sd (video_id, h_sd, s_sd, v_sd) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), h_sd_list, s_sd_list, v_sd_list))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_rgb_md (video_id, r_md, g_md, b_md) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), r_md_list, g_md_list, b_md_list))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_rgb_mn (video_id, r_mn, g_mn, b_mn) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), r_mn_list, g_mn_list, b_mn_list))
                #print(sql_update)
                cursor.execute(sql_update)

                sql_update = ('insert into anal_local_video_rgb_sd (video_id, r_sd, g_sd, b_sd) '
                              'value( "{}", "{}", "{}", "{}")'
                              .format(str(mov_id), r_sd_list, g_sd_list, b_sd_list))
                #print(sql_update)
                cursor.execute(sql_update)

                db.commit()

    finally:
        db.close()

breakpoint()
print("time :", time.time() - start)
