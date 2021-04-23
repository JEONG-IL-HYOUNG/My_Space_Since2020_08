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



def ps2070():
    ### IO name
    ## input
    input_filepath = 'output/ps2050/youtube_tbl.csv'
    today_str = oaislib.fn_get_date_str()

    ## output
    prefix = 'ps2070'
    output_dir = 'output/' + prefix
    oaislib.fn_output_dir_gen(output_dir)
    output_filepath = 'output/' + prefix + '/youtube_batch_user_meta.csv'

    ### data load
    input_df = pd.read_csv(input_filepath)
    input_cnt = len(input_df)
    ### process

    ## gb_mov download
    sql_str = 'select  * from gb_mov'
    gb_mov_df = oaislib.fn_get_df_from_test_mtrace_db(sql_str)
    gb_mov_cnt = len(gb_mov_df)

    ## 기존 output file 유무에 따라서 나뉨
    if os.path.isfile(output_filepath):
        output_df = pd.read_csv(output_filepath)

    else:
        output_df = pd.DataFrame(columns = ['mov_id', 'mov_prov', 'mov_prov_id', 'mov_title',
                                            'mov_owner', 'mov_date', 'mov_view_cnt',
                                            'mov_tag', 'mov_desc', 'cdate'])


    ## output_df에 신규 youtube id를 추가
    for i in range(input_cnt):

        oaislib.fn_disploop('add youtube id', i, 100, input_cnt)

        input_yid = input_df['yid'][i]

        rlt_df = output_df[output_df['mov_prov_id'] == input_yid]
        if len(rlt_df) == 0:
            input_y_url = input_df['y_url'][i]
            input_title = input_df['title'][i]
            input_channel = input_df['channel'][i]
            input_watch_cnt = input_df['watch_cnt'][i]
            input_tag = input_df['tag'][i]
            input_y_date = input_df['y_date'][i]
            input_desc = input_df['desc'][i]
            input_udate = today_str

            new_row = {'mov_prov' : 'youtube',
                       'mov_prov_id' : input_yid,
                       'mov_title' : input_title,
                       'mov_owner' : input_channel,
                       'mov_date' : input_y_date,
                       'mov_view_cnt' : input_watch_cnt,
                       'mov_tag' : input_tag,
                       'mov_desc': input_desc,
                       'cdate': input_udate}

            output_df = output_df.append(new_row, ignore_index=True)

    ## output_df에 mov_id 추가
    output_cnt = len(output_df)

    for i in range(output_cnt):
        mov_prov_v = output_df['mov_prov'].iloc[i]
        mov_prov_id_v = output_df['mov_prov_id'].iloc[i]

        if mov_prov_v == 'youtube':
            rlt_df = gb_mov_df[gb_mov_df['mov_prov_id'] == mov_prov_id_v]

            if(len(rlt_df)) == 1:
                mov_id_v = rlt_df['mov_id'].values[0]
                output_df.at[i,'mov_id'] = mov_id_v
            else:
                sys.exit('duplicated id')

    ## output_df에 신규 local id를 등록함
    gb_mov_local_df = gb_mov_df[gb_mov_df['mov_prov'] == 'local']
    gb_mov_local_cnt = len(gb_mov_local_df)

    
    for i in range(gb_mov_local_cnt):
        mov_id_v = gb_mov_local_df.at[i,'mov_id']

        rlt_df = output_df[output_df['mov_id'] == mov_id_v]

        ## 기존에 있으면 업데이트 안한다에서 사용자 동영상은 무조건 업데이트한다로 변경
        if len(rlt_df) == 0:

            mov_prov_v = gb_mov_local_df.at[i,'mov_prov']
            mov_title_v = gb_mov_local_df.at[i,'mov_title']
            mov_owner_v = gb_mov_local_df.at[i,'mov_owner']
            mov_date_v = gb_mov_local_df.at[i,'mov_date']
            mov_tag_v = gb_mov_local_df.at[i,'mov_tag']
            mov_desc_v = gb_mov_local_df.at[i,'mov_desc']
            cdate_v = oaislib.fn_get_date_str()

            new_row = { 'mov_id': mov_id_v,
                        'mov_prov' : mov_prov_v,
                        'mov_title' : mov_title_v,
                        'mov_owner' : mov_owner_v,
                        'mov_date' : mov_owner_v,
                        'mov_tag' : mov_tag_v,
                        'mov_desc' : mov_desc_v,
                        'cdate': cdate_v}

        elif len(rlt_df) == 1: # 기존에 있는 경우 업데이트
            
            print("")
        else:
            sys.exit('dup mov_id')
            

            
            output_df = output_df.append(new_row, ignore_index=True)
        
    ### save result
    output_df.to_csv(output_filepath, index=False)


if __name__ == '__main__':
    ps2070()

## finish message
print("time :", time.time() - start)
##breakpoint()
