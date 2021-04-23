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
가지고 와야하는 정보들 =()
youtube_id
title : 제목
watch_cnt :  조회수
yid_date: 등록일자
channel_id :  채널ID(등록자)
youtube_tag: 유튜브(태그)

알고리즘
#데이터 로딩
#input 데이터에서 유튭 () 하나씩 처리
    #url주소 하나로 해당 페이지 크롤링
    #크롤링된 페이지 내에서 유튜브 () 추출
        #() 추출하기 위한 정규표현식 작성
        #정규표현식을 하기 위해 크롤링한 페이지의 텍스트중 ()이 들어가 있는 텍스트 일부를 정규표현식 테스트 페이지에서 () 추출표현식 테스트해서 생성
        #찾은 거에 대해 필요 없는 앞뒤 부분 제외
        #비공개 동영상일 경우 예외처리
    #크롤링된 페이지 내에서 유튜브 () 추출
        #() 추출하기 위한 정규표현식 작성
        #정규표현식을 하기 위해 크롤링한 페이지의 텍스트중 ()이 들어가 있는 텍스트 일부를 정규표현식 테스트 페이지에서 () 추출표현식 테스트해서 생성
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
    print(target_url)
    html = urllib.request.urlopen(target_url).read()
    soup = BeautifulSoup(html, 'html.parser')

    #유튜브 id 크롤링
    #pattern = '"videoId":".{11}"'
    pattern = 'videoId":"(.*?)"'
    result_id = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
    #youtube_ids = [x[11:-1] for x in result_id]
    if len(result_id) >= 1:
        result_youtube_id = result_id[0]
        print(result_youtube_id)
    else:
        result_youtube_id = -1


    #타이틀 크롤링
    #pattern_title = '"title\\":\\".*lengthSeconds"'
    pattern_title = 'title":"(.*?)"'
    result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
    #youtube_title = [x[8:-1] for x in result_title]
    '''
    print(type(youtube_title))
    print(youtube_title[0])
    youtube_title2 = youtube_title[0]
    youtube_title3= youtube_title2.split(',')
    print(youtube_title3[0])
    실험삼아 해본 코드 밑에 깔끔하게 정리
    '''
    if len(result_title) >= 1:
        result_youtube_title = result_title[0].split(",")[0]# 패턴에서 title: 부분 지우고, lengthSecond 전까지 잘라내기
        print(result_youtube_title)  # 나중에 삭제해도 되는부분. 확인용이었음
    else:
        result_youtube_title = -1


    #조회수 크롤링
    #pattern_viewcount = '"viewCount\\":\\"\d*"' 기존에 썻던 코드
    pattern_viewcount = 'viewCount":"(.*?)"'
    result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
    #viewcount = [y[13:-1] for y in result_viewcount] # list 형식으로 같은 값을 두개 찾아옴.
    if len(result_viewcount) >= 1 :
        result_youtube_viewcount = result_viewcount[0]
        print(result_youtube_viewcount)
    else:
        result_youtube_viewcount = -1

    #업로드날짜 크롤링
    #pattern_upload = 'uploadDate\\":\\"\S*?,'
    pattern_upload = 'uploadDate":"(.*?)"'
    result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
    #upload_date = [y[13:-4] for y in result_upload]
    if len(result_upload) >= 1 :
        result_youtube_upload = result_upload[0]
        print(result_youtube_upload)
    else:
        result_youtube_upload = -1
    print('')



    #채널등록자 크롤링
    pattern_owner = 'ownerChannelName":"(.*?)",'
    #pattern_owner = 'ownerChannelName\\\":\\\"\S*?\\\",' 기존에 썻던 코드
    result_owner = re.findall(pattern_owner, str(soup))
    #owner = [y[7:-1] for y in result_owner] 기존에 썻던 코드
    if len(result_owner) >= 1:
        result_youtube_owner = result_owner[0]
        print(result_youtube_owner)
    else:
        result_youtube_owner = -1



    ##
    ## 20-10-28 위 까진 정규 표현식을 다 바꾸긴 했음./
    ## 태그 크롤링은 이 방식이 안됨 다른 걸로 바꿔야 할듯

    #유튜브 tag(keyword) 크롤링
    pattern_tag =  'keywords\\":\[.*?\]'
    #pattern_tag = 'keywords":":"(.*?)","' 이 방법은 안됨..
    tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
    result_tag = [y[11:-1] for y in tag]
    if len(result_tag) >= 1:
        result_youtube_tag = result_tag[0]
        print(result_youtube_tag)
    else:
        result_youtube_tag = -1
    print('')

    youtube_metainfo_df = pd.DataFrame(columns=['youtube_id','youtube_url','title','watch_cnt','upload_date', 'channelOwner', 'Tag'])  # ps20-40 데이터 프레임 생성
    '''
    youtube_metainfo_df['youtube_id'] = result_youtube_id
    youtube_metainfo_df['youtube_url'].iloc[i] = target_url
    youtube_metainfo_df['title'].iloc[i] = result_youtube_title
    youtube_metainfo_df['watch_cnt'].iloc[i] = result_youtube_viewcount
    youtube_metainfo_df['upload_date'].iloc[i] = result_youtube_upload
    youtube_metainfo_df['Tag'].iloc[i] = result_youtube_tag
    '''
    new_row = {'youtube_id':result_youtube_id,
               'youtube_url':target_url,
               'title':result_youtube_title,
               'watch_cnt':result_youtube_viewcount,
               'upload_date':result_youtube_upload,
               'channelOwner': result_youtube_owner,
               'Tag':result_youtube_tag}

    output_df = output_df.append(new_row, ignore_index=True)

    #output_df = pd.concat([output_df, youtube_metainfo_df])
    print('')

output_df.to_csv(output_filepath, index=False)


















