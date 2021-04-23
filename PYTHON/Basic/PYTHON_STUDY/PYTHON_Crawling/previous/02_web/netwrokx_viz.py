# -*- coding: utf-8 -*-
# author : oaiskoo
# date : 2006
# goal : 
#
# desc : 
# desc : 
# desc : 
# desc : 
# desc : 
# desc : 
#
# prss : 
# prss : 
# prss : 
# prss : 
# prss : 
# prss : 

# note
# 20

import os
import shutil
import time
import re
import pandas as pd
import numpy as np
if os.path.exists('../python/oaislib_org.py'):
    shutil.copy('../python/oaislib_org.py', 'oaislib.py')
import oaislib
start = time.time()

import danbi

import numpy as np
import pandas as pd
import re
import networkx as nx
import matplotlib.pyplot as plt
from apyori import apriori
from matplotlib import font_manager

sql_str = 'select TITLE_MORP_KO from anal_morp'
morp_df = oaislib.fn_get_df_from_lab_db(sql_str)
wordset = morp_df['TITLE_MORP_KO'].map(lambda x : oaislib.fn_get_text_ko(x).split())

wordset = [['뷰티', '즌', '에뛰드', '하우스', '크로스핏', '강연', '여름'],
['초콜릿'],
['메이크업', '이사배', '수지', '화보'],
['진짜', '음식', '맛'],
['사과', '티비', '바나나', '티비', '팝콘', '팝콘', '티비', '유나', '하루', '유나'],
['런닝맨', '이광수', '토니안', '김광규', '송중기', '개리', '예능'],
['구구단', '아육대', '개막식'],
['트창', '트위치', '트위치', '하이라이트', '하이라이트', '트창', '화', '트창', '김', '다미'],
['오분', '순삭'],
['토이스토리', '줄거리', '정리', '정리', '시리즈'],
['전남친', '남사', '친'],
['주작'],
['도서관', '대도', '트위치'],
['꽃매미'],
['부동산', '주말', '터', '농막', '농', '땅'],
['슛포', '러브', '자네', '독일'],
['일본', '도쿄', '혐한', '시위', '인터뷰', '도쿄', '올림픽', '시오리', '유튜버', '일본인', '반응'],
['코스트코', '한국'],
['야구', '외야수', '외야'],
['하울', '다이소', '하울', '박템', '쇼핑', '딩고', '다이소'],
['개봉', '기', '개봉', '기'],
['갤럭시', '아이폰'],
['로얄', '픽', '뷰티', '어워즈'],
['베트남'],
['조인성', '정우성', '족구'],
['예비군'],
['신예은', '광고'],
['국악', '소녀', '송소희'],
['워터', '프루프', '메이크업', '워터', '프루프'],
['길거리', '음식', '대림동', '차이나타운', '장수', '커플']]


result = (list(apriori(wordset, min_support=0.001)))
df = pd.DataFrame(result)
df['length'] = df['items'].apply(lambda x: len(x))
df = df[(df['length'] == 2) & (df['support'] > 0.001)].sort_values(by='support', ascending=False)

G = nx.Graph()
ar=(df['items'])
G.add_edges_from(ar)

pr = nx.pagerank(G)
nsize = np.array([v for v in pr.values()])
nsize = 2000 * (nsize - min(nsize)) / (max(nsize) - min(nsize))


font_dirs = ['C:\Windows\Fonts']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)

# 네트워크 그래프
plt.figure(figsize=(1024, 768))
plt.axis('off')
nx.draw_networkx(G,
                 font_family='NanumGothic',
                 node_color=list(pr.values()),
                 node_size=nsize,
                 alpha=0.7,
                 edge_color='.5', 
                 cmap=plt.cm.YlGn)

#plt.show()
plt.savefig('static/img/network.png')


print("time :", time.time() - start)
breakpoint()
