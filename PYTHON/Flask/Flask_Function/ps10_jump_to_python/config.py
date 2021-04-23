import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False #이벤트처리옵션, 추가메모리사용 일단은 사용안함

SECRET_KEY = "dev"
#Flask-WTF를 사용하기 위해 플라스크 환경변수 SECRET_KEY