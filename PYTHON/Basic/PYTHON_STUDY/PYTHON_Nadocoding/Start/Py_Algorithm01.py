'''
https://wikidocs.net/2843
파이썬으로 배우는 알고리즘 트레이딩
ch02 까지
'''

test1 = 'naver daum'
test1.split(' ')
print(test1.split(' '))
print(test1)
test1.split(' ')[0]
print(test1.split(' ')[0])

'''
문제 2-1 다음(Daum)의 주가가 89,000원이고 네이버(Naver)의 주가가 751,000원이라고 가정하고,
        어떤 사람이 다음 주식 100주와 네이버 주식 20주를 가지고 있을 때 그 사람이 가지고 있는 주식의 총액을 계산하는 프로그램을 작성하세요.
        
문제 2-2 문제 2-1에서 구한 주식 총액에서 다음과 네이버의 주가가 각각 5%, 10% 하락한 경우에 손실액을 구하는 프로그램을 작성하세요.

문제 2-3 우리나라는 섭씨 온도를 사용하는 반면 미국과 유럽은 화씨 온도를 주로 사용합니다. 화씨 온도(F)를 섭씨 온도(C)로 변환할 때는 다음과 같은 공식을 사용합니다. 
        이 공식을 사용해 화씨 온도가 50일 때의 섭씨 온도를 계산해 보세요. C = (F-32)/1.8        
        
문제 2-4 화면에 "pizza"를 10번 출력하는 프로그램을 작성하세요.

문제 2-5 월요일에 네이버의 주가가 100만 원으로 시작해 3일 연속으로 하한가(-30%)를 기록했을 때 수요일의 종가를 계산해 보세요.

문제 2-6 다음 형식과 같이 이름, 생년월일, 주민등록번호를 출력하는 프로그램을 작성해 보세요. 이름: 파이썬 생년월일: 2014년 12월 12일 주민등록번호: 20141212-1623210

문제 2-7 s라는 변수에 'Daum KaKao'라는 문자열이 바인딩돼 있다고 했을 때 문자열의 슬라이싱 기능과 연결하기를 이용해 s의 값을 'KaKao Daum'으로 변경해 보세요.

문제 2-8 a라는 변수에 'hello world'라는 문자열이 바인딩돼 있다고 했을 때 a의 값을 'hi world'로 변경해 보세요.

문제 2-9 x라는 변수에 'abcdef'라는 문자열이 바인딩돼 있다고 했을 때 x의 값을 'bcdefa'로 변경해 보세요.

'''
print()
#2-1
daum = 89000
naver = 751000
total = daum*100 + naver*20
print(total)
print()

#2-2 손실액구하기
daum1 = daum*0.05 *100
naver1 = naver*0.1*20
loss = daum1 + naver1
print(loss)

#2-3 화씨 온도 50일 때 섭씨 온도. C = (F-32)/1.8
faren = input('화씨 온도를 입력하세여: ')
celsius  = (int(faren) - 32) / 1.8
print(celsius)

#2-4
print('pizza\n' *10 )

#2-5 100만 원으로 시작해 3일 연속으로 하한가(-30%)를 기록했을 때 수요일의 종가

monday = 1000000
#3일 연속 하한가
wendesdayend = 1000000 *0.7*0.7*0.7
print(wendesdayend)

#2-6은 너무 쉽고

#2-7 'Daum KaKao' 문자열의 슬라이싱 기능과 연결하기를 이용해 s의 값을 'KaKao Daum'으로 변경
kakao = 'Daum KaKao'
kakao1 = kakao[-5:] + ' ' + kakao[:4]
print(kakao1)

#2-8 a라는 변수에 'hello world'라는 문자열이 바인딩돼 있다고 했을 때 a의 값을 'hi world'로 변경
a = 'hello world'
a1 = a.replace('hello', 'hi')
print(a1)

#2-9 x라는 변수에 'abcdef'라는 문자열이 바인딩돼 있다고 했을 때 x의 값을 'bcdefa'로 변경

x = 'abcdef'
x1= x[1:] + x[0]
print(x1)