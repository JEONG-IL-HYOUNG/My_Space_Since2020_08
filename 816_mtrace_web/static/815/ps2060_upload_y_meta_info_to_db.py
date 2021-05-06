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

def ps2060():
    start = time.time()
    ### IO name
    ## input
    input_filepath = 'output/ps2050/youtube_tbl.csv'

    ## output
    prefix = 'ps2060'
    output_dir = 'output/' + prefix 
    oaislib.fn_output_dir_gen(output_dir)
    ##output_filepath = 'output/' + prefix + '/.csv'

    ### data load
    input_df = pd.read_csv(input_filepath)
    input_df = input_df.convert_dtypes()
    input_cnt = len(input_df)

    ### process

    ## get go_mov tbl data
    sql_str = 'select * from gb_mov'
    y_meta_tbl_df = oaislib.fn_get_df_from_test_mtrace_db(sql_str)

    ##input_df
    ##Index(['yid', 'y_url', 'title', 'channel', 'watch_cnt', 'tag', 'desc',
    ##       'y_date', 'udate'],

    ## y_meta_tbl_df
    ##Index(['mov_id', 'mov_prov', 'mov_prov_id', 'mov_title', 'mov_owner',
    ##       'mov_date', 'mov_view_cnt', 'mov_tag', 'mov_desc', 'cdate'],


    ### DB 연결
    db = oaislib.fn_connect_test_mtrace_db()    
    try:
        with db.cursor() as cursor:
            for i in range(input_cnt):
                print(i)
                ## input_df.yid가 y_meta_tbl_df에 있는지 확인
                yid_v = input_df['yid'].iloc[i]
                title_v = input_df['title'].iloc[i]
                channel_v = input_df['channel'].iloc[i]
                watch_cnt_v = input_df['watch_cnt'].iloc[i]
                tag_v = input_df['tag'].iloc[i]
                desc_v = input_df['desc'].iloc[i]
                y_date_v = input_df['y_date'].iloc[i]
                udate_v = input_df['udate'].iloc[i]

                ##desc에 한글만 오게 필터링
                ## desc_v = oaislib.fn_get_text_ko(desc_v)

                ##desc에서 이모지 기호제거

                if desc_v is not pd.NA:
                    desc_v =oaislib.fn_rm_all_expt_bmp(desc_v)
                    desc_v = re.sub('[-=+#/\?:^$.,@*\"※~&%ㆍ!ㅡ』\\\;_‘|\(\)\[\]\<\>`\'…》]', ' ', desc_v)

                
                ##tag에서 이모지 기호제거
                if tag_v is not pd.NA:
                    tag_v =oaislib.fn_rm_all_expt_bmp(tag_v)
                    tag_v = re.sub('[-=+#/\?:^$.,@*\"※~&%ㆍ!ㅡ』\\\;_‘|\(\)\[\]\<\>`\'…》]', ' ', tag_v)

                ##제목에서 이모지, 기호 제거
                if title_v is not pd.NA:
                    title_v =oaislib.fn_rm_all_expt_bmp(title_v)
                    title_v = re.sub('[-=+#/\?:^$.,@*\"※~&%ㆍ!ㅡ』\\\;_‘|\(\)\[\]\<\>`\'…》]', ' ', title_v)

                ## 기존에 등록된 것 경우 update
                if yid_v in y_meta_tbl_df['mov_prov_id'].values:
                    mov_id_v = y_meta_tbl_df['mov_id'][y_meta_tbl_df['mov_prov_id'] == yid_v].values[0]
                    provider_v = y_meta_tbl_df['mov_prov'][y_meta_tbl_df['mov_id'] == mov_id_v].values[0]
                    if provider_v == 'youtube':
                        ## 확인이 되었으니 업데이트

                        sql_v = f'update gb_mov set mov_prov = "youtube" , mov_prov_id = "{yid_v}", mov_title = "{title_v}", mov_owner = "{channel_v}", mov_date = "{y_date_v}", mov_view_cnt = {watch_cnt_v}, mov_desc = "{desc_v}",  cdate = "{udate_v}", mov_tag = "{tag_v}" where mov_id = {mov_id_v}'
                        ##print(sql_v)
                        cursor.execute(sql_v)

                    else:
                        ## 다른 프로바이더니 pass
                        pass
                else:
                    ## 기존에 없는경우는 추가
                    sql_v = f'insert into gb_mov (mov_prov, mov_prov_id,  mov_title, mov_owner, mov_date, mov_view_cnt, mov_tag, mov_desc,  cdate) values ("youtube" ,"{yid_v}", "{title_v}", "{channel_v}", "{y_date_v}", {watch_cnt_v}, "{tag_v}", "{desc_v}",  "{udate_v}")'
                    ##print(sql_v)
                    cursor.execute(sql_v)

                ## 중간에 커밋
                if i % 1000 == 0:
                    db.commit()
            db.commit()
    finally:
        db.close()
    print("time :", time.time() - start)

if __name__ == '__main__':
    ps2060()
    breakpoint()
