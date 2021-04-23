# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 2006
# goal : 
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
# 200701 - 영상정보 기반으로 검색하는 함수 추가
## 200818 - 유사영상 검색에서 태그유사도를 같이 검토하는 조건을 추가

import os
import shutil
import time
import re
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
from datetime import datetime

def get_video_by_keyword(keyword, cnt):
    keyword = keyword.strip()
    sql_title = f'select video_id, provi_video_id, title, reg_dt from video_syc where title like "%{keyword}%" and con_provider_id = "YouTube" limit {cnt}'
    #print(sql_title)
    std_video_df = oaislib.fn_get_df_from_lab_db(sql_title)
    std_video_df.columns = ['video_id', 'youtube_id', 'title', 'date']
    return std_video_df

def get_video_info_by_keyword(keyword, cnt):
    std_video_df = get_video_by_keyword(keyword, cnt)
    video_cnt = len(std_video_df)
    
    if video_cnt > 0:
        youtube_ids=std_video_df['youtube_id'].to_list()
        titles=std_video_df['title'].to_list()
        video_ids=std_video_df['video_id'].to_list()
        std_video_info=zip(youtube_ids, titles, video_ids)
    else:
        std_video_info = list()
        
    return std_video_info, video_cnt

def get_video_df_by_videoid(videoid, cnt):
    sql_title = f'select video_id, provi_video_id, title, reg_dt from video_syc where video_id = "{videoid}" and con_provider_id = "YouTube" limit {cnt}'
    std_video_df = oaislib.fn_get_df_from_lab_db(sql_title)
    
    return std_video_df

def get_sim_video_for_web(std_video_df):
    sim_video_df=pd.DataFrame('-', index=range(16), columns=['video_id','youtube_id', 'title', 'sim','rank'])
    idx = -1
    video_cnt = min(len(std_video_df),4)
    for i in range(video_cnt):
        video_id01 = std_video_df['video_id'].iloc[i]
        sql_get_sim_video = f'select video_id2, youtube_id2, sim, rank from anal_video_similarity_with_word where video_id1 = "{video_id01}" '
        rlt_df = oaislib.fn_get_df_from_lab_db(sql_get_sim_video)
        video_cnt = min(len(rlt_df), 4)
        
        for j in range(video_cnt):
            idx +=1
            video_id02 = rlt_df['video_id2'].iloc[j]
            sql_get_title = f'select title from video_syc where video_id = "{video_id02}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_get_title)
            sim_video_df['video_id'].iloc[idx] = rlt_df['video_id2'].iloc[j]
            sim_video_df['youtube_id'].iloc[idx] = rlt_df['youtube_id2'].iloc[j]
            title = title_df['title'].iloc[0]
            sim_video_df['title'].iloc[idx] = title
            sim_video_df['sim'].iloc[idx] = round(rlt_df['sim'].iloc[j],3)
            sim_video_df['rank'].iloc[idx] = rlt_df['rank'].iloc[j]            
    return sim_video_df

def get_sim_video_for_mobile(std_video_id):
    ## 동영상이 나오는지 확인하는 쿼리(DB를 좀더 쌓아야 할 듯)
    sql_get_sim_video = f'select video_id2, youtube_id2, sim, rank from(  select a.video_id1 as video_id1, a.youtube_id1 as youtube_id1, a.video_id2 as video_id2, a.youtube_id2 as youtube_id2, a.sim as sim, a.rank as rank from anal_video_similarity_with_word as a join anal_video_colorfeature as b  on a.video_id1 = b.video_id and b.success = "yes") c where c.video_id1 = "{std_video_id}" and sim > 0.1'

    rlt_df  = oaislib.fn_get_df_from_lab_db(sql_get_sim_video)
    rlt_cnt = len(rlt_df)
    sim_video_df= pd.DataFrame('', index=range(rlt_cnt), columns=['video_id','youtube_id', 'title', 'sim','rank'])
    
    for i in range(rlt_cnt):
        video_id = rlt_df['video_id2'].iloc[i]
        youtube_id = rlt_df['youtube_id2'].iloc[i]
        sql_get_title = f'select title from video_syc where video_id = "{video_id}"'
        title = oaislib.fn_get_df_from_lab_db(sql_get_title)
        rank = rlt_df['rank'].iloc[i]
        sim = rlt_df['sim'].iloc[i]
        sim_video_df['video_id'].iloc[i] = video_id
        sim_video_df['youtube_id'].iloc[i] = youtube_id
        sim_video_df['title'].iloc[i] = title['title'].iloc[0]
        sim_video_df['sim'].iloc[i] = sim
        sim_video_df['rank'].iloc[i] = rank
        
    return sim_video_df

