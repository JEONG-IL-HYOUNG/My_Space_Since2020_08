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

import oaislib    
    
def fn_get_clean_text(text):
    text = str(text)
    text = text.replace("\\", "")  # 위의 표현으로 역슬래시가 제거가 안되어서 추가함
    text = re.sub('[-=+,#/\?:^⭐☆＂ㅣ’$.,💫”"@🕺*\"※~💉&%😍🥶🤬💚🚞♨☞♬ㆍ!ㅡ』\\;_‘|\(\)\[\]\<\>`\'…》`]', '', text)
    return text

#유튜브 유튜브 인기동영상 페이지에서 제목을 가져오는 코드
def ps2010():
    # I/O
    target_url = "https://www.youtube.com/feed/trending"
    output_filepath = 'output/ps2010/y_keyword.csv'


    prefix = 'ps2010'
    output_dir = 'output/' + prefix
    oaislib.fn_output_dir_gen(output_dir)

    
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
    y_trend_keywords = trend_title.split()

    ##한 글자만 있는경우 삭제
    for i in range(len(y_trend_keywords)):
        #print(type(y_trend_keywords[i]))
        if len(y_trend_keywords[i]) <= 1:
            y_trend_keywords[i] = ''

    ##집합형으로 중복문자 삭제 후 다시 리스트 변환
    my_set = set(y_trend_keywords)
    y_trend_keywords = list(my_set)

    ##공백문자 삭제
    y_trend_keywords = [x for x in y_trend_keywords if x]

    #날짜 넣기
    trend_keyword_df = pd.DataFrame(columns=['y_keyword','cdate'])
    trend_keyword_df['y_keyword'] = y_trend_keywords

    ## 중복제거 
    trend_keyword_df.drop_duplicates(inplace=True, subset=['y_keyword'])

    ## 날짜 추가
    today_str = oaislib.fn_get_date_str()
    trend_keyword_df['cdate'] = today_str

    if os.path.isfile(output_filepath):
        print("yes exist")
        previous_df = pd.read_csv(output_filepath)
        output_df = pd.concat([previous_df, trend_keyword_df], axis=0)
        output_df.to_csv(output_filepath, index=False)
    else:
        print('nothing, makemake')
        trend_keyword_df.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    ps2010()
