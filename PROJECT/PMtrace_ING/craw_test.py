# 크롤링할때 import
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
import lxml
import requests

# if os.path.exists('../python/oaislib_org.py'):
#     shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib


input_yurl = 'https://www.youtube.com/watch?v=HAlcc-HMz7k'

#search = search_histroy.query.filter_by(seq=input_yurl).first()
##############

html = urllib.request.urlopen(input_yurl).read()
soup = BeautifulSoup(html, 'html.parser')
# 타이틀 크롤링
pattern_title = '<title>(.*?)</title>'
result_title = re.findall(pattern_title, str(soup), re.MULTILINE | re.IGNORECASE)
if len(result_title) >= 1:
    result_youtube_title = result_title[0][:-10]
    print(result_youtube_title)
else:
    result_youtube_title = -1
    print(result_youtube_title)