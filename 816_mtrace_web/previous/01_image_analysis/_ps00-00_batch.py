# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 200609
# goal : ps01에 대한 배치 프로세스
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

#while True:
os.system('python ps01-10_cal_video_sim_preprocess_with_morp.py')
os.system('python ps01-11_cal_video_sim_preprocess_with_word.py')
os.system('python ps01-22_cal_video_sim_cosine_fast_with_morp.py')
os.system('python ps01-23_cal_video_sim_cosine_fast_with_word.py')
os.system('python ps02-13_cleaning_lab_colorfeature.py')
os.system('python ps02-20_find_same_video_from_youtube.py')