def get_video_info_from_video_id(video_id):
    sql_get_video_info = f'select provi_video_id, title from video_syc where video_id = "{video_id}"'
    rlt_df = oaislib.fn_get_df_from_lab_db(sql_get_video_info)
    youtube_id = rlt_df['provi_video_id'].iloc[0]
    title = rlt_df['title'].iloc[0]
    return youtube_id, title



def get_video_by_youtubeid(youtubeid, cnt):
    youtubeid = youtubeid.strip()
    sql_title = f'select video_id, provi_video_id, title, reg_dt from video_syc where provi_video_id like "%{youtubeid}%" and con_provider_id = "YouTube" limit {cnt}'
    std_video_df = oaislib.fn_get_df_from_lab_db(sql_title)
    std_video_df.columns = ['video_id', 'youtube_id', 'title', 'date']
    return std_video_df

def imgbase_search_std_video(search_video_keyword, search_youtubeid):
    search_video_keyword = search_video_keyword.strip()
    if len(search_video_keyword) > 0:
        std_video_df = get_video_by_keyword(search_video_keyword,4)
    else:
        std_video_df = get_video_by_youtubeid(search_youtubeid,4)

    return std_video_df

def imgbase_search_sim_video_info2(vid, yid, cnt):
    std_vid = vid.strip()
    yid = yid.strip()
    if len(vid) > 0:
        std_video_df = get_video_df_by_videoid(std_vid, cnt)
    else:
        std_video_df = get_video_by_youtubeid(yid, cnt)

    if len(std_video_df) == 1:
        std_vid = std_video_df['video_id'].iloc[0]
        sim_video_df = imgbase_get_same_video(std_vid)

        if len(sim_video_df) > 0:
            sim_video_df['sim'] = round(sim_video_df['sim'],3)

            ## 태그 유사도 계산
            sim_video_df['tag_sim'] = 0 # add tag sim column
            for i in range(len(sim_video_df)):
                vid01 = sim_video_df['videoid1'].iloc[i]
                vid02 = sim_video_df['videoid2'].iloc[i]
                tag_sim = get_tag_sim_in_vids(vid01, vid02)
                sim_video_df['tag_sim'].iloc[i] = round(tag_sim,3)            

            ## zip 파일화
            videoid01s = sim_video_df['videoid1'].to_list()      
            youtubeid01s = sim_video_df['youtubeid1'].to_list()
            ch_nm1s = sim_video_df['ch_nm1'].to_list()
            videoid02 = sim_video_df['videoid2'].to_list()                
            youtubeid02s = sim_video_df['youtubeid2'].to_list()
            ch_nm2s = sim_video_df['ch_nm2'].to_list()            
            v1_start_times = sim_video_df['v1_start_time'].to_list()           
            v1_end_times = sim_video_df['v1_end_time'].to_list()             
            v2_start_times = sim_video_df['v2_start_time'].to_list()           
            v2_end_times = sim_video_df['v2_end_time'].to_list()              
            sims = sim_video_df['sim'].to_list()                             
            title01s = sim_video_df['title01'].to_list()                 
            title02s = sim_video_df['title02'].to_list()          
            tag_sims = sim_video_df['tag_sim'].to_list()
            
            sim_video_info = zip(videoid01s,
                                 youtubeid01s,
                                 ch_nm1s,
                                 videoid02,
                                 youtubeid02s,
                                 ch_nm2s,
                                 v1_start_times,
                                 v1_end_times,
                                 v2_start_times,
                                 v2_end_times,
                                 sims,
                                 title01s,
                                 title02s,
                                 tag_sims)
            
            video_cnt = len(sim_video_df)
            
        else:
            sim_video_info = list()
            video_cnt = 0
            
    else:
        sim_video_info = list()
        video_cnt = 0

    return sim_video_info, video_cnt

