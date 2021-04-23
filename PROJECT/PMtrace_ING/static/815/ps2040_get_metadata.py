import os
import shutil
from urllib.request import urlopen
import urllib.request
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import date
import sys

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
    
#여태 수집한 여러 자료들의 메타정보 수집하고 저장하는 코드
def ps2040(dn_num):
    ### I/O name
    input_filepath = 'output/ps2020/youtube_ids.csv'
    output_filepath = 'output/ps2040/youtube_get_metadata.csv'

    prefix ='ps2040'
    output_dir = 'output/' + prefix
    oaislib.fn_output_dir_gen(output_dir)

    
    ### data load
    output_df = pd.DataFrame()
    y_meta_df = pd.read_csv(input_filepath)

    ## 당일 키워드만 가지고 옴
    today_str = oaislib.fn_get_date_str()
    y_meta_df = y_meta_df[y_meta_df['cdate'] == today_str]
    
    #y_meta_df = y_meta_df[:3]
    y_cnt = len(y_meta_df)

    ## 당일 데이터가 없는 경우
    if y_cnt == 0:
        print('ps20_40:: today keywords number is 0')
        sys.exit()

    ## dn_num보다 크면 줄이기
    if y_cnt > dn_num:
        y_meta_df = y_meta_df[:1000]
        y_cnt = len(y_meta_df)
        
    for i in range(y_cnt):
        
        oaislib.fn_disploop(prefix, i, 10, y_cnt)
        time.sleep(5)
        
        url_str = y_meta_df['y_url'].iloc[i]
        target_url = url_str
#        print(target_url)
        html = urllib.request.urlopen(target_url).read()
        soup = BeautifulSoup(html, 'html.parser')

        #유튜브 id 크롤링
        #pattern = '"videoId":".{11}"'
        pattern = 'videoId":"(.*?)"'
        result_id = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        #youtube_ids = [x[11:-1] for x in result_id]
        if len(result_id) >= 1:
            result_youtube_id = result_id[0]
#            print(result_youtube_id)
        else:
            result_youtube_id = -1

        #타이틀 크롤링
        pattern_title = '<title>(.*?)</title>'
        result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_title) >= 1:
            result_youtube_title = result_title[0][:-10]
        #    print(result_youtube_title)
        else:
            result_youtube_title = -1
        #    print(result_youtube_title)

        #조회수 크롤링
        pattern_viewcount = 'viewCount":"(.*?)"'
        result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_viewcount) >= 1 :
            result_youtube_viewcount = result_viewcount[0]
            #print(result_youtube_viewcount)
        else:
            result_youtube_viewcount = -1

        #업로드날짜 크롤링
        pattern_upload = 'uploadDate":"(.*?)"'
        result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_upload) >= 1 :
            result_youtube_upload = result_upload[0]
            #print(result_youtube_upload)
        else:
            result_youtube_upload = -1

        #채널등록자 크롤링
        pattern_owner = 'ownerChannelName":"(.*?)",'
        result_owner = re.findall(pattern_owner, str(soup))
        if len(result_owner) >= 1:
            result_youtube_owner = result_owner[0]
#            print(result_youtube_owner)
        else:
            result_youtube_owner = -1

        #유튜브 tag(keyword) 크롤링
        pattern_tag =  'keywords\\":\[.*?\]'
        tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
        result_tag = [y[11:-1] for y in tag]
        if len(result_tag) >= 1:
            result_youtube_tag = result_tag[0]
#            print(result_youtube_tag)
        else:
            result_youtube_tag = -1

        # 2020-12-08 디스크립션 크롤링 추가
        pattern_descript = 'shortDescription":"(.*?)"'
        result_descript = re.findall(pattern_descript, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_descript) >= 1:
            result_description = result_descript[0]
#            print(result_description)
        else:
            result_description = -1




        new_row = {'yid':result_youtube_id,
                   'y_url':target_url,
                   'title':result_youtube_title,
                   'watch_cnt':result_youtube_viewcount,
                   'y_date':result_youtube_upload,
                   'channel': result_youtube_owner,
                   'tag':result_youtube_tag,
                   'description' : result_description}

        output_df = output_df.append(new_row, ignore_index=True)

    # for문 벗어나서 열을 추가해서 코드 돌린 날짜를 넣기
    output_df['cdate'] = today_str

    output_df.drop_duplicates(inplace=True, subset=['yid', 'y_url'])
    if os.path.isfile(output_filepath):
#        print("yes exist")
        previous_df = pd.read_csv(output_filepath)
        output_df = pd.concat([previous_df, output_df], axis=0)
        output_df.to_csv(output_filepath, index=False)
    else:
        #print('nothing, makemake')
        output_df.to_csv(output_filepath, index=False)
    print()

if __name__ == '__main__':
    ps2040(100)
