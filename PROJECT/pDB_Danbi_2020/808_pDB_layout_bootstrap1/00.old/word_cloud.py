# Display the generated image:
# the matplotlib way:
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

from IPython import get_ipython
ipy = get_ipython()
if ipy is not None:
    ipy.run_line_magic('matplotlib', 'inline')

# currentPath = os.getcwd()
# print(currentPath)

# path = 'C:/Users/velbetwise/AppData/Local/Microsoft/Windows/Fonts/NanumGothic.ttf'
# font_name = fm.FontProperties(fname=path).get_name()

# plt.rc('font', family=font_name)

df = pd.read_csv('worddata.csv')

df.head()

font_path = 'NanumFont_TTF_ALL/NanumGothic.ttf'

text = df['text'].values

wordcloud = WordCloud(    font_path = font_path,
                          width = 800,
                          height = 800,
                          max_font_size=50,
                          max_words=100,
                          background_color="white").generate(str(text))

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

wordcloud.to_file("static/img/first_review.png")

#plt.savefig('static/img/wordcloud.svg')