def imgbase_search_sim_video_info(search_video_keyword, search_youtubeid):
    ## 기준 동영상 검색
    search_video_keyword = search_video_keyword.strip()
    if len(search_video_keyword) > 0:
        std_video_df = get_video_by_keyword(search_video_keyword,4)
    else:
        std_video_df = get_video_by_youtubeid(search_youtubeid,4)

    ## 유사동영상 검색    
    if len(std_video_df) > 0:
        for i in range(len(std_video_df)):
            vid = std_video_df.loc[i, 'video_id']
            if i == 0:
                rlt_df = imgbase_get_same_video(vid)
            else:
                rlt_df = pd.concat([rlt_df, imgbase_get_same_video(vid)])

        if len(rlt_df) > 0: 
            videoid01s = rlt_df['videoid1'].to_list()      
            youtubeid01s = rlt_df['youtubeid1'].to_list()          
            videoid02 = rlt_df['videoid2'].to_list()                
            youtubeid02s = rlt_df['youtubeid2'].to_list()              
            v1_start_times = rlt_df['v1_start_time'].to_list()           
            v1_end_times = rlt_df['v1_end_time'].to_list()             
            v2_start_times = rlt_df['v2_start_time'].to_list()           
            v2_end_times = rlt_df['v2_end_time'].to_list()              
            sims = rlt_df['sim'].to_list()                             
            title01s = rlt_df['title01'].to_list()                 
            title02s = rlt_df['title02'].to_list()          

            video_info = zip(videoid01s,
                             youtubeid01s,
                             videoid02,
                             youtubeid02s,
                             v1_start_times,
                             v1_end_times,
                             v2_start_times,
                             v2_end_times,
                             sims,
                             title01s,
                             title02s)
            video_cnt = len(rlt_df)
            
        else:
            video_info = pd.DataFrame()
            video_cnt = 0
            
    else:
        video_info = pd.DataFrame()
        video_cnt = 0
        
    return video_info, video_cnt

def imgbase_get_same_video(vid):
    vid = vid.strip()
    sql_str = f'select videoid1, youtubeid1,ch_nm1, videoid2, youtubeid2, ch_nm2, v1_start_time, v1_end_time, v2_start_time, v2_end_time, sim from anal_search_same_video where videoid1 = "{vid}" and use_yn = "y" and sim < 0.015 order by rand() limit 10 '
    rlt_df = oaislib.fn_get_df_from_lab_db(sql_str)

    ##각 비디오id에 대해서 영상타이틀이 필요함 
    rlt_df["title01"] = 0
    rlt_df["title02"] = 0

    if len(rlt_df) > 0:
        for i in range(len(rlt_df)):
            vid01 = rlt_df.loc[i, 'videoid1']
            sql_str = f'select title from video_syc where video_id = "{vid01}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)

            if len(title_df) > 0:
                title01 = title_df.loc[0, 'title']
            else:
                title01 = ""
                
            rlt_df.loc[i, 'title01'] = title01

            vid02 = rlt_df.loc[i, 'videoid2']
            sql_str = f'select title from video_syc where video_id = "{vid02}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)

            if len(title_df) > 0:
                title02 = title_df.loc[0, 'title']
            else:
                title02=""
                
            rlt_df.loc[i, 'title02'] = title02

    else:
        rlt_df = pd.DataFrame()
        
    return rlt_df

def imgbase_show_all(img_dis, tag_sim_para):
    sql_str = f'select videoid1, youtubeid1,ch_nm1, videoid2, youtubeid2, ch_nm2, v1_start_time, v1_end_time, v2_start_time, v2_end_time, sim from anal_search_same_video where sim < "{img_dis}" and use_yn = "y" and channel_same = "n" order by rand() limit 1000'
    rlt_df = oaislib.fn_get_df_from_lab_db(sql_str)

    ## check tag similarity        
    if len(rlt_df) > 0:
        ##각 비디오id에 대해서 영상타이틀이 필요함 
        rlt_df["title01"] = 0
        rlt_df["title02"] = 0

        ## 태그유사도(tag_sim)가 일정 수준 이상인 것만 한번 더 필터링함
        rlt_df['tag_sim'] = 0 # add column

        for i in range(len(rlt_df)):
            vid01 = rlt_df['videoid1'].iloc[i]
            vid02 = rlt_df['videoid2'].iloc[i]
            tag_sim = get_tag_sim_in_vids(vid01, vid02)
            rlt_df['tag_sim'].iloc[i] = round(tag_sim,3)

        ## filtering
        rlt_df =  rlt_df[rlt_df['tag_sim'] > tag_sim_para]
    else:
        rlt_df = pd.DataFrame()

    ## get title of videos
    ## 다시 if절을 거는 이유는 앞에서 필터링되면서 rlt_df가 null이 되는 경우도 있기에
    if len(rlt_df) > 0 :       
        for i in range(len(rlt_df)):
            vid01 = rlt_df['videoid1'].iloc[i]
            sql_str = f'select title from video_syc where video_id = "{vid01}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)
            if len(title_df) > 0:
                title01 = title_df['title'].iloc[0]
            else:
                title01 = ""
            rlt_df['title01'].iloc[i] = title01

            vid02 = rlt_df['videoid2'].iloc[i]
            sql_str = f'select title from video_syc where video_id = "{vid02}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)
            if len(title_df) > 0:
                title02 = title_df['title'].iloc[0]
            else:
                title02 = ""
            rlt_df['title02'].iloc[i] = title02
            rlt_df['sim'] = round(rlt_df['sim'],3)

    else:
        rlt_df = pd.DataFrame()
        
    return rlt_df

