from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    user_nm = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    pw1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('pw2', '비밀번호가 일치하지 않습니다')])
    pw2 = PasswordField('비밀번호확인', validators=[DataRequired()])


# 로그인 폼
class UserLoginForm(FlaskForm):
    user_nm = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    pw = PasswordField('비밀번호', validators=[DataRequired()])


class post_db_test(FlaskForm):
    prj_nm = StringField('비디오 유알엘', validators=[DataRequired(), Length(min=3, max=250)])