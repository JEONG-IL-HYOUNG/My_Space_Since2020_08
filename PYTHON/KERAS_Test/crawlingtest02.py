from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import os

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('created '+directory)
    except OSError:
        print('Error : already Created' + directory)

search = input('검색 ')
createFolder('data/'+search)
print('1')
##여기 url 가져오는 부분이 직접 입력을 해야하는거같음.. 일단
url = f'https://www.google.co.kr/search?q={quote_plus(search)}&tbm=isch&ved=2ahUKEwiJmJPTxp_sAhX0xIsBHQ0pBC0Q2-cCegQIABAA&oq=cat&gs_lcp=CgNpbWcQAzICCAAyBQgAELEDMgIIADIFCAAQsQMyBQgAELEDMgUIABCxAzICCAAyAggAMgIIADICCAA6CAgAELEDEIMBUIYhWIgnYL8oaABwAHgAgAF6iAHWBJIBAzAuNZgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=Nit8X4mlMPSJr7wPjdKQ6AI&bih=888&biw=1920&hl=ko'

print("2")
driver = webdriver.Chrome("D:\D@MyStudy\GITHUB\GITHUB_STUDY\pythonProject\chromedriver.exe")
driver.get(url)
print("3")
options = webdriver.ChromeOptions()
print("4")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
print("5")
driver.get(url)
print("6")
for i in range(2000):
    driver.execute_script("window.scrollBy(0,100000)")
html = driver.page_source
print("7")
soup = BeautifulSoup(html, features="html.parser")
print("8")
img = soup.select('img')

n = 1
imgurl = []

for i in img:
    try:
        imgurl.append(i.attrs["src"])
    except KeyError:
        imgurl.append(i.attrs["data-src"])

for i in imgurl:
    urlretrieve(i, "data/"+ search +'/' + str(n) + ".jpg")
    n += 1
    print('downloading.........{}'.format(n))

driver.close()


