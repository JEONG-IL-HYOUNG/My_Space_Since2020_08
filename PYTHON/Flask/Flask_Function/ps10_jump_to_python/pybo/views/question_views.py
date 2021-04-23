from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)  # 페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    #폼 전송이 POST로 요청된 경우 질문데이터를 한건 등록하도록 수정, form.validate_on_submit() 은 POST로 전송된 폼 데이터의 정합성을 체크
    #폼 데이터의 정합성은 폼 작성시 생성했던 DataRequired() 같은 체크항목을 말한다.
    #폼으로 전송된 "제목"은 form.subject.data 처럼 data속성을 사용하여 얻을 수 있다.    # POST로 전송된 데이터의 저장이 완료되면 메인화면(main.index)으로 리다이렉트


    return render_template('question/question_form.html', form=form)#create함수는 QuestionForm을 사용한다.
# QuestionForm은 질문을 등록하기 위해 사용할 플라스크의 폼(Form)이다.
# render_template 함수는 템플릿 렌더시 QuestionForm의 객체 form을 전달.
# form 객체는 템플릿에서 라벨이나 입력폼등을 만들때 필요하다.