# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200629
# goal : 유튜브 영상 다운로드실패한 비디오 아이디 관련 lab DB 정리 
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
#import re
#import pandas as pd
#import numpy as np
if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
start = time.time()
print("start ps02-13_cleaning_lab_colorfeature.py")

##anal_video_colorfeature 정리
sql_str = 'delete from anal_video_colorfeature where success is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_md where h_md is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_mn where h_mn is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_sd where h_sd is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_mn where r_mn is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_md where r_md is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_sd where r_sd is null'
oaislib.fn_run_sql_to_lab_db(sql_str)

##anal_video_colorfeature 정리
sql_str = 'delete from anal_video_colorfeature where success = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_md where h_md = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_mn where h_mn = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_hsv_sd where h_sd = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_mn where r_mn = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_md where r_md = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)

sql_str = 'delete from anal_video_rgb_sd where r_sd = ""'
oaislib.fn_run_sql_to_lab_db(sql_str)




#breakpoint()
print("time :", time.time() - start)