def imgbase_show_all2(img_dis, tag_sim_para):
    sql_str = f'select videoid1, youtubeid1,ch_nm1, videoid2, youtubeid2, ch_nm2, v1_start_time, v1_end_time, v2_start_time, v2_end_time, sim, tag_sim from anal_search_same_video where sim < "{img_dis}" and use_yn = "y" and channel_same = "n" and tag_sim > 0.05 order by rand() limit 1000'
    rlt_df = oaislib.fn_get_df_from_lab_db(sql_str)
    ##각 비디오id에 대해서 영상타이틀이 필요함 
    rlt_df["title01"] = 0
    rlt_df["title02"] = 0
    ## get title of videos
    if len(rlt_df) > 0 :       
        for i in range(len(rlt_df)):
            vid01 = rlt_df['videoid1'].iloc[i]
            sql_str = f'select title from video_syc where video_id = "{vid01}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)
            if len(title_df) > 0:
                title01 = title_df['title'].iloc[0]
            else:
                title01 = ""
            rlt_df['title01'].iloc[i] = title01

            vid02 = rlt_df['videoid2'].iloc[i]
            sql_str = f'select title from video_syc where video_id = "{vid02}"'
            title_df = oaislib.fn_get_df_from_lab_db(sql_str)
            if len(title_df) > 0:
                title02 = title_df['title'].iloc[0]
            else:
                title02 = ""
            rlt_df['title02'].iloc[i] = title02
            rlt_df['sim'] = round(rlt_df['sim'],3)

    else:
        rlt_df = pd.DataFrame()
        
    return rlt_df

def imgbase_show_all_info(img_dis, tag_sim_para):
    
    std_sim_video_df = imgbase_show_all2(img_dis, tag_sim_para)
    video_cnt = len(std_sim_video_df)
    if video_cnt > 0:
        videoid01s = std_sim_video_df['videoid1'].to_list()
        youtubeid01s = std_sim_video_df['youtubeid1'].to_list()
        ch_nm1s = std_sim_video_df['ch_nm1'].to_list()
        videoid02 = std_sim_video_df['videoid2'].to_list()
        youtubeid02s = std_sim_video_df['youtubeid2'].to_list()
        ch_nm2s = std_sim_video_df['ch_nm2'].to_list()
        v1_start_times = std_sim_video_df['v1_start_time'].to_list()
        v1_end_times = std_sim_video_df['v1_end_time'].to_list()
        v2_start_times = std_sim_video_df['v2_start_time'].to_list()
        v2_end_times = std_sim_video_df['v2_end_time'].to_list()
        sims = std_sim_video_df['sim'].to_list()
        title01s = std_sim_video_df['title01'].to_list()
        title02s = std_sim_video_df['title02'].to_list()
        tag_sims = std_sim_video_df['tag_sim'].to_list()

        std_sim_video_info = zip(videoid01s,
                                 youtubeid01s,
                                 ch_nm1s,
                                 videoid02,
                                 youtubeid02s,
                                 ch_nm2s,
                                 v1_start_times,
                                 v1_end_times,
                                 v2_start_times,
                                 v2_end_times,
                                 sims,
                                 title01s,
                                 title02s,
                                 tag_sims)
    else:
        std_sim_video_df = pd.DataFrame()
        video_cnt = 0

    return std_sim_video_info, video_cnt

