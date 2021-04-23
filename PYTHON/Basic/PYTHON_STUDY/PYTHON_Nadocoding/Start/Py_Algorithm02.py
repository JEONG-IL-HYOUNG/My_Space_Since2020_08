'''
ch03. 파이썬 기본 자료구조
'''
########리스트
kospi_top10 = ['삼성전자', 'SK하이닉스', '현대차', '한국전력', '아모레퍼시픽', '제일모직', '삼성전자우', '삼성생명', 'NAVER', '현대모비스']

#append, insert

kospi_top10.append('SK텔레콤')
print(kospi_top10)
kospi_top10[0] = '샘숭전자'
kospi_top10.insert(0,'DAUM')
print(kospi_top10)

print(len(kospi_top10))

del kospi_top10[10:]
print(kospi_top10)

########튜플 수정불가
t = ('Samsung', 'LG', 'SK')
#t.add('xxx') 추가 불가
#t.append('sss')
#t.insert(1,'aaa')
#t[0] = 'Apple' 변경불가
#del t['LG']

print(t)
print(t[0:2])


#####딕셔너리
cur_price = {}
print(type(cur_price))
cur_price['daeshin'] = 30000
print(cur_price)

cur_price['Daum KAKAO'] = 80000
print(cur_price)
print(len(cur_price))
##딕셔너리는 인덱싱을 지원하지 않는다.
#cur_price[0] 오류남
print(cur_price['daeshin'])

cur_price['naver'] = 360000
print(cur_price)

del cur_price['daeshin']
print(cur_price)

cur_price = {'Daum KAKAO': 80000, 'naver':800000, 'daeshin':30000}
print(cur_price)

print(cur_price.keys())
print(list(cur_price.keys()))
print()
print()

stock_list = list(cur_price.keys())
print(stock_list)

price_list = list(cur_price.values())
print(price_list)

print('Samsung' in cur_price.keys())
