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

#20-10에서 가져온 youtube_trend_title(keyword)로 검색했을 때 화면에 보이는 동영상들의 유튜브 아이디 수집
def get_yid_by_search_df():

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
    get_yid_by_search_df()
