# -*- coding: utf-8 -*-
##author : oaiskoo
##date : 2006
##goal : 
##
##input
##
##
##process
##
##
##output
##
## 
##history
##-2009
##--task
##
import os
import shutil
import time
import re
import pandas as pd
import numpy as np
from moviepy.editor import VideoFileClip
from os.path import basename

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
import glob


#일초당 캡쳐
def capture_image2(yid, y_clip, y_imgpath ):
    print(yid + ' image capture start')
    duration = int(y_clip.duration)
    for i in range(duration-1):
        img_filepath = y_imgpath + '/' + yid + '_' + str(1000000 + i) + '.jpg'
        y_clip.save_frame(img_filepath, i)
    
def ps3020():        
    ### IO name
    ## input
    input_dir = 'output/ps3010/'
    input_filepath = 'output/ps3010/01_y_tbl_dn.csv'

    ## output
    output_dir = 'output/ps3020/'
    previous_filepath = 'output/ps3020/01_y_img_tbl.csv'

    ### data load
    input_df = pd.read_csv(input_filepath)
    output_df = input_df.copy()
    output_df['img_yn'] = 'n'
    output_df['img_date'] = ''
    today_str = oaislib.fn_get_date_str()
    
    ## 업데이트된 리스트를 불러온 후에 거기에 다운로드 정보를 덮어씌운다.
    if os.path.exists(previous_filepath):
        previous_df = pd.read_csv(previous_filepath)
        previous_df = previous_df[previous_df.img_yn == 'y']
        previous_cnt = len(previous_df)

        for i in range(previous_cnt):
            yid_str = previous_df['yid'].iloc[i]
            img_date_str = previous_df['img_date'].iloc[i]
            output_df.img_yn.loc[output_df.yid == yid_str] = 'y'
            output_df.img_date.loc[output_df.yid == yid_str] = img_date_str

    ## input_dir에 있는 모든 mp4에 대한 동영상 리스트를 가지고 옴
    mp4_list = glob.glob(input_dir + '*.mp4')
    v_cnt = len(mp4_list)

    ### process
    ## 동영상 하나씩 output폴더에 동일 폴더명이 있는지 확인 후
    ## 있으면 안에 있는 파일을 지우고, 캡쳐뜨고, 없으면 폴더를 만들고 캡쳐뜸
    ## 캡쳐는 1초 단위이며 캡쳐 완료 후 해당 동영상은 삭제함
    for i in range(v_cnt):
        y_filepath = mp4_list[i]
        y_filename = basename(y_filepath)
        yid_str = y_filename[:-4]

        y_imgpath = output_dir + yid_str
        oaislib.fn_init_folder(y_imgpath) #폴더 초기화(폴더 생성 후 내부파일 삭제)

        ## image capture
        y_clip = VideoFileClip(y_filepath).resize(width=480)
        capture_image2(yid_str, y_clip, y_imgpath)
        del(y_clip)

        ##완료 후 파일 삭제
        os.remove(y_filepath)
            
        ## 테이블에 업데이트
        output_df.img_yn.loc[output_df.yid == yid_str] = 'y'
        output_df.img_date.loc[output_df.yid == yid_str] = today_str

    output_df.to_csv(previous_filepath, index=False)

if __name__ == '__main__':
    ps3020()
