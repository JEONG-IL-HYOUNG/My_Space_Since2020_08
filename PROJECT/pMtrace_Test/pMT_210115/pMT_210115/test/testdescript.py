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

if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib


target_url = "https://www.youtube.com/watch?v=608tfOtduRU"
output_filepath = 'output/ps2040/test_description.csv'
output_df = pd.DataFrame()

print(target_url)
html = urllib.request.urlopen(target_url).read()
soup = BeautifulSoup(html, 'html.parser')

#유튜브 id 크롤링
pattern_descript = 'shortDescription":"(.*?)"'
result_descript = re.findall(pattern_descript, str(soup), re.MULTILINE | re.IGNORECASE)
if len(result_descript) >= 1:
    result_description = result_descript[0]
    print(result_description)
else:
    result_description = -1
    print(result_description)

new_row = {'description' : result_description}
output_df = output_df.append(new_row, ignore_index=True)

if os.path.isfile(output_filepath):
    print("yes exist")
    previous_df = pd.read_csv(output_filepath)
    output_df = pd.concat([previous_df, output_df], axis=0)
    output_df.to_csv(output_filepath, index=False)
else:
    print('nothing, makemake')
    output_df.to_csv(output_filepath, index=False)
