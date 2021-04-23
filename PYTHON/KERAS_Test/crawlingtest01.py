'''
네이버에서 50장 가져오는건데 이 크롤러는 별로 안좋아보임
'''


from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from urllib.parse import quote_plus

baseUrl = 'https://search.naver.com/search.naver?where=image&sm=tab_jum&query='
plusUrl = input('검색어를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

html = urlopen(url).read()
soup = bs(html, "html.parser")
img = soup.find_all(class_='_img')

print(img[0])

n = 1
for i in img:
    imgUrl = i['data-source']
    with urlopen(imgUrl) as f:
        with open(plusUrl+str(n) + '.jpg', 'wb') as h:
            img = f.read()
            h.write(img)
    n += 1

print('다운로드완료')


