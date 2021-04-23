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
import sys


if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
start = time.time()

### IO name
## input
input_filepath = 'output/ps2070/youtube_batch_user_meta.csv'

## output
prefix = 'ps4010'
output_dir = 'output/' + prefix 
oaislib.fn_output_dir_gen(output_dir)
output_filepath = 'output/' + prefix + '/simple_meta_str.csv'

### data load
if os.path.isfile(input_filepath):
    input_df = pd.read_csv(input_filepath)
    input_cnt = len(input_df)
else:
    sys.exit(prefix + '::input file do not exist')
    

### process
## yid gethering
today_str = oaislib.fn_get_date_str()    

if os.path.isfile(output_filepath):
    output_df = pd.read_csv(output_filepath)
    output_cnt = len(output_df)

    ## 기존 input_df에서 mov_id 추가된 것 확인하고 추가하고 mstr_yn는 n로 설정
    for i in range(input_cnt):

        oaislib.fn_disploop(prefix, i, 10, input_cnt)
        input_mov_id = input_df['mov_id'].iloc[i]

        if output_cnt > 0:
            previous_ids = output_df['mov_id'].values
            if input_mov_id in previous_ids:
                ## 신규 yid가 기존에 있는 경우 패스
                pass
            else:
                new_row = {'mov_id' : input_mov_id,
                           'mstr_yn' : 'n',
                           'mstr_str': '',
                           'mstr_dt' : '',
                           'cdate' : today_str}
                output_df = output_df.append(new_row, ignore_index=True)
        
else:
    output_df = input_df[['mov_id']].copy()
    output_df['mstr_yn'] = 'n'
    output_df['mstr_str'] = ''    
    output_df['cdate'] = today_str

## make meta string for new yid
output_cnt = len(output_df)
if output_cnt == 0:
    sys.exit("no mov id")

for i in range(output_cnt):
    if output_df['mstr_yn'].iloc[i] == 'n':
        mov_id_v = output_df['mov_id'].iloc[i]

        title_v = input_df.mov_title.loc[input_df.mov_id == mov_id_v].values[0]
        tag_v = input_df.mov_tag.loc[input_df.mov_id == mov_id_v].values[0]
        desc_v = input_df.mov_desc.loc[input_df.mov_id == mov_id_v].values[0]
        
        mstr_str_v = str(title_v) + str(tag_v) + str(desc_v)
        mstr_str_v = oaislib.fn_get_ko_en_num_from_text(mstr_str_v)
        
        output_df.at[i,'mstr_str'] = mstr_str_v
        output_df.at[i,'mstr_yn'] = 'y'
        
        
### save result
output_df.to_csv(output_filepath, index=False)
    
## finish message
print("time :", time.time() - start)
breakpoint()
