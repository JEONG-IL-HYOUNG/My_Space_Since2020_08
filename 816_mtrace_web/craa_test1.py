import re
# regex = re.compile(
#         r'^(?:http|ftp)s?://' # http:// or https://
#         r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
#         r'localhost|' #localhost...
#         r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
#         r'(?::\d+)?' # optional port
#         r'(?:/?|[/?]\S+)$', re.IGNORECASE)
#
# print(re.match(regex, "http://www.example.com/111") is not None) # True
# print(re.match(regex, "https://www.example.com") is not None)            # False
#

import urllib
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# url = 'https://www.youtube.com/watch?v=ygwFy0kcqR8'
# req = Request(url)
#
# from urllib.request import Request, urlopen
# from urllib.error import URLError, HTTPError
# url = 'https://www.youtube.com'
# req = Request(url)
# try:
#     response = urlopen(req).read()
# except HTTPError as e:
#     print('The server couldn\'t fulfill the request.')
#     print('Error code: ', e.code)
# except URLError as e:
#     print('We failed to reach a server.')
#     print('Reason: ', e.reason)
# else:
#     print('aa')
#input_yurl = 'https://www.youtube.com/watch?v=ygwFy0kcqR8'
input_yurl = 'https://www.youtube.'


# input_yurl =''
error = None
https = 'https://'
find_https = input_yurl.find(https)
print(find_https)
print(input_yurl)
if input_yurl == '':
    error = '검색어를 입력하세요!!!'
    print(error)

if error is None:
    expr = re.compile(
        r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]'
        r'+(:[0-9]+)?|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-]*)?\??(?:[-\+=&;%@.\w]*)#?(?:[\w]*))?)')
    if expr.match(input_yurl):
        print('it is valid')
        
