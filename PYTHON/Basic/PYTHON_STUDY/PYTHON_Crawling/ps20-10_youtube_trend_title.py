import os
import shutil
from urllib.request import urlopen
import urllib.request
from urllib import parse
import re
from bs4 import BeautifulSoup
import pandas as pd
import datetime

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')

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

if __name__ == '__main__':
    ps20_10_youtube_trend_title()