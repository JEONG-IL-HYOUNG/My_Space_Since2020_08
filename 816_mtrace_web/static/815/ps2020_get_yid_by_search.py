import os
import shutil
from urllib.request import urlopen
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')

import oaislib    
    
#20-10에서 가져온 youtube_trend_title(keyword)로 검색했을 때 화면에 보이는 동영상들의 유튜브 아이디 수집
def ps2020():

    input_filepath = 'output/ps2010/y_keyword.csv'
    y_keyword_df = pd.read_csv(input_filepath)

    ## 당일 수집된 키워드에 대해서만 추출
    today_str = oaislib.fn_get_date_str()
    y_keyword_df = y_keyword_df[y_keyword_df['cdate'] == today_str]
    #y_keyword_df = y_keyword_df[:3]
    
    output_filepath = 'output/ps2020/youtube_ids.csv'
    title_cnt = len(y_keyword_df)

    prefix = 'ps2020'
    output_dir = 'output/' + prefix
    oaislib.fn_output_dir_gen(output_dir)

    if title_cnt == 0:
        sys.exit("no today keywords")
    
    for i in range(title_cnt):
        time.sleep(5)
        oaislib.fn_disploop(prefix, i, 10, title_cnt)
        keyword = y_keyword_df['y_keyword'].iloc[i]
        keyword = keyword.encode('utf-8')
        keyword = str(keyword)

        target_url='https://www.youtube.com/results?search_query=' + keyword
        html = urllib.request.urlopen(target_url).read()
        soup = BeautifulSoup(html, 'html.parser')
        pattern = '"\/watch\?v=.{11}"'
        result = re.findall(pattern, str(soup), re.MULTILINE | re.IGNORECASE)
        youtube_ids = [x[10:-1] for x in result]
        youtube_urls = ["https://www.youtube.com/watch?v=" + x for x in youtube_ids]
        youtube_df = pd.DataFrame(columns = ['yid', 'y_url', 'keyword', 'cdate'])
        youtube_df['yid'] = youtube_ids
        youtube_df['y_url'] = youtube_urls
        youtube_df['keyword'] = y_keyword_df['y_keyword'].iloc[i]
        youtube_df['cdate'] = y_keyword_df['cdate'].iloc[i]

        if i == 0:
            output_df = youtube_df.copy()
        else:
            output_df = pd.concat([output_df, youtube_df], axis=0)

    output_df.drop_duplicates(inplace=True, subset=['yid', 'y_url'])
    if os.path.isfile(output_filepath):
        print("yes exist")
        previous_df = pd.read_csv(output_filepath)
        output_df = pd.concat([previous_df, output_df], axis=0)
        output_df.to_csv(output_filepath, index=False)
    else:
        print('nothing, makemake')
        output_df.to_csv(output_filepath, index=False)

if __name__ == '__main__':
    ps2020()
