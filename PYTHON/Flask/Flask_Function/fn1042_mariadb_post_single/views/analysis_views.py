from flask import Blueprint, url_for, render_template, request
from werkzeug.utils import redirect
from .auth_views import login_required


bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@bp.route('/analysis/', methods=('GET', 'POST'))
def analysis():
    if request.method == 'POST':
        return render_template('analysis.html')
    else:
        return '포스트로 안넘어왔음'

