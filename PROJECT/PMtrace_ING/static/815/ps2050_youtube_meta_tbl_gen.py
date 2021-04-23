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

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
from datetime import date
start = time.time()

def ps2050():
    ### IO name
    ## input
    input_filepath = 'output/ps2040/youtube_get_metadata.csv'

    ## output
    output_filepath = 'output/ps2050/youtube_tbl.csv'

    ### data load
    input_df = pd.read_csv(input_filepath)
    input_df = input_df.sort_values(by=['cdate'], axis=0)
    today_str = oaislib.fn_get_date_str()

    ### process
    if os.path.isfile(output_filepath):
        output_df = pd.read_csv(output_filepath)
        
    else:
        output_df = pd.DataFrame(columns = ['yid', 'y_url', 'title', 'channel',
                                            'watch_cnt', 'tag', 'desc','y_date','udate'])

    output_cnt = len(output_df)        
    input_cnt = len(input_df)  
    prefix = 'ps2050'
    output_dir = 'output/' + prefix
    oaislib.fn_output_dir_gen(output_dir)

    
    for i in range(input_cnt):

        oaislib.fn_disploop(prefix, i, 10, input_cnt)
            
        input_yid = input_df['yid'].iloc[i]
        input_y_url = input_df['y_url'].iloc[i]    
        input_title = input_df['title'].iloc[i]
        input_channel = input_df['channel'].iloc[i]
        input_watch_cnt = input_df['watch_cnt'].iloc[i]
        input_tag = input_df['tag'].iloc[i]
        input_y_date = input_df['y_date'].iloc[i]
        input_desc = input_df['description'].iloc[i]
        input_udate = today_str

        
        if output_cnt > 0:

            previous_ids = output_df['yid'].values
            if input_yid in previous_ids:
                ## 신규 yid가 기존에 있는 경우
                output_df.title.loc[output_df.yid == input_yid] = input_title
                output_df.channel.loc[output_df.yid == input_yid] = input_channel
                output_df.watch_cnt.loc[output_df.yid == input_yid] = input_watch_cnt
                output_df.tag.loc[output_df.yid == input_yid] = input_tag
                output_df.y_date.loc[output_df.yid == input_yid] = input_y_date
                output_df.desc.loc[output_df.yid == input_yid] = input_desc
                output_df.udate.loc[output_df.yid == input_yid] = today_str

            else:
                ## 신규 yid가 기존에 없는 경우
                new_row = {'yid': input_yid,
                        'y_url':input_y_url,
                        'title':input_title,
                        'channel':input_channel,
                        'watch_cnt':input_watch_cnt,
                        'tag':input_tag,
                        'desc':input_desc,   
                        'y_date':input_y_date,
                        'udate':today_str}
                output_df = output_df.append(new_row, ignore_index=True)
            
        else:
            new_row = {'yid': input_yid,
                    'y_url':input_y_url,
                    'title':input_title,
                    'channel':input_channel,
                    'watch_cnt':input_watch_cnt,
                    'tag':input_tag,
                    'desc':input_desc,   
                    'y_date':input_y_date,
                    'udate':today_str}
            output_df = output_df.append(new_row, ignore_index=True)

    ### save result
    output_df.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    ps2050()

