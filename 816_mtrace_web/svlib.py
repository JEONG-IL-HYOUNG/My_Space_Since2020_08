import os
import shutil
from urllib.request import urlopen
import urllib.request
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
#
# if os.path.exists('../python/oaislib_org.py'):
#     shutil.copy('../python/oaislib_org.py', 'oaislib.py')

#ps20-10
#유튜브 유튜브 인기동영상 페이지에서 제목을 가져오는 코드
def ps20_10_youtube_trend_title():
    def fn_get_clean_text(text):
        text = str(text)
        text = text.replace("\\", "")  # 위의 표현으로 역슬래시가 제거가 안되어서 추가함
        text = re.sub('[-=+,#/\?:^⭐☆＂ㅣ’$.,💫”"@🕺*\"※~💉&%😍🥶🤬💚🚞♨☞♬ㆍ!ㅡ』\\;_‘|\(\)\[\]\<\>`\'…》`]', '', text)
        return text

    output_df = pd.DataFrame()
    # I/O
    target_url = "https://www.youtube.com/feed/trending"
    output_filepath = 'output/ps20-10/youtube_trend_title.csv'

    #Crawling
    html = urllib.request.urlopen(target_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    #타이틀 가져오기 이 여기 정규표현식이 깔끔하게 처리가 안됨..
    pattern = 'title":{.*?}'
    #pattern = 'title":"(.*?)"'
    result_title = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
    trend_title = [x[25:-2] for x in result_title]
    print(trend_title)
    print('')

    #특수문자 삭제하는 함수
    trend_title = fn_get_clean_text(trend_title)
    print(trend_title)

    # 띄어쓰기 기준(어절) 나누기
    youtube_trend_title = trend_title.split()

    ##한 글자만 있는경우 삭제
    for i in range(len(youtube_trend_title)):
        #print(type(youtube_trend_title[i]))
        if len(youtube_trend_title[i]) <= 1:
            youtube_trend_title[i] = ''
    #집합형으로 중복문자 삭제 후 다시 리스트 변환
    my_set = set(youtube_trend_title)
    youtube_trend_title = list(my_set)
    #공백문자 삭제
    youtube_trend_title = [x for x in youtube_trend_title if x]

    #날짜 넣기
    search_date = pd.datetime.now() # 되긴하는데 다른걸로 바꿔야됨.
    youtube_search_date = search_date.date()
    print(youtube_search_date)
    print('')
    trend_title_df = pd.DataFrame(columns=['date', 'youtube_trend_title'])
    trend_title_df['youtube_trend_title']= youtube_trend_title
    trend_title_df['date'] = youtube_search_date

    output_df = pd.concat([output_df, trend_title_df])

    if os.path.isfile(output_filepath):
        print("yes exist")
        output_df.to_csv(output_filepath, mode='a', header=False, index=False)
    else:
        print('nothing, makemake')
        output_df.to_csv(output_filepath, index=False)
    return output_df

#ps20-20
#20-10에서 가져온 youtube_trend_title(keyword)로 검색했을 때 화면에 보이는 동영상들의 유튜브 아이디 수집
def ps20_20_get_yid_by_search_df():
    input_filepath = 'output/ps20-10/youtube_trend_title.csv'
    youtube_trend_title_df = pd.read_csv(input_filepath)
    output_filepath = 'output/ps20-20/youtube_ids.csv'
    output_df = pd.DataFrame()
    for i in range(len(youtube_trend_title_df)):
        print(i)
        keyword = youtube_trend_title_df['youtube_trend_title'].iloc[i]
        keyword = keyword.encode('utf-8')
        keyword = str(keyword)

        target_url='https://www.youtube.com/results?search_query=' + keyword
        html = urllib.request.urlopen(target_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        pattern = '"\/watch\?v=.{11}"'
        result = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        youtube_ids = [x[10:-1] for x in result]
        youtube_urls = ["https://www.youtube.com/watch?v=" + x for x in youtube_ids]
        youtube_df = pd.DataFrame(columns = ['youtube_id', 'youtube_url', 'keyword', 'date'])
        youtube_df['youtube_id'] = youtube_ids
        youtube_df['youtube_url'] = youtube_urls
        youtube_df['keyword'] = youtube_trend_title_df['youtube_trend_title'].iloc[i]
        youtube_df['date'] = youtube_trend_title_df['date']
        output_df = pd.concat([output_df, youtube_df])
        print('')


    output_df.drop_duplicates(inplace=True, subset=['youtube_id', 'youtube_url'])
    if os.path.isfile(output_filepath):
        print("yes exist")
        output_df.to_csv(output_filepath, mode='a', header=False, index=False)
    else:
        print('nothing, makemake')
        output_df.to_csv(output_filepath, index=False)
    print('')
    return output_df

#ps20-30
#20-20에서 가져온 유튜브 아이디 값으로 웹페이지 접속했을때
#옆에 보이는 관련동영상 부분의 유튜브 아이디를 가져 오는 코드
def ps20_30_get_additional_yid():
    # I/O
    input_filepath = 'output/ps20-20/youtube_ids.csv'
    youtube_ids_df = pd.read_csv(input_filepath)
    output_filepath = 'output/ps20-30/youtube_ids_additional.csv'
    output_df = pd.DataFrame()
    for i in range(len(youtube_ids_df)):
        print(i)
        url_str = youtube_ids_df['youtube_url'].iloc[i]
        keyword_str = youtube_ids_df['keyword'].iloc[i]
        target_url = url_str
        html = urllib.request.urlopen(target_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        pattern = '"videoId":".{11}"'
        result = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        youtube_ids = [x[11:-1] for x in result]
        youtube_urls = ["https://www.youtube.com/watch?v=" + x for x in youtube_ids]
        youtube_df = pd.DataFrame(columns=['youtube_id', 'youtube_url','keyword'])  # ps10-30 데이터 프레임 생성
        youtube_df['youtube_id'] = youtube_ids
        youtube_df['youtube_url'] = youtube_urls
        youtube_df['keyword'] = keyword_str

        output_df = pd.concat([output_df, youtube_df])
        print('')
    #for문 벗어나서 열을 추가해서 코드 돌린 날짜를 넣기
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
    ps20_10_youtube_trend_title()
    ps20_20_get_yid_by_search_df()
    ps20_30_get_additional_yid()
    ps20_40_getmetadata()