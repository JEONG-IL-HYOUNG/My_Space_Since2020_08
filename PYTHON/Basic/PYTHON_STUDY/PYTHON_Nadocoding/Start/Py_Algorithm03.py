'''
문제 3-1
9월 초의 네이버 종가는 표 3.2와 같습니다. 09/07의 종가를 리스트의 첫 번째 항목으로 입력해서 naver_closing_price라는 이름의 리스트를 만들어보세요.
09/11	금	488,500
09/10	목	500,500
09/09	수	501,000
09/08	화	461,500
09/07	월	474,500

문제 3-2
문제 3-1에서 만든 naver_closing_price를 이용해 해당 주에 종가를 기준으로 가장 높았던 가격을 출력하세요. (힌트: 리스트에서 최댓값을 찾는 함수는 max()이고, 화면에 출력하는 함수는 print()입니다.)

문제 3-3
문제 3-1에서 만든 naver_closing_price를 이용해 해당 주에 종가를 기준으로 가장 낮았던 가격을 출력하세요. (힌트: 리스트에서 최솟값을 찾는 함수는 min()이고, 화면에 출력하는 함수는 print()입니다.)

문제 3-4
문제 3-1에서 만든 naver_closing_price를 이용해 해당 주에서 가장 종가가 높았던 요일과 가장 종가가 낮았던 요일의 가격 차를 화면에 출력하세요..

문제 3-5
문제 3-1에서 만든 naver_closing_price를 이용해 수요일의 종가를 화면에 출력하세요.

문제 3-6
문제 3-1의 표 3.2를 이용해 날짜를 딕셔너리의 키 값으로, 종가를 딕셔너리의 값으로 사용해 naver_closing_price2라는 딕셔너리를 만드세요.

문제 3-7
문제 3-6에서 만든 naver_closing_price2 딕셔너리를 이용해 09/09일의 종가를 출력하세요.
'''

#문제1
naver_closing_price = [474500, 461500, 501000, 500500, 488500]

#문제2,3,4,5
print(max(naver_closing_price))
print(min(naver_closing_price))
print(max(naver_closing_price)-min(naver_closing_price))
print(naver_closing_price[2])

#문제6
naver_closing_price2 = {'09/07':474500, '09/08':461500, '09/09':501000, '09/10': 500500, '09/11':488500}
print(naver_closing_price2)

#문제7
print(naver_closing_price2['09/09'])