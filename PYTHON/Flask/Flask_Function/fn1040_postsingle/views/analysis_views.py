from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
#from .auth_views import login_required


bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/analysis/', methods=('GET', 'POST'))
def analysis():
    if request.method == 'POST':
        result = request.form['video_url']
        #return 'post로 전달된 데이터({})'.format(result)
        return render_template('analysis.html', vvvvv = result)
    else:
        return '포스트로 안넘어왔음'


