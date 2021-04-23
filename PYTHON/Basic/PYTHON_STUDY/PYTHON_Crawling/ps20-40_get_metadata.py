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

#여태 수집한 여러 자료들의 메타정보 수집하고 저장하는 코드
def ps20_40_getmetadata():
    # I/O
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
        pattern_title = 'title":"(.*?)"'
        result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_title) >= 1:
            result_youtube_title = result_title[0].split(",")[0]# 패턴에서 title: 부분 지우고, lengthSecond 전까지 잘라내기
            print(result_youtube_title)  # 나중에 삭제해도 되는부분. 확인용이었음
        else:
            result_youtube_title = -1

        #조회수 크롤링
        pattern_viewcount = 'viewCount":"(.*?)"'
        result_viewcount = re.findall(pattern_viewcount, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_viewcount) >= 1 :
            result_youtube_viewcount = result_viewcount[0]
            print(result_youtube_viewcount)
        else:
            result_youtube_viewcount = -1

        #업로드날짜 크롤링
        pattern_upload = 'uploadDate":"(.*?)"'
        result_upload = re.findall(pattern_upload, str(soup), re.MULTILINE | re.IGNORECASE)
        if len(result_upload) >= 1 :
            result_youtube_upload = result_upload[0]
            print(result_youtube_upload)
        else:
            result_youtube_upload = -1
        print('')

        #채널등록자 크롤링
        pattern_owner = 'ownerChannelName":"(.*?)",'
        result_owner = re.findall(pattern_owner, str(soup))
        if len(result_owner) >= 1:
            result_youtube_owner = result_owner[0]
            print(result_youtube_owner)
        else:
            result_youtube_owner = -1

        #유튜브 tag(keyword) 크롤링
        pattern_tag =  'keywords\\":\[.*?\]'
        tag = re.findall(pattern_tag, str(soup), re.MULTILINE | re.IGNORECASE)
        result_tag = [y[11:-1] for y in tag]
        if len(result_tag) >= 1:
            result_youtube_tag = result_tag[0]
            print(result_youtube_tag)
        else:
            result_youtube_tag = -1
        print('')

        #youtube_metainfo_df = pd.DataFrame(columns=['youtube_id','youtube_url','title','watch_cnt','upload_date', 'channelOwner', 'Tag'])
        new_row = {'youtube_id':result_youtube_id,
                   'youtube_url':target_url,
                   'title':result_youtube_title,
                   'watch_cnt':result_youtube_viewcount,
                   'upload_date':result_youtube_upload,
                   'channelOwner': result_youtube_owner,
                   'Tag':result_youtube_tag}

        output_df = output_df.append(new_row, ignore_index=True)
        print('')
    # for문 벗어나서 열을 추가해서 코드 돌린 날짜를 넣기
    search_date = pd.datetime.now()  # 되긴하는데 다른걸로 바꿔야됨.
    youtube_search_date = search_date.date()
    print(youtube_search_date)
    print('')
    output_df['search date'] = youtube_search_date

    output_df.drop_duplicates(inplace=True, subset=['youtube_id', 'youtube_url'])
    if os.path.isfile(output_filepath):
        print("yes exist")
        output_df.to_csv(output_filepath, mode='a', header=False, index=False)
    else:
        print('nothing, makemake')
        output_df.to_csv(output_filepath, index=False)
    print('')
    return output_df

if __name__ == '__main__':
    ps20_40_getmetadata()
