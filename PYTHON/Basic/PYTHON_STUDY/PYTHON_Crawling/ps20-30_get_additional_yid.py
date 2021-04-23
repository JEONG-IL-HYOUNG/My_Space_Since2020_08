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

if __name__ == '__main__':
    ps20_30_get_additional_yid()

