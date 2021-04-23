import os
import shutil
from urllib.request import urlopen
import urllib.request
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
'''
가지고 와야하는 정보들
youtube_id
title : 제목
watch_cnt :  조회수
yid_date: 등록일자
channel_id :  채널ID(등록자)
youtube_tag: 유튜브(태그)
'''

'''
알고리즘
#데이터 로딩
#input 데이터에서 유튭 url 하나씩 처리
    #url주소 하나로 해당 페이지 크롤링
    #크롤링된 페이지 내에서 유튜브 title 추출
        #title 추출하기 위한 정규표현식 작성
        #정규표현식을 하기 위해 크롤링한 페이지의 텍스트중 title이 들어가 있는 텍스트 일부를 정규표현식 테스트 페이지에서 title 추출표현식 테스트해서 생성
        #찾은 거에 대해 필요 없는 앞뒤 부분 제외
    #크롤링된 페이지 내에서 유튜브 watch_cnt 추출
        #watch_cnt 추출하기 위한 정규표현식 작성
        #정규표현식을 하기 위해 크롤링한 페이지의 텍스트중 watch_cnt이 들어가 있는 텍스트 일부를 정규표현식 테스트 페이지에서 watch_cnt 추출표현식 테스트해서 생성
        #찾은 거에 대해 필요 없는 앞뒤 부분 제외     
    
'''
#I/O
input_filepath = 'output/ps20-30/youtube_ids_additional.csv'
youtube_metadata_df = pd.read_csv(input_filepath)

output_filepath = 'output/ps20-40/youtube_get_metadata.csv'

output_df = pd.DataFrame()

for i in range(len(youtube_metadata_df)):
    print(i)
    url_str = youtube_metadata_df['youtube_url'].iloc[i]


    target_url = url_str
    html = urllib.request.urlopen(target_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    soup_str = str(soup)
    soup_str= '"ownerChannelName\":\"Tottenham Hotspur\",\"uploadDate\":\"2020-10'
    #타이틀 크롤링
    pattern_title = '"title\\":\\".*lengthSeconds"'
    result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
    youtube_title = [x[8:-1] for x in result_title]
    '''
    print(type(youtube_title))
    print(youtube_title[0])
    youtube_title2 = youtube_title[0]
    youtube_title3= youtube_title2.split(',')
    print(youtube_title3[0])
    실험삼아 해본 코드 밑에 깔끔하게 정리
    '''
    result_youtube_title = youtube_title[0].split(",")[0] # 패턴에서 title: 부분 지우고, lengthSecond 전까지 잘라내기
    print(result_youtube_title) # 나중에 삭제해도 되는부분. 확인용이었음

    #조회수 크롤링
    pattern_viewcount = '"viewCount\\":\\"\d*"'
    result_viewcount = re.findall(pattern_viewcount, soup_str, re.MULTILINE | re.IGNORECASE)
    viewcount = [y[13:-1] for y in result_viewcount] # list 형식으로 같은 값을 두개 찾아옴.
    if len(viewcount) > 1 :
        result_youtube_viewcount = viewcount[0]
        print(result_youtube_viewcount)
    else:
        result_youtube_viewcount = -1

    #업로드날짜 크롤링
    pattern_upload = 'uploadDate\\":\\"\S*?,'
    result_upload = re.findall(pattern_upload, soup_str, re.MULTILINE | re.IGNORECASE)
    print((result_upload))
    print('')

    '''
    #채널등록자 크롤링
    pattern_owner = 'ownerChannelName\\\":\\\"\S*?\\\",'
    #pattern_owner = 'ownerChannelName\'
    result_owner = re.findall(pattern_owner, soup_str)
    print(result_owner)
    owner = [y[7:-1] for y in result_owner]
    print(owner)

    '''


    print('')


    youtube_metainfo_df = pd.DataFrame(columns=['youtube_url', 'title','viewcount'])  # ps10-30 데이터 프레임 생성
    youtube_metainfo_df['youtube_url'] = target_url
    youtube_metainfo_df['title'] = result_youtube_title
    youtube_metainfo_df['viewcount'] = result_youtube_viewcount






    print(" ")