def get_same_video_search_cnt():
    sql_str = 'select count(*) from anal_search_same_video'
    same_search_cnt = oaislib.fn_get_df_from_lab_db(sql_str)
    return same_search_cnt.iloc[0,0]

def get_today_str():
    now = datetime.now()
    date_str = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
    return date_str

def get_same_video_search_today_cnt():
    today_str = get_today_str()
    sql_str = f'select count(*) from anal_search_same_video where insert_date = "{today_str}"'
    video_today_cnt = oaislib.fn_get_df_from_lab_db(sql_str)
    return video_today_cnt.iloc[0,0]

def get_new_same_video_list():
    sql_str = 'select DISTINCT  c.youtube_id as youtube_id, c.title as title, c.insert_date as insert_date from (select a.youtubeid1 as youtube_id, b.title as title, a.insert_date as insert_date from anal_search_same_video a  join video_syc b  on a.videoid1 = b.VIDEO_ID) c order by c.insert_date desc limit 4'
    same_video_df = oaislib.fn_get_df_from_lab_db(sql_str)
    return same_video_df

def get_survey_score():
    sql_str = 'select score from anal_survey'
    vote_rlt_df = oaislib.fn_get_df_from_lab_db(sql_str)
    
    vote_cnt = len(vote_rlt_df)
    vote_good_cnt = len(vote_rlt_df[vote_rlt_df['score']>2])
    
    return vote_cnt, vote_good_cnt

def get_1_video():
    sql_str = 'select  YOUTUBE_ID, TITLE_ORG , TITLE_MORP_KO from anal_morp order by rand() limit 1'
    video_df = oaislib.fn_get_df_from_lab_db(sql_str)
    rlt = video_df.iloc[0]
    youtube_id = rlt['youtube_id']
    title = rlt['title_org']
    tag = rlt['title_morp_ko']
    return youtube_id, title, tag

def survey_add_score(video_id, score):
    score = int(score)
    sql_str = f'insert into anal_survey (VIDEO_ID ,score ) values("{video_id}","{score}")'
    oaislib.fn_run_sql_to_lab_db(sql_str)

## 두 비디오에 대해서 비디오 유사도를 구함(결과가 없을 수도 있음)
def get_tag_sim_in_vids(vid01, vid02):
    sql_str = f"select SIM from anal_video_similarity_with_morp where VIDEO_ID1 = '{vid01}' and VIDEO_ID2  = '{vid02}'"
    rlt_df = oaislib.fn_get_df_from_lab_db(sql_str)

    if len(rlt_df)  == 1:
        rlt_val = rlt_df['sim'].values[0]
    else:
        rlt_val = 0
    return rlt_val


def make_cloud_image():
    sql="SELECT KEYTAG_ORG FROM anal_morp ORDER BY RAND() LIMIT 200"
    result_df = oaislib.fn_get_df_from_lab_db(sql)

    txt_all = ""
    for i in range(len(result_df)):
        txt = oaislib.fn_get_text_ko(result_df['keytag_org'].iloc[i])
        txt_all = txt_all + txt

    font_path='./static/font/NanumGothic.ttf'
    wordcloud=WordCloud(font_path=font_path,
                        width=1600,
                        height=800,
                        max_font_size=50,
                        max_words=1000,
                        background_color="white").generate(txt_all)

    wordcloud.to_file("./static/img/wordcloud.png")


if __name__ == '__main__':
    '''

    keyword = '문재인'

    vid01 = '048F1B15-FC00-48D8-89D4-7E8B9CF21657'
    vid02 = '354AABA6-4C19-4A36-82CF-AB15E8812133'
    rlt = get_tag_sim_in_vids(vid01, vid02)


    img_dis = 0.02
    tag_sim = 0.1
    rlt = imgbase_show_all_info(img_dis, tag_sim)


    vid = '21C93939-65B0-4C4F-B41D-150204EC226D'
    yid = "CgarPVmMKog"
    cnt = 4
    rlt = imgbase_search_sim_video_info2(vid, yid, cnt)
    
    print(rlt)
    '''
    #imgbase_show_all2(0.1, 0.1)

    yid = 'jnS1zqJR3B8'
    vid = ''
    cnt = 10
    rlt_df =imgbase_search_sim_video_info2(vid, yid, cnt)
    print(rlt_df)

    print("")



