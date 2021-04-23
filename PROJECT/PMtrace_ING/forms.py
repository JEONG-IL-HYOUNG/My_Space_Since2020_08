from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    user_nm = StringField('ID', validators=[DataRequired(), Length(min=3, max=25)])
    pw1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('pw2', '비밀번호가 일치하지 않습니다')])
    pw2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    user_rnm = StringField('ID', validators=[DataRequired()])
    email =  StringField('EMAIL', validators=[DataRequired()])
    phone =  StringField('PHONE', validators=[DataRequired()])


# 로그인 폼
class UserLoginForm(FlaskForm):
    user_nm = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    pw = PasswordField('비밀번호', validators=[DataRequired()])


class post_db_test(FlaskForm):
    prj_nm = StringField('비디오 유알엘', validators=[DataRequired(), Length(min=3, max=250)])
    seq = StringField('테스트search', validators=[DataRequired(), Length(min=3, max=250)])

#아이디 찾기 폼
class SearchIdForm(FlaskForm):
    user_rnm = StringField('ID', validators=[DataRequired()])
    email = StringField('EMAIL', validators=[DataRequired()])
    phone = StringField('PHONE', validators=[DataRequired()])

#비밀번호 찾기 폼
class SearchPwForm(FlaskForm):
    user_nm = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    user_rnm = StringField('ID', validators=[DataRequired()])
    email = StringField('EMAIL', validators=[DataRequired()])
    phone = StringField('PHONE', validators=[DataRequired()])
    pw1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('pw2', '비밀번호가 일치하지 않습니다')])
    pw2 = PasswordField('비밀번호확인', validators=[DataRequired()])