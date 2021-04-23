from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
'''
config.py에 작성한 항목들을 app.config 환경변수로 읽어들이기 위해 app.config.from_object(config) 문장을 추가.
그리고 전역 변수로 db, migrate 객체를 만들고 create_app 함수에서 init_app 메서드를 이용하여 초기화
플라스크에서 자주 사용되는 패턴
db 객체를 create_app 함수내에서 생성하면 블루프린트와 같은 다른 모듈에서 db객체를 import하여 사용할수 없기 때문에
이처럼 create_app 함수 밖에서 생성하고 실제 객체 초기화는 create_app에서 수행하는 패턴
'''

